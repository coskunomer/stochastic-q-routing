import random
import numpy as np
import matplotlib.pyplot as plt

from Network import Network
from QNode import QNode
from layout import generate_irregular_grid

# ----------------------------------------
# Config
# ----------------------------------------
phases = [
    (300_000, 2.5),
    (1_000_000, 3.5),  # <-- High load
    (300_000, 2.5),
]
record_interval = 10_000
num_runs = 10

all_runs_delivery_times = []
time_points = []

# ----------------------------------------
# Multiple Simulations
# ----------------------------------------
for seed in range(num_runs):
    print(f"\n🎲 Run {seed + 1}/{num_runs} — Seed = {seed}")
    random.seed(seed)

    graph, _ = generate_irregular_grid()
    net = Network(graph, QNode)

    run_delivery_times = []
    cumulative_delivered = []

    for idx, (phase_steps, load) in enumerate(phases, start=1):
        phase_end = net.time + phase_steps
        print(f"\n📊 Phase {idx}: {phase_steps:,} steps, load {load}")

        while net.time < phase_end:
            net.inject_random_packets(load)
            net.tick()

            cumulative_delivered.extend(net.delivered_packets)
            net.delivered_packets.clear()

            if net.time % record_interval == 0:
                delivered_in_interval = [
                    p for p in cumulative_delivered
                    if net.time - record_interval < p["delivered_at"] <= net.time
                ]

                if delivered_in_interval:
                    avg_time = sum(
                        p["delivered_at"] - p["created_at"]
                        for p in delivered_in_interval
                    ) / len(delivered_in_interval)

                    run_delivery_times.append(avg_time)

                    if seed == 0:
                        time_points.append(net.time)

                    print(f"  Step {net.time:,}: avg delay (last {record_interval}) = {avg_time:.2f}")

    all_runs_delivery_times.append(run_delivery_times)

# ----------------------------------------
# Aggregate & Save Data
# ----------------------------------------
avg_over_runs = np.mean(all_runs_delivery_times, axis=0)
std_dev = np.std(all_runs_delivery_times, axis=0)

np.savez("results/q_routing_results.npz", time=np.array(time_points), avg=avg_over_runs, std=std_dev)

# ----------------------------------------
# Plotting
# ----------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(time_points, avg_over_runs, label="Average Delay", color="blue")
plt.fill_between(time_points,
                 avg_over_runs - std_dev,
                 avg_over_runs + std_dev,
                 color="blue", alpha=0.2, label="±1 std. dev.")

# High load phase start and end
high_load_start = time_points.index(min(t for t in time_points if t >= 300_000)) 
high_load_end = time_points.index(min(t for t in time_points if t >= 1_300_000)) 

hl_start_x = time_points[high_load_start]
hl_end_x = time_points[high_load_end]

plt.axvline(x=hl_start_x, color="red", linestyle="dotted")
plt.axvline(x=hl_end_x, color="red", linestyle="dotted")
plt.text(hl_start_x, max(avg_over_runs), "High Load Start", color="red", ha="left", va="bottom")
plt.text(hl_end_x, max(avg_over_runs), "High Load End", color="red", ha="left", va="bottom")

plt.xlabel("Simulation Time (steps, ×10⁵)")
plt.ylabel("Average Delivery Time (steps)")
plt.title(f"Q-Routing: Avg Delay over {num_runs} Runs with Load Phases")
plt.grid(True)
plt.legend()

plt.xticks(
    ticks=[t for t in time_points if t % 100_000 == 0],
    labels=[f"{t // 100_000}×10⁵" for t in time_points if t % 100_000 == 0]
)

plt.tight_layout()
plt.show()
