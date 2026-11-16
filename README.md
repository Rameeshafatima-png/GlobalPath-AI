# GlobalPath AI — Single-Folder Study Abroad Planner

A full-stack study-abroad planning application powered by one LangGraph AI agent. Enter a destination country, degree, budget and field to receive a personalized plan with university options, scholarships, activities, estimated costs and an application roadmap.

## Architecture

**Single agent, single task.** One LangGraph node (`study_abroad_planner`) performs the study-abroad planning task. FastAPI serves both the API and the HTML/CSS/JavaScript website. No separate frontend server is needed.

## Structure

```text
GlobalPath_AI/
├── app.py
├── schemas.py
├── study_agent.py
├── prompts.py
├── requirements.txt
├── .env.example
├── README.md
├── templates/index.html
└── static/
    ├── style.css
    └── script.js
```

## Setup (Windows PowerShell)

Run these commands from this folder:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your keys to `.env`:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
TAVILY_API_KEY=your_tavily_api_key
```

Start the complete application with one command:

```powershell
uvicorn app:app --reload
```

Open **http://127.0.0.1:8000**. API docs: http://127.0.0.1:8000/docs

## API

`POST /api/study-plan`

Example JSON:

```json
{
  "country": "Germany",
  "degree": "Master's",
  "budget": 15000,
  "currency": "EUR",
  "budget_type": "annual",
  "field": "Artificial Intelligence",
  "academic_score": "82%",
  "english_test": "IELTS 6.5",
  "intake": "Winter 2027"
}
```

## Environment variables

- `GOOGLE_API_KEY` — required for Gemini.
- `GEMINI_MODEL` — optional; defaults to `gemini-2.5-flash`.
- `TAVILY_API_KEY` — optional, recommended for live web research.

Without Tavily, the model can still draft a plan, but it cannot perform live research. Verify fees, scholarships, deadlines, admission requirements and visa rules on official university and government websites. Costs are estimates and may change. No admission, scholarship or visa outcome is guaranteed.

## License

MIT
