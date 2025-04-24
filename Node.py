import random
from collections import deque

class Node:
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
        next_hop = random.choice(self.neighbors) 
        return next_hop, packet