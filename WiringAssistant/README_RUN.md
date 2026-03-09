# WiringAssistant (fixed demo)

## Backend
```bash
cd WiringAssistant/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Frontend
```bash
cd WiringAssistant/frontend
npm install
npm run dev -- --port 5173
```

Open http://localhost:5173 and click **Auto-detect** then **Optimize wiring**.
