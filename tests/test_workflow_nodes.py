from unittest.mock import patch

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

@patch("concert_planner.workflow.nodes.interrupt", return_value=1)
def test_select_accommodation_type_node(mock_interrupt):
    state = {}

    result = select_accommodation_type_node(state)

    mock_interrupt.assert_called_once_with(
        {
            "type": "accommodation_type",
            "message": "Where would you like to stay?",
            "options": ["hotel", "camping"],
        }
    )

    assert result == {
        "accommodation_type": "camping",
    }

@patch("concert_planner.workflow.nodes.interrupt", return_value=1)
def test_select_accommodation_node(mock_interrupt):
    accommodations = [
        {"name": "Hotel A", "price": 200},
        {"name": "Hotel B", "price": 300},
    ]
    state = {"accommodations": accommodations}

    result = select_accommodation_node(state)

    mock_interrupt.assert_called_once_with(
        {
            "type": "accommodation_selection",
            "message": "Choose accommodation",
            "options": accommodations,
        }
    )

    assert result == {
        "selected_accommodation": accommodations[1],
    }

@patch(
    "concert_planner.workflow.nodes.interrupt",
    return_value={"action": "select", "selection": 1},
)
def test_review_flight_node_select(mock_interrupt):
    flights = [
        {"airline": "Airline A", "price": 200},
        {"airline": "Airline B", "price": 300},
    ]
    state = {"flights": flights}

    result = review_flight_node(state)

    mock_interrupt.assert_called_once_with(
        {
            "type": "flight_review",
            "message": (
                "Review the flight options. "
                "You can select a flight or request a revision."
            ),
            "options": flights,
        }
    )

    assert result == {
        "selected_flight": flights[1],
        "user_feedback": None,
    }

@patch(
    "concert_planner.workflow.nodes.interrupt",
    return_value={
        "action": "revise",
        "feedback": "Find cheaper flights.",
    },
)
def test_review_flight_node_revise(mock_interrupt):
    state = {
        "flights": [
            {"airline": "Airline A", "price": 200},
        ]
    }

    result = review_flight_node(state)

    mock_interrupt.assert_called_once()

    assert result == {
        "selected_flight": None,
        "user_feedback": "Find cheaper flights.",
    }

@patch(
    "concert_planner.workflow.nodes.interrupt",
    return_value=True,
)
def test_confirm_purchase_node(mock_interrupt):
    festival = {"name": "Wacken Open Air", "price": 250}
    accommodation = {"name": "Camping", "price": 100}
    flight = {"airline": "Lufthansa", "price": 200}

    state = {
        "selected_festival": festival,
        "selected_accommodation": accommodation,
        "selected_flight": flight,
    }

    result = confirm_purchase_node(state)

    mock_interrupt.assert_called_once_with(
        {
            "type": "purchase_confirmation",
            "message": "Please review your trip before purchase.",
            "festival": festival,
            "accommodation": accommodation,
            "flight": flight,
            "total_price": 550,
        }
    )

    assert result == {
        "purchase_approved": True,
    }

def test_buy_tickets_node_purchase_cancelled():
    state = {
        "purchase_approved": False,
    }

    result = buy_tickets_node(state)

    assert result == {
        "final_result": "Purchase cancelled by user.",
    }

@patch("concert_planner.workflow.nodes.generate_final_summary")
@patch("concert_planner.workflow.nodes.calculate_total_price")
def test_buy_tickets_node_purchase_approved(
    mock_calculate_total_price,
    mock_generate_final_summary,
):
    festival = {"name": "Wacken Open Air", "price": 250}
    accommodation = {"name": "Camping", "price": 100}
    flight = {"airline": "Lufthansa", "price": 200}

    state = {
        "purchase_approved": True,
        "selected_festival": festival,
        "selected_accommodation": accommodation,
        "selected_flight": flight,
    }

    mock_calculate_total_price.invoke.return_value = 550
    mock_generate_final_summary.invoke.return_value = (
        "Your trip to Wacken Open Air is confirmed!"
    )

    result = buy_tickets_node(state)

    mock_calculate_total_price.invoke.assert_called_once_with(
        {
            "festival": festival,
            "accommodation": accommodation,
            "flight": flight,
        }
    )

    mock_generate_final_summary.invoke.assert_called_once_with(
        {
            "festival": festival,
            "accommodation": accommodation,
            "flight": flight,
            "total_price": 550,
        }
    )

    assert result == {
        "final_result": "Your trip to Wacken Open Air is confirmed!",
        "total_price": 550,
    }