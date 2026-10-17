# Contributing to CampusGuard

## Development setup

1. Install Python 3.10 or newer, Node.js 18 or newer, and the project dependencies.
2. Follow the local setup instructions in [README.md](./README.md).
3. Run the backend and frontend locally before making changes.

## Before opening a pull request

- Run `python -m compileall -q server main.py`.
- Run `npm run build` from `web`.
- Update the README when user-visible behavior or setup changes.
- Keep anonymous-report privacy guarantees intact.
- Do not send incident data to external AI services.

## Pull requests

Describe the user-facing change, security or privacy impact, and validation commands
in the pull request description. Keep changes focused and include screenshots for
visual changes when practical.
