"""Festival research agent."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from concert_planner.config.settings import OPENAI_API_KEY
from concert_planner.models import FestivalResults
from concert_planner.models.state import ConcertPlannerState
from concert_planner.prompts.festival_prompts import (
    FESTIVAL_AGENT_SYSTEM_PROMPT,
)


def create_llm():
    """Create the language model used by the Festival Research Agent."""

    return ChatOpenAI(
        model="gpt-5-nano",
        api_key=OPENAI_API_KEY,
    )


def initialize_festival_agent():
    """Initialize the Festival Research Agent."""

    llm = create_llm()
    return create_festival_agent(llm)


def create_festival_agent(llm):
    """Create the Festival Research Agent with structured output."""

    return llm.with_structured_output(FestivalResults)


def research_festivals(state: ConcertPlannerState, festival_agent):
    """Research suitable music festivals based on the user's request."""

    result = festival_agent.invoke(
        [
            SystemMessage(content=FESTIVAL_AGENT_SYSTEM_PROMPT),
            HumanMessage(
                content=f"""
                Find suitable music festivals based on this request:

                {state["user_request"]}
                """
            ),
        ]
    )

    festivals = [festival.model_dump() for festival in result.festivals]

    return {"festivals": festivals}
