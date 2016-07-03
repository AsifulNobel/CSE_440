#!/usr/bin/env python3

from graphAdt import Graph
from priorityQueueAdt import AdaptableHeapPriorityQueue

def shortest_path_lengths(g, src, dest):
    """Compute shortest-path distances from src to reachable vertices of g until dest vertex is found.

    Graph g can be undirected or directed, but must be weighted such that e.element() returns a numeric weight for each edge e.

    Return dictionary mapping each reachable vertex to its distances from src.
    """

    d = {}                  # d[v] is upper bound distance from vertices s to v
    path = {}               # dictionary containing previous vertex object for shortest path
    cloud = {}              # visited map
    pq = AdaptableHeapPriorityQueue()   # vertex v will have key d[v]
    pqlocator = {}          # locator map from vertex to its pq queue

    # for each vertex v of the graph, add an entry to the priority
    # queue, with the source having distance 0 and all others
    # having infinite distance
    vertex_list = g.vertices()

    for v in vertex_list:
        if v is src:
            d[v] = 0
        else:
            d[v] = float('inf')
        path[v] = None
        pqlocator[v] = pq.add(d[v], v)

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key

        if u is dest:
            break

        del pqlocator[u]

        edge_list = g.incident_edges(u)

        for e in edge_list:
            v = e.opposite(u)

            if v not in cloud:
                wgt = e.element()

                if d[u] + wgt < d[v]:
                    d[v] = d[u] + wgt
                    path[v] = u
                    pq.update(pqlocator[v], d[v], v)

    return cloud, path

def shortest_path(g, org, dest):
    d, p = shortest_path_lengths(g, org, dest)
    path = []
    end = dest

    # Checks if shortest path distance of origin to destination is infinity.
    # If yes, then return that infinity value and no need to find a path
    if d[end] != float('inf'):
        while org is not dest:
            path.append(dest)

            dest = p[dest]

        path.append(org)
        path.reverse()

    return path, d[end]

def vertices_available(g, org, dest):
    vertices_list = g.vertices()
    found_count = 0

    for vertex in vertices_list:
        if vertex.element() == org or vertex.element() == dest:
            found_count += 1

    return found_count

def route_finder(fileName, org, dest):
    cityMap = Graph()
    inputEnd = 'END OF INPUT'

    with open(fileName, 'rb') as inpFile:

        for line in inpFile:
            line = line.strip().decode('utf-8')

            if line != inputEnd:
                lineElems = line.split()

                if len(lineElems) >= 3:
                    v1 = cityMap.get_vertex(lineElems[0])
                    v2 = cityMap.get_vertex(lineElems[1])
                    c1 = v1 if v1 else cityMap.insert_vertex(lineElems[0])
                    c2 = v2 if v2 else cityMap.insert_vertex(lineElems[1])
                    cityMap.insert_edge(c1, c2, int(lineElems[2]))


    vertices_found = vertices_available(cityMap, org, dest)

    if vertices_found == 2:
        path, distance = shortest_path(cityMap, cityMap.get_vertex(org), cityMap.get_vertex(dest))

        path_size = len(path)

        print('\ndistance: ', distance, ' km')
        print('route:')

        if path_size > 1:
            counter = zip(range(0, len(path)-1), range(1, len(path)))
            for c1, c2 in counter:
                d = cityMap.get_edge(path[c1], path[c2]) if cityMap.get_edge(path[c1], path[c2]) else cityMap.get_edge(path[c2], path[c1])
                print(path[c1].element(), 'to', path[c2].element(), '->', d.element(), 'km')
        else:
            print('none')
    elif vertices_found == 1 and org == dest:
        print('\ndistance: ', 0, ' km')
        print(org, 'to', dest, '->', 0, 'km')
    elif vertices_found == 1:
        print('Found only one vertex')
    else:
        print('Vertices not available')


if __name__ == '__main__':
    import sys

    route_finder(sys.argv[1], sys.argv[2], sys.argv[3])
