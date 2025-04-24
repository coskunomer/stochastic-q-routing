import matplotlib.pyplot as plt
from BellmanFordNode import BellmanFordNode
from layout import generate_irregular_grid
from Network import Network

# ------------------------------------------------------------------
# Set‑up
# ------------------------------------------------------------------
graph, _ = generate_irregular_grid()
net = Network(graph, BellmanFordNode)

phases = [
    (1_000_000, 2.5), 
    (1_000_000, 1.0),   
]
record_interval = 50_000  

time_points, avg_delivery_times = [], []
cumulative_delivered = []

# ------------------------------------------------------------------
# Simulation loop
# ------------------------------------------------------------------
for phase_idx, (phase_steps, load) in enumerate(phases, start=1):
    phase_end = net.time + phase_steps
    print(f"\n📈  Starting phase {phase_idx} — load {load}, "
          f"steps {phase_steps:,}\n")

    while net.time < phase_end:
        net.inject_random_packets(load)
        net.tick()

        cumulative_delivered.extend(net.delivered_packets)
        net.delivered_packets.clear()

        if net.time % record_interval == 0:
            total_delivered = len(cumulative_delivered)
            active_packets  = sum(len(node.queue) for node in net.nodes.values())

            # Only consider packets delivered in the most recent interval
            delivered_in_interval = [
                p for p in cumulative_delivered
                if net.time - record_interval < p["delivered_at"] <= net.time
            ]

            if delivered_in_interval:
                avg_time = (
                    sum(p["delivered_at"] - p["created_at"]
                        for p in delivered_in_interval) / len(delivered_in_interval)
                )
                time_points.append(net.time)
                avg_delivery_times.append(avg_time)

                print(f"Step {net.time:,}: "
                      f"✅ delivered {total_delivered:,}  | "
                      f"📦 active {active_packets:,}  | "
                      f"⏱ avg delay (last {record_interval}) {avg_time:.2f}")

# ------------------------------------------------------------------
# Plot
# ------------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(time_points, avg_delivery_times, marker="o")
plt.xlabel("Simulation Time (steps)")
plt.ylabel("Average Delivery Time (steps)")
plt.title("Average Delivery Time Over Two‑Phase Load Profile")
plt.grid(True)
plt.tight_layout()
plt.show()
