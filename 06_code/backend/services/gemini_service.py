"""Google Gemini service used by the LearnSphere Study Coach."""
from __future__ import annotations

import logging
import os
import re
import time
from typing import Any

try:
    from google import genai
    from google.genai import types
except ModuleNotFoundError:  # Allows the rest of the Flask app to start without the optional client installed.
    genai = None
    types = None


SYSTEM_PROMPT = """You are LearnSphere AI, a Study Assistant designed to help students learn, understand concepts, solve academic problems, prepare for exams, complete programming exercises, and revise subjects.

You can answer study-related questions from ANY academic subject or field. Do not use a predefined subject list and do not restrict your answers to subjects explicitly mentioned in this prompt.

When a student asks an academic question, identify the subject, topic, intent, and required answer style automatically and provide the most useful answer.

For exam questions, provide accurate, clear, exam-friendly answers.

For theory questions, provide definitions, explanations, key points, examples, advantages/disadvantages, comparisons, and other relevant information as appropriate.

For programming questions, provide correct working code and explain the logic.

For numerical questions, solve the problem step by step.

For MCQs, identify the correct answer and explain it briefly.

For short-answer requests, keep the answer concise.

For detailed-answer requests, provide a detailed explanation.

For follow-up questions, use the conversation history to understand the student's meaning.

If the student asks about an academic subject that is not explicitly mentioned in this prompt, still answer the question. Never reject an academic question simply because the subject is not predefined.

Use simple, student-friendly language and adapt the explanation to the student's level.

Prioritize correctness and clarity. Do not fabricate facts.

The primary purpose of LearnSphere AI is academic learning, education, assignments, programming practice, and exam preparation.

For cybersecurity requests, support legitimate education, defence, and safe lab practice; do not provide harmful or unauthorized instructions, and offer a safe alternative instead."""

MAX_HISTORY_MESSAGES = 20
MAX_MESSAGE_LENGTH = 6000
DEFAULT_MODEL = "gemini-flash-latest"
MAX_RETRY_ATTEMPTS = 2
MODEL_NAME_PATTERN = re.compile(r"^gemini-[a-z0-9][a-z0-9._-]*$", re.IGNORECASE)
logger = logging.getLogger(__name__)


class GeminiServiceError(ValueError):
    """A safe, user-facing Gemini service failure.

    Attributes:
        retryable: whether the client may retry the request (transient errors)
        error_code: optional short provider-neutral error code
    """
    def __init__(self, message: str, *, retryable: bool = False, error_code: str | None = None):
        super().__init__(message)
        self.retryable = bool(retryable)
        self.error_code = error_code


def _history_limit() -> int:
    try:
        return max(0, min(int(os.getenv("STUDY_COACH_HISTORY_LIMIT", str(MAX_HISTORY_MESSAGES))), 50))
    except ValueError:
        return MAX_HISTORY_MESSAGES


def _clean_history(history: list[dict[str, Any]]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for item in history[-_history_limit():]:
        role = str(item.get("role", ""))
        content = str(item.get("content", "")).strip()
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": content[:MAX_MESSAGE_LENGTH]})
    return messages


def _conversation_prompt(history: list[dict[str, str]], user_message: str) -> str:
    transcript = []
    for item in history:
        speaker = "Student" if item["role"] == "user" else "Study Coach"
        transcript.append(f"{speaker}: {item['content']}")
    transcript.append(f"Student: {user_message}")
    transcript.append("Study Coach:")
    return "\n\n".join(transcript)


def _validated_model_name() -> str:
    """Return a syntactically valid Gemini model ID without making a second API call."""
    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    if not MODEL_NAME_PATTERN.fullmatch(model):
        raise GeminiServiceError(
            "GEMINI_MODEL must be a valid Gemini model ID, for example gemini-flash-latest."
        )
    return model


def _error_message(error: Exception) -> str:
    code = getattr(error, "code", None)
    status = str(code).upper()
    if code in {401, 403} or "UNAUTHENTICATED" in status or "PERMISSION_DENIED" in status:
        return "Gemini authentication failed. Check GEMINI_API_KEY in the server environment."
    if "RESOURCE_EXHAUSTED" in status:
        return "Study Coach: Gemini's project quota is exhausted. Wait for the quota reset or update quota/billing in Google AI Studio."
    if code == 429:
        return "Gemini is currently busy or its free-tier limit was reached. Please try again shortly."
    if code in {408, 500, 502, 503, 504} or "UNAVAILABLE" in status or "DEADLINE" in status:
        return "Gemini is temporarily unavailable. Please try again later."
    return "Gemini could not complete this request. Please try again."


def _is_transient_error(error: Exception) -> bool:
    """Return whether a provider error is safe to retry with backoff."""
    code = getattr(error, "code", None)
    status = str(code).upper()
    error_type = type(error).__name__.upper()
    details = f"{status} {error_type} {error}".upper()
    # RESOURCE_EXHAUSTED indicates a quota/billing exhaustion — do not retry.
    if "RESOURCE_EXHAUSTED" in details:
        return False
    return (
        code in {408, 429, 500, 502, 503, 504}
        or any(
            marker in details
            for marker in (
                "DEADLINE_EXCEEDED",
                "SERVICE_UNAVAILABLE",
                "UNAVAILABLE",
                "TIMEOUT",
                "CONNECTION",
                "NETWORK",
            )
        )
    )


def generate_chat_response(history: list[dict[str, Any]], user_message: str) -> str:
    """Generate a validated Study Coach reply without exposing provider internals."""
    message = str(user_message or "").strip()
    if not message:
        raise GeminiServiceError("Write a question for your study coach")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise GeminiServiceError("Your question must be 6,000 characters or fewer")

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_key_here":
        raise GeminiServiceError("Gemini is not configured. Set GEMINI_API_KEY in backend/.env.")
    if genai is None or types is None:
        raise GeminiServiceError("Gemini support is not installed. Run python -m pip install -r requirements.txt.")

    model = _validated_model_name()
    prompt = _conversation_prompt(_clean_history(history), message)
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.7,
        max_output_tokens=900,
    )

    for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
        try:
            logger.debug(
                "Gemini request starting: model=%s history_messages=%s message_characters=%s attempt=%s/%s",
                model,
                len(_clean_history(history)),
                len(message),
                attempt,
                MAX_RETRY_ATTEMPTS,
            )
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
            text = (getattr(response, "text", None) or "").strip()
            if not text:
                raise GeminiServiceError("Gemini did not return a text response. Please rephrase your question.")
            return text
        except GeminiServiceError:
            raise
        except Exception as error:
            logger.exception(
                "Gemini API request failed | exception_type=%s | exception_message=%s | exception_repr=%r",
                type(error).__name__,
                str(error),
                error,
            )
            # Log only header names. Provider header values can contain identifiers.
            try:
                headers = getattr(error, "headers", None) or getattr(getattr(error, "response", None), "headers", None)
                if headers:
                    logger.debug("Provider header names: %s", list(dict(headers).keys()))
            except Exception:
                pass

            # If details indicate quota exhausted, prefer a clear error code and do not retry.
            details = f"{getattr(error, 'code', '')} {type(error).__name__} {error}".upper()
            is_resource_exhausted = "RESOURCE_EXHAUSTED" in details
            error_code = "RESOURCE_EXHAUSTED" if is_resource_exhausted else None
            # Transient decision: do not retry RESOURCE_EXHAUSTED even if it's a 429.
            retryable = _is_transient_error(error) and attempt < MAX_RETRY_ATTEMPTS
            if not _is_transient_error(error) or attempt == MAX_RETRY_ATTEMPTS:
                raise GeminiServiceError(_error_message(error), retryable=retryable, error_code=error_code) from error

            delay_seconds = 2 ** (attempt - 1)
            logger.warning(
                "Retrying transient Gemini API error in %s second(s): attempt=%s/%s",
                delay_seconds,
                attempt + 1,
                MAX_RETRY_ATTEMPTS,
            )
            time.sleep(delay_seconds)

    raise GeminiServiceError("Gemini could not complete this request. Please try again.")
