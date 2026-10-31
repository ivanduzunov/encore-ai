"""Flight research agent."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from concert_planner.config.settings import OPENAI_API_KEY
from concert_planner.models import FlightResults
from concert_planner.models.state import ConcertPlannerState
from concert_planner.prompts.flight_prompts import (
    TRAVEL_AGENT_SYSTEM_PROMPT,
)


def create_llm():
    """Create the language model used by the Flight Research Agent."""

    return ChatOpenAI(
        model="gpt-5-nano",
        api_key=OPENAI_API_KEY,
    )


def create_flight_agent(llm):
    """Create the Flight Research Agent with structured output."""

    return llm.with_structured_output(FlightResults)


def initialize_flight_agent():
    """Initialize the Flight Research Agent."""

    llm = create_llm()
    return create_flight_agent(llm)


def research_flights(
    state: ConcertPlannerState,
    flight_agent,
):
    """Research suitable flights for the selected music festival."""

    festival = state["selected_festival"]
    accommodation = state["selected_accommodation"]
    feedback = state.get("user_feedback")

    print("\n✈️ TRAVEL RESEARCH AGENT")

    human_prompt = f"""
    You are a travel research assistant.

    Find suitable flight options for a person
    travelling from Sofia, Bulgaria to the city
    where their selected music festival takes place.

    Festival:
    {festival}

    Selected accommodation:
    {accommodation}

    Consider:
    - destination city
    - festival dates
    - reasonable departure and arrival times
    - reasonable price
    - suitability for attending the festival
    """

    if feedback:
        human_prompt += f"""

    IMPORTANT USER FEEDBACK:

    {feedback}

    Revise the flight recommendations according
    to the user's feedback.

    Do not simply repeat the previous options.
    """

    result = flight_agent.invoke(
        [
            SystemMessage(content=TRAVEL_AGENT_SYSTEM_PROMPT),
            HumanMessage(content=human_prompt),
        ]
    )

    flights = [
        flight.model_dump()
        for flight in result.flights
    ]

    print(f"\n✈️ Found {len(flights)} flight options.")

    return {
        "flights": flights,
    }