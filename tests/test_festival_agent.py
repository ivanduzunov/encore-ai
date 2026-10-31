"""Tests for the Festival Research Agent."""

from unittest.mock import MagicMock, patch

from concert_planner.agents.festival_agent import (
    create_festival_agent,
    create_llm,
    initialize_festival_agent,
    research_festivals,
)
from concert_planner.config.settings import OPENAI_API_KEY
from concert_planner.models import FestivalResults


def test_research_festivals():
    """The agent should return festivals as a list of dictionaries."""

    festival = MagicMock()
    festival.model_dump.return_value = {
        "name": "Wacken Open Air",
        "country": "Germany",
        "city": "Wacken",
        "price": 250.0,
        "genre": "Metal",
        "dates": "29 July - 1 August",
    }

    agent_result = MagicMock()
    agent_result.festivals = [festival]

    festival_agent = MagicMock()
    festival_agent.invoke.return_value = agent_result

    state = {
        "user_request": "Find metal festivals in Europe with a budget of 300 EUR.",
    }

    result = research_festivals(state, festival_agent)

    festival_agent.invoke.assert_called_once()
    assert result == {
        "festivals": [
            {
                "name": "Wacken Open Air",
                "country": "Germany",
                "city": "Wacken",
                "price": 250.0,
                "genre": "Metal",
                "dates": "29 July - 1 August",
            }
        ]
    }


def test_create_festival_agent():
    """The factory should configure structured output with FestivalResults."""

    llm = MagicMock()

    create_festival_agent(llm)

    llm.with_structured_output.assert_called_once_with(FestivalResults)


def test_initialize_festival_agent():
    """The initializer should create and return a configured festival agent."""

    with (
        patch("concert_planner.agents.festival_agent.create_llm") as mock_create_llm,
        patch("concert_planner.agents.festival_agent.create_festival_agent") as mock_create_agent,
    ):
        llm = MagicMock()
        agent = MagicMock()

        mock_create_llm.return_value = llm
        mock_create_agent.return_value = agent

        result = initialize_festival_agent()

        mock_create_llm.assert_called_once_with()
        mock_create_agent.assert_called_once_with(llm)
        assert result is agent


def test_create_llm():
    """The LLM should use the configured model and API key."""

    with patch("concert_planner.agents.festival_agent.ChatOpenAI") as mock_chat_openai:
        create_llm()

        mock_chat_openai.assert_called_once_with(
            model="gpt-5-nano",
            api_key=OPENAI_API_KEY,
        )
