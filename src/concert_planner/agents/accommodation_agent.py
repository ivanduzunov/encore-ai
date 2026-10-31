"""Accommodation research agent."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from concert_planner.config.settings import OPENAI_API_KEY
from concert_planner.models import AccommodationResults
from concert_planner.models.state import ConcertPlannerState
from concert_planner.prompts.accommodation_prompts import (
    ACCOMMODATION_AGENT_SYSTEM_PROMPT,
)


def create_llm():
    """Create the language model used by the Accommodation Research Agent."""

    return ChatOpenAI(
        model="gpt-5-nano",
        api_key=OPENAI_API_KEY,
    )


def create_accommodation_agent(llm):
    """Create the Accommodation Research Agent with structured output."""

    return llm.with_structured_output(AccommodationResults)


def initialize_accommodation_agent():
    """Initialize the Accommodation Research Agent."""

    llm = create_llm()
    return create_accommodation_agent(llm)


def find_accommodation(
    state: ConcertPlannerState,
    accommodation_agent,
):
    """Find suitable accommodation for the selected music festival."""

    festival = state["selected_festival"]
    accommodation_type = state["accommodation_type"]

    if accommodation_type == "camping":
        camping = {
            "name": f"{festival['name']} Official Camping",
            "type": "camping",
            "city": festival["city"],
            "price": 0,
            "description": "Official festival camping.",
        }

        print(f"\n🏕️ Automatically selected: {camping['name']}")

        return {
            "accommodations": [camping],
            "selected_accommodation": camping,
        }

    result = accommodation_agent.invoke(
        [
            SystemMessage(content=ACCOMMODATION_AGENT_SYSTEM_PROMPT),
            HumanMessage(
                content=f"""
                Find suitable hotel accommodation for the
                selected music festival.

                Festival:
                {festival}

                Accommodation type:
                {accommodation_type}

                Find several suitable options.

                Consider:
                - proximity to the festival
                - price
                - location
                - value for money
                - festival dates
                """
            ),
        ]
    )

    accommodations = [accommodation.model_dump() for accommodation in result.accommodations]

    print(f"\n🏨 Found {len(accommodations)} hotels near {festival['city']}")

    return {"accommodations": accommodations}
