from concert_planner.workflow.routers import (
    accommodation_router,
    flight_review_router,
)


def test_accommodation_router_select():
    state = {"selected_accommodation": None}

    assert accommodation_router(state) == "select"


def test_accommodation_router_travel():
    state = {"selected_accommodation": {"name": "Hotel A"}}

    assert accommodation_router(state) == "travel"


def test_flight_review_router_revise():
    state = {"selected_flight": None}

    assert flight_review_router(state) == "revise"


def test_flight_review_router_continue():
    state = {"selected_flight": {"airline": "Lufthansa"}}

    assert flight_review_router(state) == "continue"