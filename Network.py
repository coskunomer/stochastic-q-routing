import math
import random
from collections import defaultdict
from typing import Dict, List, Tuple, Type

Packet = Dict[str, object] 
Graph  = Dict[int, List[Tuple[int, float]]]

class Network:
    """
    Generic network simulator that delegates routing/learning
    to per‑node objects (BellmanFordNode, QNode, …).

    Each node class must expose:
        - __init__(node_id: int, neighbors: List[int], network: "Network")
        - receive_packet(packet: Packet) -> None
        - process() -> Optional[Tuple[int, Packet]]
          (returns (next_hop, packet) if it forwarded one this tick)
        - queue  (Iterable or list‑like storing its pending packets)
    """

    def __init__(self, graph: Graph, node_cls: Type):
        """
        Parameters
        ----------
        graph     : {node_id: [(neighbor_id, weight), ...], ...}
        node_cls  : class implementing the interface described above
        """
        self.time               = 0
        self.delivered_packets  : List[Packet] = []
        self.graph = graph
        self.nodes: Dict[int, object] = {
            nid: node_cls(nid, [nbr for nbr, _ in neigh], network=self)
            for nid, neigh in graph.items()
        }

    # ------------------------------------------------------------------
    # Packet‑injection helpers
    # ------------------------------------------------------------------
    def _new_packet(self, src: int, dst: int) -> Packet:
        return {
            "src":         src,
            "dst":         dst,
            "created_at":  self.time,
            "next_hop":    None,
            "delivered_at": None,
        }

    def inject_packet(self, src: int, dst: int) -> None:
        self.nodes[src].receive_packet(self._new_packet(src, dst))

    def inject_random_packets(self, load: float) -> None:
        """
        Poisson‑like traffic: expected `load` packets this tick
        (fractional part handled via Bernoulli trial).
        """
        n = int(math.floor(load))
        if random.random() < (load - n):
            n += 1

        node_ids = list(self.nodes.keys())
        for _ in range(n):
            src = random.choice(node_ids)
            dst = random.choice([v for v in node_ids if v != src])
            self.inject_packet(src, dst)

    # ------------------------------------------------------------------
    # Simulation step
    # ------------------------------------------------------------------
    def tick(self) -> None:
        """
        One time‑unit of network activity:
        1. Each node dequeues (at most) one packet and decides a next hop.
        2. Those packets are delivered to the next hop’s input queue.
        3. Global clock increments.
        """
        to_deliver: Dict[int, List[Packet]] = defaultdict(list)

        # 1. Processing
        for node in self.nodes.values():
            result = node.process()
            if result:
                next_hop, packet = result
                to_deliver[next_hop].append(packet)

        # 2. Delivery
        for nid, pkts in to_deliver.items():
            for p in pkts:
                self.nodes[nid].receive_packet(p)

        self.time += 1

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------
    def get_active_packets(self) -> int:
        return sum(len(getattr(n, "queue", [])) for n in self.nodes.values())

    def get_delivered_packets_count(self) -> int:
        return len(self.delivered_packets)