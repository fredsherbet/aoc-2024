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


graph = Graph()

with open('input') as input:
    for l in input:
        a,b = l.strip().split('-')
        graph.add(a, b)

triples = set()
for a,b in graph.connections:
    if not (a.startswith('t') or b.startswith('t')):
        continue
    for c in graph.nodes[a]:
        if c in graph.nodes[b]:
            triples.add(tuple(sorted((a,b,c))))

print("\n".join(sorted(str(t) for t in triples)))

