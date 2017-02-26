import networkx as nx
import random
import pickle as pk

class BAGraph(nx.Graph):

    def __init__(self, m, N):
        if m < 1 or m >= N:
            raise nx.NetworkXError("Barabási–Albert network must have m >= 1"
                                   " and m < n, m = %d, n = %d" % (m, N))
        # start with m initial nodes
        super().__init__(data=nx.empty_graph(m))
        self.m = m
        self.N = N
        self.targets = self.nodes()
        self.repeated_nodes = []
        self.increment()

    def set_targets(self, m):
        # pick uniformly from repeated_nodes (preferential attachment
        self.targets = BAGraph._random_subset(self.repeated_nodes, m)

    def increment(self):
        current = self.m
        while current < self.N:
            self.add_edges_from(zip([current] * self.m, self.targets))
            # Add one node to the list for each new edge just created.
            self.repeated_nodes.extend(self.targets)
            # And the new node "current" has m edges to add to the list.
            self.repeated_nodes.extend([current] * self.m)
            # Now choose m unique nodes from the existing nodes
            self.set_targets(self.m)
            current += 1

    def save_to_file(self, name=None):
        if not name:
            fn = 'data/phase1/ba_{0}_m{1}.pkl'.format(str(self.number_of_nodes()), str(self.m))
        else:
            fn = 'data/phase1/{0}_{1}_m{2}.pkl'.format(str(name), str(self.number_of_nodes()), str(self.m))
        with open(fn, 'wb') as file:
            pk.dump(self, file)

    @staticmethod
    def load_from_file(N, m, name=None):
        if not name:
            name = 'ba'
        fn = 'data/phase1/{0}_{1}_m{2}.pkl'.format(str(name), str(N), str(m))
        with open(fn, 'rb') as file:
            return pk.load(file)

    @staticmethod
    def _random_subset(seq, m):
        """ Return m unique elements from seq.

        This differs from random.sample which can return repeated
        elements if seq holds repeated elements.
        """
        targets = set()
        while len(targets) < m:
            x = random.choice(seq)
            targets.add(x)
        return targets

class RandomAttachmentGraph(BAGraph):
    def __init__(self, m, N):
        super().__init__(m, N)

    def set_targets(self):
        return

    def save_to_file(self, name=None):
        if not name:
            fn = 'data/phase1/ra_{0}_m{1}.pkl'.format(str(self.number_of_nodes()), str(self.m))
        else:
            fn = 'data/phase1/{0}_{1}_m{2}.pkl'.format(str(name), str(self.number_of_nodes()), str(self.m))
        with open(fn, 'wb') as file:
            pk.dump(self, file)

    @staticmethod
    def load_from_file(N, m, name=None):
        if not name:
            name = 'ra'
        fn = 'data/phase1/{0}_{1}_m{2}.pkl'.format(str(name), str(N), str(m))
        with open(fn, 'rb') as file:
            return pk.load(file)