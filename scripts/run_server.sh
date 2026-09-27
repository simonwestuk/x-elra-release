
#!/usr/bin/env bash
# Development: uvicorn xelra.server.app:app --host 0.0.0.0 --port 8000 --reload
# Production:  remove --reload, add --workers
uvicorn xelra.server.app:app --host 0.0.0.0 --port "${PORT:-8000}" --workers "${WORKERS:-4}"
