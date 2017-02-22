import networkx as nx
import random

class BAGraph(nx.Graph):

    def __init__(self, m, N):
        super().__init__()
        self.m = m
        self.N = N

        # start with 2 nodes and one edge connecting them
        self.add_nodes_from([0, 1])
        self.add_edge(0, 1)

    def add_next_node(self):
        node = max(self.nodes()) + 1
        self.add_node(node)
        return node

    def _check_all_connected(self, node):
        nbs = self.neighbors(node)
        not_connected = set(self.nodes()) - set(nbs)
        if len(not_connected) == 1 and list(not_connected)[0] == node:
            return True
        else:
            return False

    def add_m_edges(self, m):
        edges_added = 0

        # check that current node is not already connected to everything
        while edges_added < m and not self._check_all_connected(self.nodes()[-1]):
            new_node = self.nodes()[-1]
            existing_node = self.choose_node()

            # do not add self loops
            if new_node == existing_node:
                continue

            # there is already an edge between these 2 nodes
            if new_node in self.neighbors(existing_node):
                continue

            else:
                self.add_edge(new_node, existing_node)
                edges_added += 1

    def increment(self, t, m=None):
        if m == None:
            m = self.m
        for i in range(t):
            self.add_next_node()
            self.add_m_edges(m)

    def increment_till_max(self):
        self.increment_till_n(self.N)

    def increment_till_n(self, n):
        remaining = n - len(self.nodes())
        if remaining < 0:
            raise ValueError("You are already past the max number of nodes!")
        self.increment(remaining)

    def choose_node(self):
        end = len(self.edges()) - 1
        index = random.randint(0, end)
        edge = self.edges()[index]
        node = edge[0] if random.random() < 0.5 else edge[1]
        return node
