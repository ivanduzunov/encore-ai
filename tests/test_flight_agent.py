from unittest.mock import MagicMock, patch

from concert_planner.agents.flight_agent import (
    create_flight_agent,
    create_llm,
    initialize_flight_agent,
    research_flights,
)
from concert_planner.config.settings import OPENAI_API_KEY
from concert_planner.models import Flight, FlightResults


def test_create_flight_agent():
    mock_llm = MagicMock()

    create_flight_agent(mock_llm)

    mock_llm.with_structured_output.assert_called_once_with(FlightResults)


def test_initialize_flight_agent():
    mock_llm = MagicMock()
    mock_agent = MagicMock()

    with (
        patch(
            "concert_planner.agents.flight_agent.create_llm",
            return_value=mock_llm,
        ),
        patch(
            "concert_planner.agents.flight_agent.create_flight_agent",
            return_value=mock_agent,
        ),
    ):
        result = initialize_flight_agent()

    assert result is mock_agent


@patch("concert_planner.agents.flight_agent.ChatOpenAI")
def test_create_llm(mock_chat_openai):
    create_llm()

    mock_chat_openai.assert_called_once_with(
        model="gpt-5-nano",
        api_key=OPENAI_API_KEY,
    )

def test_research_flights():
    flight = Flight(
        airline="Lufthansa",
        departure="Sofia",
        arrival="Berlin",
        route="SOF-FRA-BER",
        price=250.0,
        duration="4 hours",
    )

    mock_agent = MagicMock()
    mock_agent.invoke.return_value = MagicMock(
        flights=[flight]
    )

    state = {
        "selected_festival": {"name": "Wacken Open Air"},
        "selected_accommodation": {"name": "Festival Camping"},
        "user_feedback": None,
    }

    result = research_flights(state, mock_agent)

    mock_agent.invoke.assert_called_once()

    assert result == {
        "flights": [flight.model_dump()]
    }


def test_research_flights_with_feedback():
    flight = Flight(
        airline="Ryanair",
        departure="Sofia",
        arrival="Hamburg",
        route="SOF-HAM",
        price=180.0,
        duration="3 hours",
    )

    mock_agent = MagicMock()
    mock_agent.invoke.return_value = MagicMock(
        flights=[flight]
    )

    state = {
        "selected_festival": {"name": "Wacken Open Air"},
        "selected_accommodation": {"name": "Festival Camping"},
        "user_feedback": "Find cheaper flights.",
    }

    result = research_flights(state, mock_agent)

    messages = mock_agent.invoke.call_args.args[0]
    human_prompt = messages[1].content

    assert "Find cheaper flights." in human_prompt
    assert "Do not simply repeat the previous options." in human_prompt
    assert result["flights"] == [flight.model_dump()]