# CampusGuard

> Tap for help. Report for prevention. Stay safe.

CampusGuard is a local campus safety dispatch board. Students send an SOS or report a danger, security officers triage and update incidents, and administrators generate weekly prevention insights.

Built with FastAPI, SQLite, React/Vite, and local Gemma through Ollama. No external AI APIs, websockets, maps, or push services. Includes simple role-based login.

## Screenshots

![Student SOS](docs/screenshots/student-sos.png)
![Dispatch dashboard](docs/screenshots/dispatch-dashboard.png)
![Weekly insights](docs/screenshots/weekly-insights.png)

## Quick start

**Requirements:** Python 3.10+, Node.js 18+ with npm, and [Ollama](https://ollama.com) for Gemma-powered triage and narratives. Ollama is optional: without it, CampusGuard uses local fallbacks.

Open two terminals at the project root.

**Backend**

```powershell
irm https://ollama.com/install.ps1 | iex
pip install -r requirements.txt
ollama pull gemma3:1b
python seed.py
uvicorn main:app --host 0.0.0.0
```

`seed.py` loads 30 reports plus SOS hotspot data. It is safe to rerun: it resets alerts, status history, and insights, but keeps registered users and responders.

To keep client IPs out of access logs during an anonymous-report demo, add `--no-access-log`.

**Frontend**

```powershell
cd web
npm install
npm run dev
```

Open <http://localhost:5173/>. Vite proxies `/api` to FastAPI at `http://127.0.0.1:8000`. Check a production build with `npm run build`.

### Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama endpoint |
| `OLLAMA_MODEL` | `gemma3:1b` | Model name |
| `OLLAMA_TIMEOUT` | `8` | Request timeout (seconds) |
| `VITE_CAMPUS_EMERGENCY_NUMBER` | `911` | Number shown on SOS confirmation |
| `VITE_HTTPS_KEY`, `VITE_HTTPS_CERT` | unset | Certificate paths for HTTPS dev server |

### Phone demo (HTTPS)

Browsers only allow geolocation on HTTPS or localhost. To demo on a phone:

1. Install [mkcert](https://github.com/FiloSottile/mkcert), then from `web` run:

   ```powershell
   mkcert -install
   mkcert 192.168.1.50 localhost 127.0.0.1
   mkcert -CAROOT
   ```

   Use your laptop's real LAN IP in place of `192.168.1.50`. The last command prints the directory containing `rootCA.pem`.

2. Copy `rootCA.pem` to the phone and install it as a trusted CA certificate. Trusting it only on the laptop is not enough.
3. Put the phone and laptop on the same Wi-Fi network or hotspot, and allow inbound TCP ports 5173 and 8000 through Windows Firewall.
4. Start Vite with the generated certificate:

   ```powershell
   $env:VITE_HTTPS_KEY = "C:\path\to\192.168.1.50+2-key.pem"
   $env:VITE_HTTPS_CERT = "C:\path\to\192.168.1.50+2.pem"
   npm run dev
   ```

5. Open `https://192.168.1.50:5173` on the phone.

Vite listens on the LAN (`host: true`) and serves HTTPS when both certificate variables point to existing files.

## Demo accounts

| Account | Role | Access |
| --- | --- | --- |
| `student` / `student123` | Student | Submit SOS and danger reports |
| `responder` / `responder123` | Responder | Dispatch and Insights |
| `admin` / `admin123` | Admin | Admin, Dispatch, and Insights |

These credentials are for the local prototype only. **Replace them before any deployment.** Admin and responder API routes require a SQLite-backed bearer session. **Log out** invalidates the session and removes the browser token.

## Routes

| Route | Purpose |
| --- | --- |
| `/` | Mobile-first student app: SOS and danger reports |
| `/login` | Role-based sign-in |
| `/dashboard` | Dispatch ledger with SOS banner, polling, and status controls |
| `/insights` | SQL statistics, SVG charts, and Gemma prevention narrative |
| `/admin` | System health, summary stats, recent alerts, and the responder directory |

## How it works

CampusGuard uses Gemma as a local decision-support assistant. It does not replace security staff, dispatch emergency services, or make final decisions. Everything keeps working with explicit fallbacks when Ollama or Gemma is unavailable.

```text
Student sends SOS or report -> saved immediately -> fallback triage sets initial priority
    -> Gemma refines summary and action in the background
    -> Admin/responder reviews in Dispatch -> New -> Investigating -> Resolved
    -> Insights summarizes activity and recommends prevention actions
```

### SOS

SOS never waits for AI.

1. The student taps **SOS**. The browser tries to collect GPS; the SOS still sends if permission is denied.
2. `POST /api/sos` saves an `emergency` alert with a fixed response message. Ollama is not called.
3. The alert is logged and appears at the top of Dispatch.
4. The confirmation shows the campus emergency number and **Sent by mistake? Cancel** for 10 seconds. Cancelling marks the alert `Resolved`, logs it, and adds the note `SOS cancelled by student within 10 seconds.`

### Danger reports and Gemma triage

1. The student picks a category and location, writes a description, and may choose anonymous reporting.
2. `POST /api/reports` validates the request, generates fallback triage, and saves the report with `triage_source = fallback`. The student gets an immediate response.
3. A background task sends the category, location, and description to Ollama (`/api/generate`) and shows an **AI PENDING** tag until it finishes.
4. Gemma returns JSON with `priority`, `location`, `summary`, and `recommended_action`. CampusGuard accepts it only if priority is `low`, `medium`, `high`, or `emergency`, text fields are non-empty, and the summary is 30 words or fewer. Valid results update the report and set `triage_source = gemma`.
5. Security reviews the suggestion and controls the final status.

Safeguards:

- **Priority floor:** stored priority is `max(fallback, Gemma)` over `low < medium < high < emergency`. Gemma can improve the summary and action but never lower a keyword-detected priority.
- **Prompt injection:** the description is wrapped in `<report_description>` delimiters and treated as untrusted data. Gemma is told not to identify or accuse anyone.
- **Latency:** requests use a JSON schema `format` and `keep_alive` of `30m`, and the model is warmed at startup.
- **Failure:** if Ollama is stopped, the model is missing, the request times out, or the JSON is invalid, the fallback result stays saved.

Example input and result:

```json
{
  "category": "suspicious person",
  "description": "A person has been watching students near the entrance.",
  "location": "Hostel Gate",
  "anonymous": true
}
```

```json
{
  "priority": "high",
  "location": "Hostel Gate",
  "summary": "Person observed watching students near the entrance.",
  "recommended_action": "Review CCTV and dispatch security to assess the area."
}
```

### Dispatch

The dashboard polls `GET /api/alerts`, keeps SOS alerts on top, and shows location, category, priority, summary, recommended action, triage source, and an `AI: online | offline | checking` indicator (from `GET /api/health`). Status changes go through `PATCH /api/alerts/{id}/status` and are recorded in `status_log`.

### Weekly insights

1. An admin or responder opens `/insights` and clicks **Generate this week's report**.
2. `POST /api/insights/generate` computes statistics: incident, SOS, and high-priority totals, categories, and locations.
3. Only those statistics go to Gemma, which writes a short summary and numbered recommendations from them alone. If Gemma is unavailable, a built-in fallback narrative is used.
4. Results are saved in the `insights` table and shown with charts, hotspots, and **AVG RESOLUTION**: minutes from first `New` to first `Resolved`, excluding cancelled SOS alerts.

Retrieve the latest report with `GET /api/insights/latest`.

### Responder directory

Under **People who can resolve issues**, admins maintain a directory of responders (Police, Guardian, Campus security, Medical responder, Other) with name, role, phone, optional email, and notes. It is a directory only: CampusGuard does not contact or dispatch anyone. Dispatch remains the source of truth for SOS handling.

## API

| Endpoint | Description |
| --- | --- |
| `POST /api/sos` | Send an SOS |
| `POST /api/sos/{id}/cancel` | Cancel an SOS within 10 seconds |
| `POST /api/reports` | Submit a danger report |
| `GET /api/alerts` | List alerts |
| `PATCH /api/alerts/{id}/status` | Update alert status |
| `GET /api/health` | Ollama availability |
| `GET /api/admin/overview` | Summary statistics and recent alerts |
| `GET /api/admin/responders` | List responders |
| `POST /api/admin/responders` | Add a responder |
| `DELETE /api/admin/responders/{id}` | Remove a responder |
| `POST /api/auth/login` | Create a local role session |
| `POST /api/insights/generate` | Generate weekly insights |
| `GET /api/insights/latest` | Fetch the latest insights |

## Three-minute demo

1. On the laptop, sign in at `/login` as `responder` / `responder123`.
2. On the phone, open `/` and tap **SOS**. Show the confirmation and the cancel option, then confirm the red SOS band on Dispatch and the AI status indicator.
3. On the phone, choose **Report a danger**, select `suspicious person` and **Hostel Gate**, add a short description, and submit.
4. On Dispatch, watch **AI PENDING** change to Gemma's result (or the fallback if Ollama is offline).
5. Mark the report **Investigating**, then open `/insights`, generate the weekly report, and show the hotspot, **AVG RESOLUTION**, and narrative.

## Privacy and limits

- Incident data and AI requests stay on the local machine.
- Anonymous reports store no name, device identifier, or GPS. Signing in as a student does not change this. Location is only stored when a student shares it through an SOS.
- Humans review alerts and make final operational decisions.
- CampusGuard is a prototype, not a replacement for emergency services. In immediate danger, call the appropriate campus or public emergency number.

After setup, CampusGuard runs fully offline: fonts are self-hosted, data lives in local SQLite, and Gemma runs through Ollama. Internet is only needed for installation, dependencies, the model download, and optional phone certificate setup.

## Architecture

```text
server/    FastAPI app, SQLite, Ollama services
web/       React/Vite app and CSS Modules
main.py    Root launcher for `uvicorn main:app`
seed.py    30 reports plus SOS hotspot seed data
```

| Component | Responsibility |
| --- | --- |
| React/Vite frontend | Student forms, SOS button, Dispatch, Insights UI |
| FastAPI | API routes and workflow |
| SQLite | Alerts, statuses, status history, insights |
| Fallback triage | Immediate result when AI is pending or unavailable |
| Ollama | Hosts and runs the model locally |
| Gemma | Report suggestions and weekly narrative |
| Security staff | Review recommendations and make final decisions |

The UI is a calm field dispatch board: warm paper background, hairline rules, Archivo for UI text, IBM Plex Mono for data, flat priority tags, no gradients, no emoji, no external font or CDN dependency.

## Contributing

Released under the [MIT License](./LICENSE). Gemma is open-weight software under [Google's Gemma terms](https://ai.google.dev/gemma/terms). See [CONTRIBUTING.md](./CONTRIBUTING.md) to get started.

Good first issues:

- Photo uploads for danger reports
- Campus map and incident location view
- SMS gateway behind explicit admin configuration and consent
- PWA offline queue for reports
- Swap Ollama for LM Studio or `llama.cpp`
- SOS spam protection and rate limiting
