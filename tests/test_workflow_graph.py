from concert_planner.workflow.graph import build_graph


def test_build_graph():
    graph = build_graph()

    assert graph is not None

def test_build_graph_contains_all_nodes():
    graph = build_graph()

    expected_nodes = {
        "festival_research",
        "select_festival",
        "select_accommodation_type",
        "accommodation_research",
        "select_accommodation",
        "flight_research",
        "review_flight",
        "confirm_purchase",
        "buy_tickets",
    }

    actual_nodes = set(graph.get_graph().nodes)

    assert expected_nodes.issubset(actual_nodes)

def test_build_graph_contains_expected_edges():
    graph = build_graph()
    actual_edges = {
        (edge.source, edge.target)
        for edge in graph.get_graph().edges
    }

    expected_edges = {
        ("__start__", "festival_research"),
        ("festival_research", "select_festival"),
        ("select_festival", "select_accommodation_type"),
        ("select_accommodation_type", "accommodation_research"),
        ("accommodation_research", "select_accommodation"),
        ("accommodation_research", "flight_research"),
        ("select_accommodation", "flight_research"),
        ("flight_research", "review_flight"),
        ("review_flight", "confirm_purchase"),
        ("review_flight", "flight_research"),
        ("confirm_purchase", "buy_tickets"),
        ("buy_tickets", "__end__"),
    }

    assert expected_edges.issubset(actual_edges)

def test_build_graph_has_checkpointer():
    graph = build_graph()

    assert graph.checkpointer is not None