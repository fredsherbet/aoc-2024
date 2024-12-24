from collections import defaultdict

class Graph:
    def __init__(self):
        self.connections = set()
        self.nodes = defaultdict(set)

    def add(self, a, b):
        if a > b:
            a,b = b,a
        self.connections.add((a,b))
        self.nodes[a].add(b)
        self.nodes[b].add(a)


# This is union-find,  which isn't actually useful (because we're looking for fully-connected parties)
    def find_biggest_party(self):
        # Every computer is in its own LAN party, owned by itself, with a size of 1
        self.party_count = len(self.nodes)
        self.party_owner = list(range(self.party_count))
        self.party_size = [1] * self.party_count


    def find_owner(self, a):
        owner = self.party_owner[a]
        if a == owner:
            return owner
        owner = self.find_owner(owner)
        self.party_owner[a] = owner
        return owner

    def link(self, a, b):
        a_owner = self.find_owner(a)
        b_owner = self.find_owner(b)
        if a_owner == b_owner:
            # Already partying
            return False
        # Merge in the smaller party to the bigger party
        if self.party_size[a_owner] < self.party_size[b_owner]:
            a_owner, b_owner = b_owner, a_owner
        self.cluster_owner[b_owner] = a_owner
        self.cluster_size[a_owner] += self.cluster_size[b_owner]
        self.party_count -= 1
        return True


graph = Graph()

with open('input') as input:
    for l in input:
        a,b = l.strip().split('-')
        graph.add(a, b)

# We're looking for the largest fully connected cluster.

# Build a set of all the fully connected clusters, adding in a node (and its connections to known nodes) one at a time

parties = set()
for n, connections in graph.nodes.items():
    print(f"Adding node {n}")
    parties.add(tuple([n]))
    for p in list(parties):
        #print(f"Is {n} fully connected to {p}? Has connections {connections}")
        if all(c in connections for c in p):
            print(f"{n} is fully connected to party {p}")
            parties.add(p + tuple([n]))

#print("\n".join(str(p) for p in parties))
print(max(len(p) for p in parties))
print(",".join(sorted(max(parties, key=lambda p:len(p)))))
