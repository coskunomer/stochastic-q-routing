from Network import Network
from StochasticQNode import StochasticQNode
from layout  import generate_irregular_grid
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Set‑up
# ------------------------------------------------------------------
graph, _ = generate_irregular_grid()
net = Network(graph, StochasticQNode)

# traffic pattern: (steps, load)
phases = [
    (1_000_000, 2.5), 
    (1_000_000, 3.5),   
    (1_000_000, 2.5), 
]
record_interval = 50_000

time_points, avg_delivery_times = [], []
cumulative_delivered = []

# ------------------------------------------------------------------
# Simulation
# ------------------------------------------------------------------
for idx, (phase_steps, load) in enumerate(phases, start=1):
    phase_end = net.time + phase_steps
    print(f"\n📊  Phase {idx}: {phase_steps:,} steps, load {load}")

    while net.time < phase_end:
        net.inject_random_packets(load)
        net.tick()

        cumulative_delivered.extend(net.delivered_packets)
        net.delivered_packets.clear()

        if net.time % record_interval == 0:
            total = len(cumulative_delivered)
            active = sum(len(node.queue) for node in net.nodes.values())

            # Get delivery delay only for packets delivered in this interval
            delivered_in_interval = [
                p for p in cumulative_delivered
                if net.time - record_interval < p["delivered_at"] <= net.time
            ]

            if delivered_in_interval:
                avg_time = sum(p["delivered_at"] - p["created_at"]
                            for p in delivered_in_interval) / len(delivered_in_interval)
                time_points.append(net.time)
                avg_delivery_times.append(avg_time)

                print(f"  Step {net.time:,}: "
                    f"✅ {total:,} delivered | "
                    f"📦 {active:,} active | "
                    f"⏱ avg delay (last {record_interval}) {avg_time:.2f}")


# ------------------------------------------------------------------
# Plot
# ------------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(time_points, avg_delivery_times, marker="o")
plt.xlabel("Simulation Time (steps)")
plt.ylabel("Average Delivery Time (steps)")
plt.title("Q‑Routing: Average Delivery Time Across Two‑Phase Load Profile")
plt.grid(True)
plt.tight_layout()
plt.show()
