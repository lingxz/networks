import networkx as nx
import random
import pickle as pk
import json
import os

# this should not be instantiated directly
class BaseBAGraph(nx.Graph):

    prefix = 'base'

    def __init__(self, m, N, seed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m = m
        self.N = N
        self.targets = []
        if seed is not None:
            random.seed(seed)

    def _set_targets(self, current):
        pass

    def increment(self):
        current = self.m
        while current < self.N:
            self.add_edges_from(zip([current] * self.m, self.targets))
            # Add one node to the list for each new edge just created.
            self._set_targets(current)
            current += 1

    def save_degrees(self, folder=None, root_folder=None, name=None):
        if not name:
            name = self.prefix
        if not root_folder:
            root_folder = self.prefix
        if not folder:
            folder = "degree_distribution"
        folder_path = "data/{0}/{1}".format(root_folder, folder)
        os.makedirs(folder_path, exist_ok=True)
        fn = folder_path + '/{0}_{1}_m{2}.json'.format(str(name), str(self.number_of_nodes()), str(self.m))
        with open(fn, 'w') as f:
            json.dump(self.degree(), f)


    @classmethod
    def load_degrees(cls, N, m, folder=None, root_folder=None, name=None):
        if not name:
            name = cls.prefix
        if not root_folder:
            root_folder = cls.prefix
        if not folder:
            folder = "degree_distribution"
        folder_path = "data/{0}/{1}".format(root_folder, folder)
        fn = folder_path + '/{0}_{1}_m{2}.json'.format(str(name), str(N), str(m))
        with open(fn, 'r') as f:
            return json.load(f)

    def save_to_file(self, name=None, folder=None):
        if not name:
            name = self.prefix
        if not folder:
            folder = "phase1"
        folder_path = "data/" + folder
        os.makedirs(folder_path, exist_ok=True)
        fn = 'data/phase1/{0}_{1}_m{2}.pkl'.format(str(name), str(self.number_of_nodes()), str(self.m))
        with open(fn, 'wb') as file:
            pk.dump(self, file, protocol=pk.HIGHEST_PROTOCOL)

    @classmethod
    def load_from_file(cls, N, m, name=None):
        if not name:
            name = cls.prefix
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


class BAGraph(BaseBAGraph):
    prefix = 'ba'

    def __init__(self, m, N, seed=None):
        if m < 1 or m >= N:
            raise nx.NetworkXError("Barabási–Albert network must have m >= 1"
                                   " and m < n, m = %d, n = %d" % (m, N))
        # start with m initial nodes
        super().__init__(m, N, seed=seed, data=nx.empty_graph(m))
        self.targets = self.nodes()
        self.repeated_nodes = []
        self.increment()

    def _set_targets(self, current):
        m = self.m
        self.repeated_nodes.extend(self.targets)
        # And the new node "current" has m edges to add to the list.
        self.repeated_nodes.extend([current] * self.m)
        # Now choose m unique nodes from the existing nodes
        # pick uniformly from repeated_nodes (preferential attachment)
        self.targets = BAGraph._random_subset(self.repeated_nodes, m)


class RAGraph(BaseBAGraph):

    prefix = 'ra'

    def __init__(self, m, N):
        super().__init__(m, N)
        self.targets = self.nodes()

    def _set_targets(self):
        self.targets = random.sample(self.nodes(), self.m)
