"""Shared state definition for the Concert Planner workflow."""

from typing import TypedDict


class ConcertPlannerState(TypedDict):
    user_request: str
    festivals: list
    selected_festival: dict | None
    accommodation_type: str | None
    accommodations: list
    selected_accommodation: dict | None
    flights: list
    selected_flight: dict | None
    user_feedback: str | None
    total_price: float | None
    purchase_approved: bool
    final_result: str | None
