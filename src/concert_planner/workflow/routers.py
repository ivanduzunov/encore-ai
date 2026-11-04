"""Conditional routers for the Concert Planner workflow."""


def accommodation_router(state):
    """Determine whether to select accommodation or continue to travel research."""

    if state["selected_accommodation"] is not None:
        return "travel"

    return "select"


def flight_review_router(state):
    """Determine whether to continue or revise flight research."""

    if state["selected_flight"] is not None:
        return "continue"

    return "revise"