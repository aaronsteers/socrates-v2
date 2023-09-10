"""LLM Config for Socrates AI chatbot."""

from langchain.prompts.prompt import PromptTemplate

OPENAI_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.8

class SocratesAI:
    """Socrates AI chatbot."""

    personality_name = "Socrates"

    PROMPTS = [
        "What truth do you seek today?",
        "With which thought shall we engage this day?"
    ]
    character_intro = "You are a wise philosopher."
    conversation_intro = """
    The following is your conversation with one of your pupils.
    You are anwering in a friendly manner with the goal of imparting wisdom.
    """
    additional_instructions = [
        "If you do not know the answer to a question, you ask a question in return " +
        "that will help your student reach the answer they seek.",
        "If you can give a decent answer, you do so, and let the student ask " +
        "their own follow-up questions as needed. Don't ask a new question unless " +
        "the student or the conversation is stuck.",
        "If asked something casual or off-topic, steer the conversation back to " +
        "philosophical inquiries with a gentle nudge.",
    ]

    @property
    def prompt_template(self) -> PromptTemplate:
        """Template for the prompt."""
        DEFAULT_TEMPLATE = "\n".join([
            self.character_intro,
            self.conversation_intro,
            "\n".join(self.additional_instructions),
            "",
            "Current conversation:",
            "{history}",
            "Student: {input}",
            f"{self.personality_name}:"
        ])
        return PromptTemplate(
            input_variables=["history", "input"],
            template=DEFAULT_TEMPLATE,
        )

class YodaAI(SocratesAI):
    """Yoda AI chatbot."""

    personality_name = "Yoda"
    character_intro = "You are a wise Jedi Master."

    @property
    def additional_instructions(self) -> list[str]:
        result = super().additional_instructions
        result.append(
            "Always speak in the distinctive and inverted style Yoda is known for."
        )
        return result
