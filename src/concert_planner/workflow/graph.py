"""LangGraph workflow definition for the Concert Planner."""

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from concert_planner.models.state import ConcertPlannerState
from concert_planner.workflow.nodes import (
    accommodation_research_node,
    buy_tickets_node,
    confirm_purchase_node,
    festival_research_node,
    flight_research_node,
    review_flight_node,
    select_accommodation_node,
    select_accommodation_type_node,
    select_festival_node,
)
from concert_planner.workflow.routers import (
    accommodation_router,
    flight_review_router,
)


def build_graph():
    """Build and compile the Concert Planner workflow."""

    workflow = StateGraph(ConcertPlannerState)

    workflow.add_node("festival_research", festival_research_node)
    workflow.add_node("select_festival", select_festival_node)
    workflow.add_node(
        "select_accommodation_type",
        select_accommodation_type_node,
    )
    workflow.add_node("accommodation_research", accommodation_research_node)
    workflow.add_node("select_accommodation", select_accommodation_node)
    workflow.add_node("flight_research", flight_research_node)
    workflow.add_node("review_flight", review_flight_node)
    workflow.add_node("confirm_purchase", confirm_purchase_node)
    workflow.add_node("buy_tickets", buy_tickets_node)

        # Main workflow
    workflow.add_edge(START, "festival_research")
    workflow.add_edge("festival_research", "select_festival")
    workflow.add_edge("select_festival", "select_accommodation_type")
    workflow.add_edge(
        "select_accommodation_type",
        "accommodation_research",
    )

    # Accommodation routing
    workflow.add_conditional_edges(
        "accommodation_research",
        accommodation_router,
        {
            "select": "select_accommodation",
            "travel": "flight_research",
        },
    )

    workflow.add_edge("select_accommodation", "flight_research")

    # Flight routing
    workflow.add_edge("flight_research", "review_flight")
    workflow.add_conditional_edges(
        "review_flight",
        flight_review_router,
        {
            "continue": "confirm_purchase",
            "revise": "flight_research",
        },
    )

    # Purchase
    workflow.add_edge("confirm_purchase", "buy_tickets")
    workflow.add_edge("buy_tickets", END)

    checkpointer = InMemorySaver()

    return workflow.compile(
        checkpointer=checkpointer,
        debug=True,
    )