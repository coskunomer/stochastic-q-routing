from layout import generate_irregular_grid

graph, G = generate_irregular_grid()

def get_shortest_path(graph, source):
    """
    Bellman-Ford algorithm for graphs with non-negative edge weights.
    Returns:
        distances: node -> total cost from source
        predecessors: node -> previous hop on shortest path
    """
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[source] = 0

    for _ in range(len(graph) - 1):
        for u in graph:
            for v, cost in graph[u]:
                if distances[u] + cost < distances[v]:
                    distances[v] = distances[u] + cost
                    predecessors[v] = u

    return distances, predecessors

def compute_all_routing_tables(graph):
    all_tables = {}
    for node in graph:
        dist, pred = get_shortest_path(graph, node)
        table = {}
        for dst in graph:
            if dst == node:
                continue
            next_hop = dst
            while pred[next_hop] and pred[next_hop] != node:
                next_hop = pred[next_hop]
            if pred[next_hop] is None and next_hop != node:
                next_hop = None
            table[dst] = {
                "cost": dist[dst],
                "next_hop": next_hop,
            }
        all_tables[node] = table
    return all_tables


def print_routing_tables(tables):
    for src in sorted(tables):
        print(f"Routing table for node {src}:")
        for dst in sorted(tables[src]):
            info = tables[src][dst]
            cost = info["cost"]
            next_hop = info["next_hop"]
            print(f"  to {dst:2}: cost={cost:2}, next hop={next_hop}")
        print("-" * 40)

routing_tables = compute_all_routing_tables(graph)
