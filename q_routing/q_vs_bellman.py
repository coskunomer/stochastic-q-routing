import numpy as np
import matplotlib.pyplot as plt
import random

from Network import Network
from q_routing.QNode import QNode
from bellman_ford.BellmanFordNode import BellmanFordNode
from layout import generate_irregular_grid

# ----------------------------------------
# Configuration
# ----------------------------------------
load_levels = np.arange(0.5, 4.5 + 0.01, 0.25)
num_steps = 60_000
discard_steps = 30_000

seeds = [i for i in range(20)]

def run_experiment(NodeClass, load):
    all_avg_delays = []

    for seed in seeds:
        random.seed(seed)
        graph, _ = generate_irregular_grid()
        net = Network(graph, NodeClass)

        cumulative_delivered = []

        # Run main simulation
        while net.time < num_steps:
            net.inject_random_packets(load)
            net.tick()

            cumulative_delivered.extend(net.delivered_packets)
            net.delivered_packets.clear()

        delivered = [
            p for p in cumulative_delivered
            if p["created_at"] > discard_steps
        ]

        avg_delay = np.mean([
                p["delivered_at"] - p["created_at"]
                for p in delivered
            ])
        all_avg_delays.append(avg_delay)

    return np.mean(all_avg_delays) if all_avg_delays else None


# ----------------------------------------
# Run Simulations
# ----------------------------------------
q_routing_results = []
bellman_ford_results = []

for load in load_levels:
    print(f"\n▶️ Load {load:.2f}")

    q_delay = run_experiment(QNode, load)
    bf_delay = run_experiment(BellmanFordNode, load)

    q_routing_results.append(q_delay)
    bellman_ford_results.append(bf_delay)

# ----------------------------------------
# Plotting
# ----------------------------------------
global_min = int(min(min(q_routing_results), min(bellman_ford_results)))
clip_max = 20

q_plot = np.clip(q_routing_results, global_min, clip_max)
bf_plot = np.clip(bellman_ford_results, global_min, clip_max)

plt.figure(figsize=(10, 6))
plt.plot(load_levels, q_plot, label="Q-Routing", linewidth=2)
plt.plot(load_levels, bf_plot, linestyle='dotted', label="Bellman-Ford", linewidth=2)

plt.xlabel("Network Load")
plt.ylabel("Average Packet Delivery Time")
plt.title("Average Delivery Time vs Load")
plt.ylim(global_min, clip_max)
plt.xticks(np.arange(0.5, load_levels[-1] + 0.01, 0.5))
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
