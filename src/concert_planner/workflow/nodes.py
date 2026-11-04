"""Workflow nodes for the Concert Planner."""

from langgraph.types import interrupt

from concert_planner.agents.accommodation_agent import (
    find_accommodation,
    initialize_accommodation_agent,
)
from concert_planner.agents.festival_agent import (
    initialize_festival_agent,
    research_festivals,
)
from concert_planner.agents.flight_agent import (
    initialize_flight_agent,
    research_flights,
)


def festival_research_node(state):
    """Research music festivals based on the user's request."""

    festival_agent = initialize_festival_agent()

    return research_festivals(
        state,
        festival_agent,
    )


def accommodation_research_node(state):
    """Find suitable accommodation for the selected festival."""

    accommodation_agent = initialize_accommodation_agent()

    return find_accommodation(
        state,
        accommodation_agent,
    )


def flight_research_node(state):
    """Research suitable flights for the selected festival."""

    flight_agent = initialize_flight_agent()

    return research_flights(
        state,
        flight_agent,
    )

def select_festival_node(state):
    """Pause the workflow and let the user select a festival."""

    festivals = state["festivals"]

    selection = interrupt(
        {
            "type": "festival_selection",
            "message": "Choose a festival:",
            "options": festivals,
        }
    )

    return {
        "selected_festival": festivals[selection],
    }
