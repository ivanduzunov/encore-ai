from unittest.mock import patch

from concert_planner.workflow.nodes import (
    accommodation_research_node,
    festival_research_node,
    flight_research_node,
    select_festival_node,
)


@patch("concert_planner.workflow.nodes.research_festivals")
@patch("concert_planner.workflow.nodes.initialize_festival_agent")
def test_festival_research_node(
    mock_initialize_agent,
    mock_research_festivals,
):
    mock_agent = object()
    mock_initialize_agent.return_value = mock_agent

    expected_result = {
        "festivals": [
            {"name": "Wacken Open Air"},
        ]
    }
    mock_research_festivals.return_value = expected_result

    state = {
        "user_request": "Find metal festivals in Europe",
    }

    result = festival_research_node(state)

    mock_initialize_agent.assert_called_once_with()
    mock_research_festivals.assert_called_once_with(
        state,
        mock_agent,
    )
    assert result == expected_result


@patch("concert_planner.workflow.nodes.find_accommodation")
@patch("concert_planner.workflow.nodes.initialize_accommodation_agent")
def test_accommodation_research_node(
    mock_initialize_agent,
    mock_find_accommodation,
):
    mock_agent = object()
    mock_initialize_agent.return_value = mock_agent

    expected_result = {
        "accommodations": [
            {"name": "Festival Hotel"},
        ]
    }
    mock_find_accommodation.return_value = expected_result

    state = {
        "selected_festival": {"name": "Wacken Open Air"},
        "accommodation_type": "hotel",
    }

    result = accommodation_research_node(state)

    mock_initialize_agent.assert_called_once_with()
    mock_find_accommodation.assert_called_once_with(
        state,
        mock_agent,
    )
    assert result == expected_result

@patch("concert_planner.workflow.nodes.research_flights")
@patch("concert_planner.workflow.nodes.initialize_flight_agent")
def test_flight_research_node(
    mock_initialize_agent,
    mock_research_flights,
):
    mock_agent = object()
    mock_initialize_agent.return_value = mock_agent

    expected_result = {
        "flights": [
            {"airline": "Lufthansa"},
        ]
    }
    mock_research_flights.return_value = expected_result

    state = {
        "selected_festival": {"name": "Wacken Open Air"},
        "selected_accommodation": {"name": "Festival Camping"},
    }

    result = flight_research_node(state)

    mock_initialize_agent.assert_called_once_with()
    mock_research_flights.assert_called_once_with(
        state,
        mock_agent,
    )
    assert result == expected_result

@patch("concert_planner.workflow.nodes.interrupt", return_value=1)
def test_select_festival_node(mock_interrupt):
    festivals = [
        {"name": "Wacken Open Air"},
        {"name": "Nova Rock"},
    ]

    state = {
        "festivals": festivals,
    }

    result = select_festival_node(state)

    mock_interrupt.assert_called_once_with(
        {
            "type": "festival_selection",
            "message": "Choose a festival:",
            "options": festivals,
        }
    )

    assert result == {
        "selected_festival": festivals[1],
    }