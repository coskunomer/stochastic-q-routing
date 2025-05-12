import random
import math
import numpy as np
from collections import deque
from q_routing.QNode import QNode


class SQRWALT(QNode):
    def __init__(self, node_id, neighbors, network):
        super().__init__(node_id, neighbors, network)

        self.temperature = 1
        self.queue_history = deque(maxlen=32)

    def process(self):
        return super().process()

    def tick_update(self):
        self.queue_history.append(len(self.queue))
        self.categorize_temperature()

    def categorize_temperature(self):
        avg = np.mean(self.queue_history)
        slope = self._queue_trend_slope(self.queue_history)

        mutliplier = 5
        if avg < 0.1:
            mutliplier = 0.1
        elif avg > 20:
            mutliplier = 20
        self.temperature = max(1e-10, mutliplier * abs(slope))

    def _queue_trend_slope(self, history):
        n = len(history)
        if n < 2:
            return 0.0

        t_vals = list(range(n))
        mean_t = sum(t_vals) / n
        mean_q = sum(history) / n

        numerator = sum((t - mean_t) * (q - mean_q) for t, q in zip(t_vals, history))
        denominator = sum((t - mean_t) ** 2 for t in t_vals)

        return numerator / denominator if denominator != 0 else 0.0

    def select_next_hop(self, dst):
        q_values = self.q_table.get(dst, {})
        if not q_values:
            return random.choice(self.neighbors)

        min_q = min(q_values.values())
        shifted_qs = {n: -(q - min_q) for n, q in q_values.items()}

        exp_values = {
            neighbor: math.exp(shifted_q / self.temperature)
            for neighbor, shifted_q in shifted_qs.items()
        }

        total = sum(exp_values.values())
        probabilities = {n: v / total for n, v in exp_values.items()}

        neighbors = list(probabilities.keys())
        weights = list(probabilities.values())
        return random.choices(neighbors, weights=weights, k=1)[0]
