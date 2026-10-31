
"""Tool for calculating the total festival trip price."""

from langchain_core.tools import tool


@tool
def calculate_total_price(
    festival_price: float,
    accommodation_price: float,
    flight_price: float,
) -> float:
    """
    Calculate the total price of the festival trip.
    """
    return (
        festival_price
        + accommodation_price
        + flight_price
    )
