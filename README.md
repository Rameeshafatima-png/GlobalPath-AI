# GlobalPath AI
### Your AI-Powered Study Abroad Planner

<p align="center">
  An intelligent study-abroad planning assistant that helps students explore universities, scholarships, estimated costs, and application pathways through AI-powered research.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/LangGraph-AI%20Workflow-1C3C3C?style=for-the-badge" alt="LangGraph">
  <img src="https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini">
  <img src="https://img.shields.io/badge/Tavily-Web%20Research-6C47FF?style=for-the-badge" alt="Tavily">
</p>

---

## Overview

**GlobalPath AI** is an AI-powered study-abroad planning application designed to simplify the process of exploring international education opportunities.

Choosing a university abroad involves researching admission requirements, tuition fees, scholarships, living expenses, and application deadlines. GlobalPath AI brings these planning activities together in one intelligent application.

By combining **LangGraph, Google Gemini, Tavily Search, and FastAPI**, the application generates personalized study-abroad plans based on a student's academic profile, preferred destination, field of study, and budget.

## Key Features

- **Personalized Study Plans:** Generates study-abroad recommendations based on student preferences and academic profiles.
- **University Recommendations:** Researches relevant universities and programs.
- **Scholarship Discovery:** Identifies potential scholarship opportunities.
- **Cost Estimation:** Organizes estimated tuition, accommodation, living, travel, visa, and other expenses where information is available.
- **AI-Powered Research:** Uses Tavily to gather relevant web research.
- **Intelligent Planning:** Uses Google Gemini to analyze research and generate structured recommendations.
- **Application Roadmap:** Provides a step-by-step application preparation plan.
- **Source-Aware Responses:** Includes research sources to help students verify important information.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| FastAPI | Backend and API framework |
| LangGraph | AI workflow orchestration |
| Google Gemini | AI reasoning and plan generation |
| Tavily Search | Web research and information retrieval |
| HTML5 | Frontend structure |
| CSS3 | User interface styling |
| JavaScript | Frontend interactions |
| Uvicorn | ASGI server |

## How It Works

GlobalPath AI follows a simple AI-powered workflow:

1. **Student Profile:** The student provides academic details, preferred country, study level, field, and budget.
2. **Web Research:** Tavily searches for relevant university, scholarship, and study-abroad information.
3. **AI Analysis:** Google Gemini analyzes the student profile and gathered research.
4. **Plan Generation:** LangGraph manages the planning workflow and produces structured recommendations.
5. **Results:** The application presents a personalized study-abroad plan with universities, scholarships, estimated costs, and an application roadmap.

## Project Architecture

```text
GlobalPath-AI/
│
├── app.py
├── study_agent.py
├── prompts.py
├── schemas.py
├── requirements.txt
├── .env
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md
```

### Core Components

| File | Responsibility |
|---|---|
| `app.py` | FastAPI application and backend routes |
| `study_agent.py` | LangGraph workflow, Tavily research, and Gemini integration |
| `prompts.py` | AI system instructions and response structure |
| `schemas.py` | Data models and request/response structure |
| `templates/index.html` | Main application interface |
| `static/style.css` | Frontend styling |
| `static/script.js` | Frontend functionality |
| `requirements.txt` | Python dependencies |

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Rameeshafatima-png/GlobalPath-AI.git
```

### 2. Navigate to the Project

```bash
cd GlobalPath-AI
```

### 3. Create a Virtual Environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace the placeholder values with your own API credentials.

**API Providers:**
- Google AI Studio: https://aistudio.google.com/
- Tavily: https://tavily.com/

**Security:** Never upload your `.env` file or expose API keys in public repositories.

### 6. Run the Application

```bash
uvicorn app:app --reload
```

Open your browser and visit:

```text
http://127.0.0.1:8000
```

## Example Use Case

A student wants to pursue a Bachelor's degree in Computer Science in Canada.

The student provides:
- Preferred destination: Canada
- Study level: Bachelor's
- Field of interest: Computer Science
- Annual budget: Student-defined budget
- Academic background: Student-provided qualifications

GlobalPath AI researches relevant
