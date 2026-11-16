
import json
import logging
import os
import re
import time
from typing import Any, TypedDict
from urllib.parse import urlparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from tavily import TavilyClient
from langgraph.graph import END, StateGraph

from prompts import SYSTEM_PROMPT


# =====================================================
# CONFIGURATION
# =====================================================

load_dotenv()

logger = logging.getLogger("globalpath")


class State(TypedDict):
    profile: dict
    research: list
    result: dict


# =====================================================
# PROFILE HELPER
# =====================================================

def _profile_dict(profile: Any) -> dict:

    if hasattr(profile, "model_dump"):
        return profile.model_dump()

    if isinstance(profile, dict):
        return profile

    raise TypeError(
        "Student profile must be a dictionary or Pydantic model."
    )


# =====================================================
# OFFICIAL SOURCE CHECK
# =====================================================

def _is_likely_official(url: str) -> bool:

    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return False

    return (
        host.endswith(".gc.ca")
        or host.endswith(".canada.ca")
        or host.endswith(".edu")
        or host.endswith(".ac.uk")
        or host in {
            "canada.ca",
            "educanada.ca",
            "www.educanada.ca",
            "statcan.gc.ca",
        }
    )


# =====================================================
# TAVILY WEB RESEARCH
# =====================================================

def search_official_sources(profile: dict) -> list:

    api_key = os.getenv("TAVILY_API_KEY", "").strip()

    if not api_key:
        logger.warning("TAVILY_API_KEY is missing.")
        return []

    country = str(profile.get("country", ""))
    degree = str(profile.get("degree", ""))
    field = str(profile.get("field", ""))

    queries = [
        (
            f"official university admissions {degree} {field} "
            f"international students {country} tuition scholarships"
        ),
        (
            f"official government international student visa "
            f"study permit proof of funds living costs {country}"
        ),
        (
            f"official university program page {field} {degree} "
            f"international tuition scholarships {country}"
        ),
    ]

    collected = []
    seen_urls = set()

    try:

        tavily = TavilyClient(api_key=api_key)

        for query in queries:

            try:

                response = tavily.search(
                    query=query,
                    max_results=5,
                    search_depth="advanced",
                    include_answer=False,
                )

                for item in response.get("results", []):

                    url = str(item.get("url", "")).strip()

                    if not url or url in seen_urls:
                        continue

                    seen_urls.add(url)

                    collected.append({
                        "title": item.get("title", ""),
                        "url": url,
                        "content": item.get("content", ""),
                        "source_type": (
                            "likely_official"
                            if _is_likely_official(url)
                            else "third_party_or_unverified"
                        ),
                    })

            except Exception:

                logger.exception(
                    "Tavily search failed: %s",
                    query,
                )

        logger.info(
            "Collected %s research results.",
            len(collected),
        )

    except Exception:

        logger.exception("Tavily initialization failed.")

    return collected


# =====================================================
# JSON EXTRACTION
# =====================================================

def _extract_json(raw: str) -> dict:

    text = (raw or "").strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    try:

        parsed = json.loads(text)

    except json.JSONDecodeError:

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end <= start:
            raise ValueError(
                "Gemini did not return a valid JSON object."
            )

        parsed = json.loads(
            text[start:end + 1]
        )

    if not isinstance(parsed, dict):
        raise ValueError(
            "Gemini response must be a JSON object."
        )

    return parsed


# =====================================================
# NORMALIZE GEMINI RESULT
# =====================================================

def _normalise_result(result: dict) -> dict:

    defaults = {
        "profile_summary": "",
        "suitability_analysis": "",
        "universities": [],
        "degree_recommendations": [],
        "scholarships": [],
        "activities": [],
        "cost_breakdown": [],
        "application_roadmap": [],
        "important_notes": [],
        "sources": [],
        "disclaimer": (
            "This plan is informational only. Confirm all "
            "program details, fees, deadlines, scholarships "
            "and immigration rules with official sources."
        ),
    }

    for key, default_value in defaults.items():

        if key not in result or result[key] is None:
            result[key] = default_value

    list_fields = [
        "universities",
        "degree_recommendations",
        "scholarships",
        "activities",
        "cost_breakdown",
        "application_roadmap",
        "important_notes",
        "sources",
    ]

    for key in list_fields:

        if not isinstance(result[key], list):
            result[key] = []

    for university in result["universities"]:

        if not isinstance(university, dict):
            continue

        university_defaults = {
            "name": "",
            "location": "",
            "program": "",
            "tuition_estimate": "",
            "scholarship_options": [],
            "fit_reason": "",
            "official_url": "",
        }

        for key, default_value in university_defaults.items():

            if key not in university or university[key] is None:
                university[key] = default_value

        if not isinstance(
            university["scholarship_options"],
            list
        ):
            university["scholarship_options"] = []

    for cost in result["cost_breakdown"]:

        if not isinstance(cost, dict):
            continue

        cost.setdefault("category", "")
        cost.setdefault("estimate", "")
        cost.setdefault("notes", "")

    return result


# =====================================================
# GEMINI RETRY FUNCTION
# =====================================================

def _generate_with_retry(client, model: str, prompt: str):

    max_attempts = 4

    for attempt in range(max_attempts):

        try:

            logger.info(
                "Gemini attempt %s/%s",
                attempt + 1,
                max_attempts,
            )

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=8192,
                    response_mime_type="application/json",
                ),
            )

            if not response or not response.text:

                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response

        except Exception as exc:

            error_text = str(exc).upper()

            retryable = any(
                marker in error_text
                for marker in (
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "INTERNAL",
                )
            )

            if not retryable or attempt == max_attempts - 1:
                raise

            wait_seconds = 5 * (2 ** attempt)

            logger.warning(
                "Gemini temporarily unavailable. "
                "Retrying in %s seconds.",
                wait_seconds,
            )

            time.sleep(wait_seconds)

    raise RuntimeError(
        "Gemini failed after all retry attempts."
    )


# =====================================================
# MAIN PLANNER NODE
# =====================================================

def planner_node(state: State):

    api_key = os.getenv("GOOGLE_API_KEY", "").strip()

    if not api_key:

        raise ValueError(
            "GOOGLE_API_KEY is missing. Add it to .env."
        )

    profile = _profile_dict(state["profile"])

    logger.info(
        "Starting study plan for %s",
        profile.get("country", "unknown"),
    )

    # Research
    research = search_official_sources(profile)

    # Gemini model
    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite",
    ).strip()

    if not model:
        model = "gemini-3.5-flash-lite"

    # Prompt
    prompt = f"""
{SYSTEM_PROMPT}

STUDENT PROFILE:

{json.dumps(profile, ensure_ascii=False, default=str)}

LIVE WEB RESEARCH:

{json.dumps(research, ensure_ascii=False, default=str)}

STRICT REQUIREMENTS:

- Preserve the exact student budget, currency and period.
- Never confuse annual budget with total degree budget.
- Never invent university names or program titles.
- Never invent tuition fees or application deadlines.
- Never invent scholarships or eligibility criteria.
- Use official university URLs where available.
- Do not use consultancy websites as official university sources.
- Use official government sources for immigration information.
- Never guess current visa or proof-of-funds figures.
- Clearly mark missing or unverified information.
- Return only valid JSON matching the required schema.
- Do not include Markdown fences.
"""

    client = None

    try:

        # Connect Gemini
        client = genai.Client(
            api_key=api_key
        )

        logger.info(
            "Using Gemini model: %s",
            model,
        )

        # Generate with retries
        response = _generate_with_retry(
            client=client,
            model=model,
            prompt=prompt,
        )

        # Parse JSON
        result = _extract_json(
            response.text
        )

        # Normalize response
        result = _normalise_result(
            result
        )

        logger.info(
            "Study plan generated successfully."
        )

        return {
            "research": research,
            "result": result,
        }

    except Exception as exc:

        logger.exception(
            "Study plan generation failed."
        )

        raise RuntimeError(
            f"Study plan generation failed: "
            f"{type(exc).__name__}: {exc}"
        ) from exc

    finally:

        if client is not None:

            try:
                client.close()

            except Exception:

                logger.debug(
                    "Gemini client close failed.",
                    exc_info=True,
                )


# =====================================================
# LANGGRAPH SETUP - SINGLE NODE
# =====================================================

def build_graph():

    workflow = StateGraph(State)

    workflow.add_node(
        "study_abroad_planner",
        planner_node,
    )

    workflow.set_entry_point(
        "study_abroad_planner"
    )

    workflow.add_edge(
        "study_abroad_planner",
        END,
    )

    return workflow.compile()


agent = build_graph()


# =====================================================
# FASTAPI FUNCTION
# =====================================================

def generate_study_plan(profile):

    response = agent.invoke({
        "profile": _profile_dict(profile),
        "research": [],
        "result": {},
    })

    return response["result"]
