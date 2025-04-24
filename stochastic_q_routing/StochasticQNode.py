import random
import math
from q_routing.QNode import QNode

class StochasticQNode(QNode):
    def select_next_hop(self, dst):
        """Stochastically choose neighbor based on Q-values — lower values are better."""
        q_values = self.q_table.get(dst, {})

        if not q_values:
            return random.choice(self.neighbors)

        # Convert Q-values into probabilities
        # Lower Q => higher probability, using softmax with negative Qs
        temperature = 0.001

        # Avoid overflow by shifting values before exponentiating
        min_q = min(q_values.values())
        shifted_qs = {n: -(q - min_q) for n, q in q_values.items()} 

        exp_values = {
            neighbor: math.exp(shifted_q / temperature)
            for neighbor, shifted_q in shifted_qs.items()
        }

        total = sum(exp_values.values())
        probabilities = {n: v / total for n, v in exp_values.items()}

        # Sample based on computed probabilities
        neighbors = list(probabilities.keys())
        weights = list(probabilities.values())
        return random.choices(neighbors, weights=weights, k=1)[0]
