from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from concert_planner.workflow.runner import get_workflow_interrupt


class TestWorkflowState(TypedDict):
    user_response: str


def test_workflow_interrupt_and_resume():
    def wait_for_user(state: TestWorkflowState):
        response = interrupt(
            {
                "type": "test_interaction",
                "message": "Please provide your response.",
            }
        )

        return {"user_response": response}

    workflow = StateGraph(TestWorkflowState)

    workflow.add_node("wait_for_user", wait_for_user)
    workflow.add_edge(START, "wait_for_user")
    workflow.add_edge("wait_for_user", END)

    checkpointer = InMemorySaver()
    test_graph = workflow.compile(checkpointer=checkpointer)

    config = {
        "configurable": {
            "thread_id": "integration-test-123",
        }
    }

    # Start workflow
    initial_result = test_graph.invoke(
        {"user_response": ""},
        config=config,
    )

    assert "__interrupt__" in initial_result
    assert initial_result["__interrupt__"][0].value == {
        "type": "test_interaction",
        "message": "Please provide your response.",
    }

    # Resume workflow
    resumed_result = test_graph.invoke(
        Command(resume="Wacken Open Air"),
        config=config,
    )

    assert resumed_result["user_response"] == "Wacken Open Air"

def test_get_workflow_interrupt_with_real_langgraph_result():
    def wait_for_user(state: TestWorkflowState):
        response = interrupt(
            {
                "type": "test_interaction",
                "message": "Please provide your response.",
            }
        )
        return {"user_response": response}

    workflow = StateGraph(TestWorkflowState)
    workflow.add_node("wait_for_user", wait_for_user)
    workflow.add_edge(START, "wait_for_user")
    workflow.add_edge("wait_for_user", END)

    test_graph = workflow.compile(checkpointer=InMemorySaver())

    result = test_graph.invoke(
        {"user_response": ""},
        config={
            "configurable": {
                "thread_id": "interrupt-extraction-test",
            }
        },
    )

    interrupt_payload = get_workflow_interrupt(result)

    assert interrupt_payload == {
        "type": "test_interaction",
        "message": "Please provide your response.",
    }

def test_workflow_multiple_interrupts_and_resumes():
    class MultiStepState(TypedDict):
        festival: str
        accommodation: str

    def select_festival(state: MultiStepState):
        festival = interrupt(
            {
                "type": "festival_selection",
                "message": "Choose a festival:",
            }
        )
        return {"festival": festival}

    def select_accommodation(state: MultiStepState):
        accommodation = interrupt(
            {
                "type": "accommodation_selection",
                "message": "Choose accommodation:",
            }
        )
        return {"accommodation": accommodation}

    workflow = StateGraph(MultiStepState)

    workflow.add_node("select_festival", select_festival)
    workflow.add_node("select_accommodation", select_accommodation)

    workflow.add_edge(START, "select_festival")
    workflow.add_edge("select_festival", "select_accommodation")
    workflow.add_edge("select_accommodation", END)

    test_graph = workflow.compile(
        checkpointer=InMemorySaver()
    )

    config = {
        "configurable": {
            "thread_id": "multi-interrupt-test",
        }
    }

    # First interrupt: festival selection
    first_result = test_graph.invoke(
        {"festival": "", "accommodation": ""},
        config=config,
    )

    assert first_result["__interrupt__"][0].value["type"] == (
        "festival_selection"
    )

    # Resume with festival selection
    second_result = test_graph.invoke(
        Command(resume="Wacken Open Air"),
        config=config,
    )

    assert second_result["festival"] == "Wacken Open Air"
    assert second_result["__interrupt__"][0].value["type"] == (
        "accommodation_selection"
    )

    # Resume with accommodation selection
    final_result = test_graph.invoke(
        Command(resume="Camping"),
        config=config,
    )

    assert final_result["festival"] == "Wacken Open Air"
    assert final_result["accommodation"] == "Camping"
    assert "__interrupt__" not in final_result