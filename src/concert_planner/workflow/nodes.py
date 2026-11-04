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
from concert_planner.tools.calculate_total_price import calculate_total_price
from concert_planner.tools.generate_final_summary import generate_final_summary


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

def select_accommodation_type_node(state):
    """Pause the workflow and let the user select accommodation type."""

    options = ["hotel", "camping"]

    selection = interrupt(
        {
            "type": "accommodation_type",
            "message": "Where would you like to stay?",
            "options": options,
        }
    )

    return {
        "accommodation_type": options[selection],
    }

def select_accommodation_node(state):
    """Pause the workflow and let the user select accommodation."""

    accommodations = state["accommodations"]

    selection = interrupt(
        {
            "type": "accommodation_selection",
            "message": "Choose accommodation",
            "options": accommodations,
        }
    )

    selected = accommodations[selection]
    print(f"\n🏨 Selected: {selected['name']}")

    return {
        "selected_accommodation": selected,
    }

def review_flight_node(state):
    """Pause the workflow and let the user review flight options."""

    response = interrupt(
        {
            "type": "flight_review",
            "message": (
                "Review the flight options. "
                "You can select a flight or request a revision."
            ),
            "options": state["flights"],
        }
    )

    if response["action"] == "select":
        selection = response["selection"]
        return {
            "selected_flight": state["flights"][selection],
            "user_feedback": None,
        }

    if response["action"] == "revise":
        return {
            "selected_flight": None,
            "user_feedback": response["feedback"],
        }

def confirm_purchase_node(state):
    """Pause the workflow and ask the user to confirm the purchase."""

    festival = state["selected_festival"]
    accommodation = state["selected_accommodation"]
    flight = state["selected_flight"]

    total_price = (
        festival["price"]
        + accommodation["price"]
        + flight["price"]
    )

    approval = interrupt(
        {
            "type": "purchase_confirmation",
            "message": "Please review your trip before purchase.",
            "festival": festival,
            "accommodation": accommodation,
            "flight": flight,
            "total_price": total_price,
        }
    )

    return {
        "purchase_approved": approval,
    }

def buy_tickets_node(state):
    """Finalize the trip purchase and generate the final summary."""

    if not state["purchase_approved"]:
        return {
            "final_result": "Purchase cancelled by user.",
        }

    total_price = calculate_total_price.invoke(
        {
            "festival": state["selected_festival"],
            "accommodation": state["selected_accommodation"],
            "flight": state["selected_flight"],
        }
    )

    final_summary = generate_final_summary.invoke(
        {
            "festival": state["selected_festival"],
            "accommodation": state["selected_accommodation"],
            "flight": state["selected_flight"],
            "total_price": total_price,
        }
    )

    return {
        "final_result": final_summary,
        "total_price": total_price,
    }