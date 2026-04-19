from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("MODEL_NAME", "google/flan-t5-base")
DEFAULT_MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "384"))


class InferenceEngine:
    """Small wrapper around a Hugging Face pipeline with safe fallback behavior."""

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self.model_name = model_name
        self._generator = None
        self._load_error: Optional[str] = None

    def generate(self, prompt: str) -> str:
        generator = self._get_generator()
        if generator is None:
            logger.warning("Using fallback response because model could not load: %s", self._load_error)
            return self._fallback_response(prompt)

        try:
            result = generator(
                prompt,
                max_new_tokens=DEFAULT_MAX_NEW_TOKENS,
                do_sample=False,
                truncation=True,
            )
            if not result:
                return self._fallback_response(prompt)
            output = result[0].get("generated_text") or result[0].get("summary_text") or ""
            return output.strip() if output else self._fallback_response(prompt)
        except Exception as exc:  # pragma: no cover
            logger.exception("Generation failed: %s", exc)
            return self._fallback_response(prompt)

    def _get_generator(self):
        if self._generator is not None:
            return self._generator
        try:
            self._generator = _build_pipeline(self.model_name)
            return self._generator
        except Exception as exc:  # pragma: no cover
            self._load_error = str(exc)
            logger.exception("Failed to initialize generator: %s", exc)
            return None

    def _fallback_response(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if "active mode: interview" in prompt_lower:
            return (
                "## Interview Practice\n"
                "1. Tell me about yourself and why you are interested in this role.\n"
                "2. Describe a challenging project and how you handled it.\n"
                "3. What experience do you have with the tools or skills listed in the job description?\n"
                "4. Tell me about a time you resolved a conflict or blocker.\n"
                "5. Why should we hire you for this position?\n\n"
                "### STAR Prompt\n"
                "Pick one experience and answer with Situation, Task, Action, and Result.\n\n"
                "### Practice Tip\n"
                "Paste the job description for more tailored questions."
            )
        if "active mode: resume" in prompt_lower:
            return (
                "## Rewritten Bullets\n"
                "- Built and enhanced backend features using relevant technologies aligned with the target role.\n"
                "- Collaborated with cross-functional teams to deliver reliable solutions and improve system usability.\n"
                "- Supported cloud or deployment workflows and documented outcomes with clear business impact [add metric here].\n\n"
                "## Suggested Missing Details\n"
                "- Add scale, time saved, performance improvement, or user impact where possible.\n"
                "- Add specific tools, frameworks, or cloud services you actually used."
            )
        return (
            "## Job Application Checklist\n"
            "- [ ] Review the job description and highlight top requirements\n"
            "- [ ] Tailor resume bullets to match relevant skills\n"
            "- [ ] Prepare 5 STAR stories\n"
            "- [ ] Research the company and team\n"
            "- [ ] Practice answers for role-specific questions\n"
            "- [ ] Prepare questions to ask the interviewer\n"
            "- [ ] Test meeting link, audio, and camera if virtual\n"
        )


@lru_cache(maxsize=2)
def _build_pipeline(model_name: str):
    from transformers import pipeline

    return pipeline("text2text-generation", model=model_name)
