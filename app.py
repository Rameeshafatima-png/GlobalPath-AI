
import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool

from schemas import StudentProfile

BASE = Path(__file__).resolve().parent

# Load environment variables before using the agent.
load_dotenv(BASE / ".env", override=True)

from study_agent import generate_study_plan

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("globalpath")

app = FastAPI(
    title="GlobalPath AI",
    description="AI-powered Study Abroad Planning Assistant",
    version="2.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE / "templates"
)


@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "application": "GlobalPath AI"
    }


@app.post("/api/study-plan")
async def create_plan(profile: StudentProfile):

    try:

        logger.info(
            "New study plan request: country=%s, degree=%s, field=%s",
            profile.country,
            profile.degree,
            profile.field
        )

        result = await run_in_threadpool(
            generate_study_plan,
            profile
        )

        return result

    except ValueError as exc:

        logger.warning("Validation/configuration error: %s", exc)

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        logger.exception("Study plan generation failed.")

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
