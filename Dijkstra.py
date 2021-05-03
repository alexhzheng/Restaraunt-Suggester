from queue import PriorityQueue
from Graph import Graph
class Dijkstra:
    def shortestPath(self, graph, src, tgt):
        queue = PriorityQueue()

        size = graph.getSize()

        dist = []
        parents = []
        discovered = []
        nodes = []
        for x in range(size):
            dist.append(1000000)
            parents.append(-1)
        dist[src] = 0
        for x in range(size):
            queue.put((dist[x], x))
        

        while not queue.empty():
            min = queue.get()
            u = min[1]
            discovered.append(u)
            for v in graph.outNeighbors(u):
                if dist[v] > dist[u] + int(graph.getWeight(u,v)):
                    dist[v] = dist[u] + int(graph.getWeight(u,v))
                    parents[v] = u

        
        if tgt in discovered:
            vert = tgt
            nodes.append(tgt)
            while not (vert == src) and not (parents[vert] == -1):
                nodes.append(parents[vert])
                vert = parents[vert]
            nodes.append(src)

        nodes.reverse()

        distance = 0
        for x in range (len(nodes)):
            if not x == (len(nodes) - 1) :
                distance = int(graph.getWeight(nodes[x], nodes [x+1]))

        return (nodes, distance)
