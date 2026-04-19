from __future__ import annotations

import gradio as gr

from jobprep_companion.bot import JobPrepCompanion


bot = JobPrepCompanion()


def chat(message: str, history: list[dict]) -> str:
    return bot.handle_message(message)


DESCRIPTION = """
# JobPrep Companion

A lightweight LLM-based chatbot for:
- Interview preparation
- Resume bullet rewriting
- Job application and interview checklists

## Commands
- `help`
- `reset`
- `mode: interview`
- `mode: resume`
- `mode: checklist`

## Tips
- Pick a mode first.
- In interview mode, provide a role title or job description.
- In resume mode, paste a job description and your bullets.
- In checklist mode, ask for an application or interview-prep checklist.
"""


with gr.Blocks(title="JobPrep Companion") as demo:
    gr.Markdown(DESCRIPTION)
    gr.ChatInterface(
        fn=chat,
        type="messages",
        chatbot=gr.Chatbot(height=500, type="messages"),
        textbox=gr.Textbox(
            placeholder="Type help or select a mode, for example: mode: interview",
            lines=4,
        ),
        examples=[
            "help",
            "mode: interview",
            "I am preparing for a Java backend developer interview. Generate 5 interview questions and STAR prompts.",
            "mode: resume",
            "Job description: Looking for a Java Spring Boot developer with AWS and Kafka experience.\nResume bullets:\n- Developed APIs for internal tools\n- Worked with cloud services",
            "mode: checklist",
            "Create an interview preparation checklist for a software engineer role with a 3-day prep plan.",
            "reset",
        ],
        cache_examples=False,
    )


if __name__ == "__main__":
    demo.launch()
