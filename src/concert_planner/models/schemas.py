
"""Pydantic models used by the Concert Planner agents."""

from pydantic import BaseModel


class Festival(BaseModel):
    """A music festival recommendation."""

    name: str
    country: str
    city: str
    price: float
    genre: str
    dates: str


class FestivalResults(BaseModel):
    """Structured festival research results."""

    festivals: list[Festival]


class Accommodation(BaseModel):
    """An accommodation recommendation."""

    name: str
    country: str
    city: str
    price: float
    type: str


class AccommodationResults(BaseModel):
    """Structured accommodation research results."""

    accommodations: list[Accommodation]


class Flight(BaseModel):
    """A flight recommendation."""

    airline: str
    departure: str
    arrival: str
    route: str
    price: float
    duration: str


class FlightResults(BaseModel):
    """Structured flight research results."""

    flights: list[Flight]
