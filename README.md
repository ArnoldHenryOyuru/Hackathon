# CampusGuard

> Tap for help. Report for prevention. Stay safe.

CampusGuard is a local campus safety dispatch board. Students can send an immediate SOS or report a danger; security officers can triage and update incidents; administrators can generate weekly prevention insights. It uses FastAPI, SQLite, React/Vite, and local Gemma through Ollama. No login, external AI APIs, websockets, maps, or push services are included.

## Project structure

```text
server/                 FastAPI app, SQLite, Ollama services
web/                    React/Vite app and CSS Modules
main.py                 compatible root launcher for uvicorn main:app
seed.py                 30 reports plus SOS hotspot seed data
```

## Run locally

Open two terminals from the project root.

### Backend

```powershell
pip install -r requirements.txt
ollama pull gemma3:1b
python seed.py
uvicorn main:app --host 0.0.0.0
```

Ollama is optional for the prototype. If it is unavailable, report triage and weekly narrative generation use explicit local fallbacks. All incident data and AI requests remain on the local machine.

### Frontend

```powershell
cd web
npm install
npm run dev
```

Open <http://localhost:5173/>. Vite proxies `/api` to the FastAPI server at `http://127.0.0.1:8000`.

For a production frontend check:

```powershell
npm run build
```

## Routes

- `/` — mobile-first student app with SOS and danger reporting
- `/dashboard` — security dispatch ledger, SOS banner, polling, and status controls
- `/insights` — SQL statistics, SVG charts, and Gemma prevention narrative

## API

- `POST /api/sos`
- `POST /api/reports`
- `GET /api/alerts`
- `PATCH /api/alerts/{id}/status`
- `POST /api/insights/generate`
- `GET /api/insights/latest`

Reports are saved immediately with fallback triage; the Gemma call runs afterward and updates the saved report when successful. Anonymous reports contain no student identifier. SOS never waits for AI.

## Three-minute demo

1. Open `/` and tap the red **SOS** control. If GPS is denied, the alert still sends. Open `/dashboard` and show the red SOS band at the top.
2. Return to `/`, choose **Report a danger**, select `suspicious person`, select **Hostel Gate**, add a short description, and submit. Show the confirmation and the Gemma or fallback priority/summary.
3. On `/dashboard`, mark the report **Investigating**. The status change is stored in `status_log`.
4. Open `/insights`, click **Generate this week's report**, and show the Parking Lot B hotspot plus the weekly summary.

## Design

The UI is a calm field dispatch board: warm paper background, hairline rules, Archivo for UI text, IBM Plex Mono for data, flat priority tags, no decorative gradients, no emoji, and no external font/CDN dependency.
