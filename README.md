# AI-Project-Health-Reporting
=======
# AI Project Health Reporting Agent

An enterprise-grade AI Project Health Reporting Agent that automates project health reporting from Excel project plans. This repository contains the complete deliverables for the Professional Services AI assessment.

## Deliverables Included

1. **One-page RAG methodology:** See `RAG_METHODOLOGY.md`
2. **Working AI Agent:** Instructions below. Reads project plans, calculates RAG, and provides AI reasoning.
3. **Sample Weekly Outputs:** See `SAMPLE_OUTPUTS.md`
4. **Final Monthly Presentation:** Handled dynamically via the "Export PPT" button in the UI.
5. **Design Decisions & Architecture:** See the section below.

---

## Advanced Features Implemented

- **🤖 AI Recovery Action Plan:** For any project rated RED or AMBER, a button appears to dynamically generate a 3-step, 30-day tactical recovery plan via the AI engine, presented in a beautifully styled modal.
- **📊 Executive Dashboard Visualizations:** Features a dynamic "RAG Status Distribution" Pie Chart and "Portfolio Completion Status" Bar Chart to instantly visualize portfolio health.
- **⚡ Seamless Workflow:** Includes a quick "Start Over" button to easily reset the dashboard and analyze new project plans without ever refreshing the page.

---

## Design Decisions & Architecture

**1. Tech Stack Selection:**
- **Backend:** Python + FastAPI. Selected for its native asynchronous capabilities, speed, and seamless integration with AI libraries (LangChain).
- **Frontend:** React + Vite. Selected for rapid development and dynamic UI updates. Recharts is used for data visualization.
- **AI Integration:** LangChain with OpenRouter (`google/gemini-2.5-flash`). LangChain allows for structured prompting and easy model swapping. The Gemini flash model was chosen for its massive context window and cost-effectiveness.

**2. Handling Incomplete Data Gracefully:**
- The Excel parser uses a naive but highly resilient scanning method. Instead of requiring rigid, predefined templates, it scans sheet names for keywords like "task", "milestone", or "risk" and dynamically searches for standard columns ("Status", "Severity").
- If data is missing (e.g., 0% completion), the backend explicitly handles the edge case, penalizing the score rather than throwing division-by-zero errors.

**3. AI Persona & Prompt Engineering:**
- The AI is prompted to act as a "Senior PMO Director". This persona forces the AI to focus on executive-level insights rather than just regurgitating data.
- The AI doesn't calculate the RAG score itself—it receives the mathematically calculated RAG score as an input constraint and is asked to *justify* it based on the metrics. This prevents hallucinated math while maintaining rich qualitative insights.

---

## Setup & Run Instructions

### 1. Backend Setup
Navigate to the `backend` directory, activate the virtual environment, and install dependencies:
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

**Configuration:**
The API key is pre-configured in `backend/app/core/config.py` as `OPENROUTER_API_KEY`. If you wish to change the key or model, update the settings inside `config.py` or `ai_engine.py`.

**Run Backend:**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
Navigate to the `frontend` directory in a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open the provided `localhost` URL in your browser to access the beautiful glassmorphism dashboard.

---

## Weekly Schedule Bonus

To run the agent on a weekly schedule, the backend provides a `/api/v1/weekly-report` endpoint. You can set up a simple cron job on a Linux server to trigger this every Friday at 5 PM:
```bash
0 17 * * 5 curl -X POST http://localhost:8000/api/v1/weekly-report
```

