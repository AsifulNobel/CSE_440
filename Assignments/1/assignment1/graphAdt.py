#!/usr/bin/env python3

class Graph:
    class Vertex:
        __slots__ = '_element'

        def __init__(self, x):
            self._element = x

        def element(self):
            return self._element

    class Edge:
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, u, v, x):
            self._origin = u
            self._destination = v
            self._element = x

        def endpoints(self):
            return (self._origin, self._destination)

        def opposite(self, v):
            return self._destination if v is self._origin else self._origin

        def element(self):
            return self._element


    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        return self._incoming is not self._outgoing

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()

    def get_vertex(self, x):
        verticeElements = [vertex for vertex in self.vertices()]

        for elem in verticeElements:
            if x == elem.element():
                return elem

        return None

    def edge_count(self):
        total = sum(len(self._outgoing[v]) for v in self._outgoing)

        # return total if self.is_directed() else total // 2
        return total

    def edges(self):
        result = set()

        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())

        return result

    def get_edge(self, u, v):
        return self._outgoing[u].get(v) if self._outgoing[u].get(v) else None

    def degree(self, v, outgoing=True):
        adj = self._outgoing if outgoing else self._incoming

        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """Return all (outgoing) edges incident to vertex v in the graph."""

        adj = self._outgoing if outgoing else self._incoming

        # Returns the edges that have destination as u
        for edge in adj[v].values():
            yield edge

        # Returns the edges that have destination as v
        for vert1 in adj.keys():
            for vert2 in adj[vert1].keys():
                if vert2 is v:
                    yield adj[vert1][vert2]


    def insert_vertex(self, x=None):
        v = self.Vertex(x)

        self._outgoing[v] = {}

        if self.is_directed():
            self._incoming[v] = {}

        return v

    def insert_edge(self, u, v, x=None):
        e = self.Edge(u, v, x)

        self._outgoing[u][v] = e
        self._incoming[u][v] = e

        return e
