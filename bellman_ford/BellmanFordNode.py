from collections import deque
from bellman_ford.routing_table import routing_tables

class BellmanFordNode:
    def __init__(self, node_id, neighbors, network):
        self.id = node_id
        self.neighbors = neighbors  
        self.queue = deque()
        self.network = network

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

        route = routing_tables.get(self.id, {}).get(packet['dst'])

        next_hop = route["next_hop"]
        return next_hop, packet
