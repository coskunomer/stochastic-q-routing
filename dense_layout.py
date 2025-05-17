import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt

def generate_dense_irregular_grid():
    graph = defaultdict(list)
    G = nx.Graph()
    N = 6  # 6x6 grid

    def connect(u, v):
        weight = 1
        graph[u].append((v, weight))
        graph[v].append((u, weight))  
        G.add_edge(u, v, weight=weight)

    for i in range(N * N):
        row, col = divmod(i, N)

        if col < N - 1:
            connect(i, i + 1)

        if row < N - 1:
            connect(i, i + N)

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
    plt.title("6x6 Dense Grid Network")
    plt.axis("off")
    plt.show()

# graph, G = generate_dense_irregular_grid()
# visualize_grid(graph)