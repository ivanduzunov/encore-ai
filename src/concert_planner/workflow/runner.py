"""Workflow execution runner for the Concert Planner."""

import uuid

from langgraph.types import Command

from concert_planner.workflow.graph import build_graph

graph = build_graph()

def create_initial_state(user_request: str) -> dict:
    """Create the initial state for a new workflow execution."""

    return {
        "user_request": user_request,
        "festivals": [],
        "selected_festival": None,
        "accommodation_type": None,
        "accommodations": [],
        "selected_accommodation": None,
        "flights": [],
        "selected_flight": None,
        "user_feedback": None,
        "total_price": None,
        "purchase_approved": False,
        "final_result": None,
    }

def start_workflow(user_request: str):
    """Start a new Concert Planner workflow execution."""

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    initial_state = create_initial_state(user_request)

    result = graph.invoke(
        initial_state,
        config=config,
    )

    return {
        "thread_id": thread_id,
        "result": result,
    }

def get_workflow_interrupt(result: dict):
    """Extract the pending interrupt from a workflow result."""

    interrupts = result.get("__interrupt__", ())

    if not interrupts:
        return None

    return interrupts[0].value

def resume_workflow(thread_id: str, user_response):
    """Resume a paused workflow with the user's response."""

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    result = graph.invoke(
        Command(resume=user_response),
        config=config,
    )

    return {
        "thread_id": thread_id,
        "result": result,
    }