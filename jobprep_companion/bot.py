from __future__ import annotations

import re

from jobprep_companion.inference import InferenceEngine
from jobprep_companion.prompts import HELP_TEXT, checklist_prompt, interview_prompt, resume_prompt
from jobprep_companion.state import ChatState


class JobPrepCompanion:
    def __init__(self) -> None:
        self.state = ChatState()
        self.engine = InferenceEngine()

    def handle_message(self, message: str) -> str:
        cleaned = (message or "").strip()
        if not cleaned:
            return "Please enter a message, or type `help` to see supported commands."

        lower = cleaned.lower()

        if lower == "help":
            return HELP_TEXT

        if lower == "reset":
            self.state.reset()
            return "Conversation state cleared. Please choose a mode: `mode: interview`, `mode: resume`, or `mode: checklist`."

        mode_match = re.fullmatch(r"mode\s*:\s*(interview|resume|checklist)", lower)
        if mode_match:
            mode = mode_match.group(1)
            self.state.set_mode(mode)
            return self._mode_confirmation(mode)

        if not self.state.current_mode:
            return (
                "Please choose a mode first.\n\n"
                "Examples:\n"
                "- `mode: interview`\n"
                "- `mode: resume`\n"
                "- `mode: checklist`\n\n"
                "You can also type `help` to see examples."
            )

        return self._run_mode(cleaned)

    def _run_mode(self, user_input: str) -> str:
        mode = self.state.current_mode
        if mode == "interview":
            if len(user_input) < 10:
                return "Please provide a role title, target company, or a job description so I can tailor the interview practice."
            return self.engine.generate(interview_prompt(user_input))

        if mode == "resume":
            if "job description" not in user_input.lower() and "resume" not in user_input.lower() and "bullet" not in user_input.lower():
                return (
                    "For resume mode, please paste both:\n"
                    "1. A job description or key requirements\n"
                    "2. Your current resume bullets"
                )
            return self.engine.generate(resume_prompt(user_input))

        if mode == "checklist":
            return self.engine.generate(checklist_prompt(user_input))

        return "Unknown mode. Type `reset` and select a mode again."

    @staticmethod
    def _mode_confirmation(mode: str) -> str:
        messages = {
            "interview": (
                "Interview mode is active. Paste a role title or job description, and I will generate interview questions, STAR prompts, or a mock interview."
            ),
            "resume": (
                "Resume mode is active. Paste the job description and your current resume bullets, and I will rewrite them without inventing details."
            ),
            "checklist": (
                "Checklist mode is active. Ask for an application checklist, interview-prep checklist, or a short prep plan."
            ),
        }
        return messages[mode]
