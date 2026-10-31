"""Tool for generating the final Concert Planner trip summary."""

from langchain_core.tools import tool


@tool
def generate_final_summary(
    festival: dict,
    accommodation: dict,
    flight: dict,
    total_price: float,
) -> str:
    """Print and format the final Concert Planner trip result."""

    result = f"""
    ==============================
          CONCERT PLANNER
    ==============================

    🎵 FESTIVAL
    {festival["name"]}
    {festival["city"]}, {festival["country"]}
    Dates: {festival["dates"]}
    Price: €{festival["price"]}

    🏨 ACCOMMODATION
    {accommodation["name"]}
    {accommodation["city"]}
    Price: €{accommodation["price"]}

    ✈️ FLIGHT
    {flight["airline"]}
    {flight["route"]}
    Departure: {flight["departure"]}
    Arrival: {flight["arrival"]}
    Price: €{flight["price"]}

    💰 TOTAL PRICE
    €{total_price}

    ==============================
    """

    print(result)

    return result
