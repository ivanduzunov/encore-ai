"""Tests for custom LangChain tools."""

from concert_planner.tools import calculate_total_price, generate_final_summary


def test_calculate_total_price():
    """The tool should return the sum of all trip expenses."""

    result = calculate_total_price.invoke(
        {
            "festival_price": 150,
            "accommodation_price": 200,
            "flight_price": 100,
        }
    )

    assert result == 450



def test_generate_final_summary():
    """The tool should generate a summary of the complete trip."""

    festival = {
        "name": "Rock Festival",
        "city": "Sofia",
        "country": "Bulgaria",
        "dates": "10-12 July",
        "price": 150,
    }

    accommodation = {
        "name": "Festival Hotel",
        "city": "Sofia",
        "price": 200,
    }

    flight = {
        "airline": "Bulgaria Air",
        "route": "Sofia - Berlin",
        "departure": "10 July",
        "arrival": "10 July",
        "price": 100,
    }

    result = generate_final_summary.invoke(
        {
            "festival": festival,
            "accommodation": accommodation,
            "flight": flight,
            "total_price": 450,
        }
    )

    assert "Rock Festival" in result
    assert "Festival Hotel" in result
    assert "Bulgaria Air" in result
    assert "€450" in result