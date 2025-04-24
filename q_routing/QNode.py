from collections import deque

class QNode:
    def __init__(self, node_id, neighbors, network):
        self.id = node_id
        self.neighbors = neighbors
        self.queue = deque()
        self.network = network
        self.alpha = 0.5
        self.q_table = {
            dst: {neighbor: 0.0 for neighbor in self.neighbors}
            for dst in self.network.graph
            if dst != self.id
        }

    def receive_packet(self, packet):
        self.queue.append(packet)

    def process(self):
        if not self.queue:
            return None

        packet = self.queue.popleft()

        if packet['dst'] == self.id:
            packet['delivered_at'] = self.network.time
            self.network.delivered_packets.append(packet)
            return None

        dst = packet['dst']
        next_hop = self.select_next_hop(dst)

        # Q-value update
        queue_delay = len(self.queue)
        neighbor_estimate = self.network.nodes[next_hop].get_estimate(dst)
        old_q = self.q_table[dst][next_hop]
        updated_q = old_q + self.alpha * ((queue_delay + 1 + neighbor_estimate) - old_q)
        self.q_table[dst][next_hop] = updated_q

        return next_hop, packet

    def select_next_hop(self, dst):
        """Choose neighbor with the lowest estimated Q-value."""
        q_values = self.q_table.get(dst, {})
        return min(q_values, key=q_values.get)

    def get_estimate(self, dst):
        """Return estimated delivery time to dst from this node."""
        if dst == self.id:
            return 0.0
        return min(self.q_table.get(dst, {}).values(), default=float('inf'))
