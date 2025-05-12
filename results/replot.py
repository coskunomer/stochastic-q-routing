import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# Load Data
# ----------------------------------------
q_data = np.load("results/q_routing_results.npz")
sqr_data = np.load("results/sqr_results.npz")
sqrwalt_data = np.load("results/sqrwalt_results.npz")

q_time = q_data["time"]
q_avg = q_data["avg"]
q_std = q_data["std"]

sqr_time = sqr_data["time"]
sqr_avg = sqr_data["avg"]
sqr_std = sqr_data["std"]

sqrwalt_time = sqrwalt_data["time"]  
sqrwalt_avg = sqrwalt_data["avg"] 
sqrwalt_std = sqrwalt_data["std"] 

# ----------------------------------------
# Plotting
# ----------------------------------------
plt.figure(figsize=(10, 5))

# Q-Routing
plt.plot(q_time, q_avg, label="Q-Routing", color="blue")
plt.fill_between(q_time, q_avg - q_std, q_avg + q_std, color="blue", alpha=0.2)

# SQR
plt.plot(sqr_time, sqr_avg, label="SQR", color="green")
plt.fill_between(sqr_time, sqr_avg - sqr_std, sqr_avg + sqr_std, color="green", alpha=0.2)

# SQRWALT
plt.plot(sqrwalt_time, sqrwalt_avg, label="SQRWALT", color="red")
plt.fill_between(sqrwalt_time, sqrwalt_avg - sqrwalt_std, sqrwalt_avg + sqrwalt_std, color="red", alpha=0.2)

# High Load Markers
hl_start_x = 300_000
hl_end_x = 1_300_000
y_max = max(
    np.max(q_avg + q_std),
    np.max(sqr_avg + sqr_std),
    np.max(sqrwalt_avg + sqrwalt_std)
)

plt.axvline(x=hl_start_x, color="red", linestyle="dotted")
plt.axvline(x=hl_end_x, color="red", linestyle="dotted")
plt.text(hl_start_x, y_max, "High Load Start", color="red", ha="left", va="bottom")
plt.text(hl_end_x, y_max, "High Load End", color="red", ha="left", va="bottom")

# Labels & Aesthetics
plt.xlabel("Simulation Time (steps)")
plt.ylabel("Average Delivery Time (steps)")
plt.title("Average Delivery Time Over Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ----------------------------------------
# Reporting Stats (Excluding First 100k of Each Phase)
# ----------------------------------------
phases = [
    ("1st Low Load", 0, 300_000),
    ("High Load", 300_000, 1_300_000),
    ("2nd Low Load", 1_300_000, 1_600_000),
]

def filter_stable_phase(time_array, avg_array, start, end):
    mask = (time_array > start + 100_000) & (time_array <= end)
    return avg_array[mask]

def print_stats(name, time_array, avg_array):
    print(f"\n📊 {name}")
    for label, start, end in phases:
        filtered = filter_stable_phase(time_array, avg_array, start, end)
        if len(filtered) > 0:
            mean = np.mean(filtered)
            std = np.std(filtered)
            print(f"  {label:<15} → Mean: {mean:.2f}, Std: {std:.2f}")
        else:
            print(f"  {label:<15} → No data")

print_stats("Q-Routing", q_time, q_avg)
print_stats("SQR", sqr_time, sqr_avg)
print_stats("SQRWALT", sqrwalt_time, sqrwalt_avg) 