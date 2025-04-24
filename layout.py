import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt

def generate_irregular_grid():
    graph = defaultdict(list)
    G = nx.Graph()

    def connect(u, v):
        weight = 1
        graph[u].append((v, weight))
        graph[v].append((u, weight))  
        G.add_edge(u, v, weight=weight)

    connections = [
        (0, 1), (0, 6),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 11),

        (6, 12),
        (7, 8), (7, 13),
        (8, 14),
        (9, 10), (9, 15),
        (10, 16),
        (11, 17),

        (12, 13), (12, 18),
        (13, 14), (13, 19),
        (14, 15), (14, 20),
        (15, 16), (15, 21),
        (16, 17), (16, 22),
        (17, 23),

        (18, 19), (18, 24),
        (19, 20), (19, 25),
        (20, 26),
        (21, 22), (21, 27),
        (22, 23), (22, 28),
        (23, 29),

        (24, 25), (24, 30),
        (25, 26), (25, 31),
        (26, 32),
        (27, 28), (27, 33),
        (28, 29), (28, 34),
        (29, 35),

        (30, 31),
        (31, 32),
        (33, 34),
        (34, 35),
    ]

    for u, v in connections:
        connect(u, v)

    return graph, G

def visualize_grid(graph):
    N = 6
    NODES = N * N
    
    G = nx.Graph()

    for node, neighbors in graph.items():
        for neighbor, _ in neighbors:
            G.add_edge(node, neighbor)

    pos = {i: (i % N, N - 1 - i // N) for i in range(NODES)}

    plt.figure(figsize=(8, 8))
    nx.draw(
        G, pos,
        with_labels=True,
        node_size=500,
        node_color="skyblue",
        edge_color="gray",
        font_size=10,
        font_weight="bold"
    )
    plt.title("6x6 Irregular Grid Network")
    plt.axis("off")
    plt.show()