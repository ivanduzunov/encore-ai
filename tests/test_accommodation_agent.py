from unittest.mock import MagicMock, patch

from concert_planner.agents.accommodation_agent import (
    create_accommodation_agent,
    create_llm,
    find_accommodation,
    initialize_accommodation_agent,
)
from concert_planner.config.settings import OPENAI_API_KEY
from concert_planner.models import Accommodation, AccommodationResults


def test_create_accommodation_agent():
    llm = MagicMock()

    create_accommodation_agent(llm)

    llm.with_structured_output.assert_called_once_with(AccommodationResults)


def test_initialize_accommodation_agent():
    with (
        patch("concert_planner.agents.accommodation_agent.create_llm") as mock_create_llm,
        patch(
            "concert_planner.agents.accommodation_agent.create_accommodation_agent"
        ) as mock_create_agent,
    ):
        llm = MagicMock()
        agent = MagicMock()

        mock_create_llm.return_value = llm
        mock_create_agent.return_value = agent

        result = initialize_accommodation_agent()

        mock_create_llm.assert_called_once()
        mock_create_agent.assert_called_once_with(llm)
        assert result == agent


@patch("concert_planner.agents.accommodation_agent.ChatOpenAI")
def test_create_llm(mock_chat_openai):
    create_llm()

    mock_chat_openai.assert_called_once_with(
        model="gpt-5-nano",
        api_key=OPENAI_API_KEY,
    )


def test_find_accommodation_hotel():
    festival = {
        "name": "Wacken Open Air",
        "city": "Wacken",
        "country": "Germany",
        "price": 250,
        "genre": "Metal",
        "dates": "July 29 - August 1",
    }

    accommodation = Accommodation(
        name="Hotel Example",
        country="Germany",
        city="Wacken",
        price=120,
        type="hotel",
    )

    agent = MagicMock()
    agent.invoke.return_value = MagicMock(accommodations=[accommodation])

    state = {
        "selected_festival": festival,
        "accommodation_type": "hotel",
    }

    result = find_accommodation(state, agent)

    agent.invoke.assert_called_once()

    assert result["accommodations"] == [accommodation.model_dump()]
    assert "selected_accommodation" not in result


def test_find_accommodation_camping():
    festival = {
        "name": "Wacken Open Air",
        "city": "Wacken",
        "country": "Germany",
        "price": 250,
        "genre": "Metal",
        "dates": "July 29 - August 1",
    }

    agent = MagicMock()

    state = {
        "selected_festival": festival,
        "accommodation_type": "camping",
    }

    result = find_accommodation(state, agent)

    expected_camping = {
        "name": "Wacken Open Air Official Camping",
        "type": "camping",
        "city": "Wacken",
        "price": 0,
        "description": "Official festival camping.",
    }

    agent.invoke.assert_not_called()

    assert result["accommodations"] == [expected_camping]
    assert result["selected_accommodation"] == expected_camping
