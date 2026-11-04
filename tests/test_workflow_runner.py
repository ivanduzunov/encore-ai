from unittest.mock import Mock, patch

from langgraph.types import Command

from concert_planner.workflow.runner import (
    create_initial_state,
    get_workflow_interrupt,
    resume_workflow,
    start_workflow,
)


def test_create_initial_state():
    user_request = "Find metal festivals in Germany."

    result = create_initial_state(user_request)

    assert result == {
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

@patch("concert_planner.workflow.runner.graph")
def test_start_workflow(mock_graph):
    mock_graph.invoke.return_value = {
        "final_result": "Workflow completed."
    }

    result = start_workflow("Find metal festivals in Germany.")

    invoke_args = mock_graph.invoke.call_args
    initial_state = invoke_args.args[0]
    config = invoke_args.kwargs["config"]

    assert initial_state["user_request"] == (
        "Find metal festivals in Germany."
    )
    assert config["configurable"]["thread_id"] == result["thread_id"]
    assert result["result"] == {
        "final_result": "Workflow completed."
    }


def test_get_workflow_interrupt_returns_none():
    assert get_workflow_interrupt({}) is None
    assert get_workflow_interrupt({"__interrupt__": ()}) is None

def test_get_workflow_interrupt_returns_payload():
    interrupt = Mock()
    interrupt.value = {
        "type": "festival_selection",
        "message": "Choose a festival:",
        "options": [{"name": "Wacken Open Air"}],
    }

    result = get_workflow_interrupt(
        {"__interrupt__": (interrupt,)}
    )

    assert result == {
        "type": "festival_selection",
        "message": "Choose a festival:",
        "options": [{"name": "Wacken Open Air"}],
    }

@patch("concert_planner.workflow.runner.graph")
def test_resume_workflow(mock_graph):
    mock_graph.invoke.return_value = {
        "final_result": "Workflow completed."
    }

    thread_id = "test-thread-123"
    user_response = 1

    result = resume_workflow(thread_id, user_response)

    invoke_args = mock_graph.invoke.call_args
    command = invoke_args.args[0]
    config = invoke_args.kwargs["config"]

    assert isinstance(command, Command)
    assert command.resume == user_response

    assert config == {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    assert result == {
        "thread_id": thread_id,
        "result": {
            "final_result": "Workflow completed."
        },
    }