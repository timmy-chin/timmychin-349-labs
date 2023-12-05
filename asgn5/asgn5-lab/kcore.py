import sys


class Graph:
    def __init__(self):
        self.graph = {}
        self.degree = {}

    def __repr__(self):
        res = ""
        for vertex in self.graph:
            res += vertex + " -> "
            edges = [vertex for vertex in self.graph[vertex]]
            res += edges.__repr__()
            res += "\n"
        return res

    def add(self, vertex_a, vertex_b):
        if vertex_a not in self.graph:
            self.graph[vertex_a] = [vertex_b]
        else:
            vertex_a_edges = self.graph[vertex_a]
            if vertex_b not in vertex_a_edges:
                vertex_a_edges.append(vertex_b)
        if vertex_b not in self.graph:
            self.graph[vertex_b] = [vertex_a]
        else:
            vertex_b_edges = self.graph[vertex_b]
            if vertex_a not in vertex_b_edges:
                vertex_b_edges.append(vertex_a)

    def calculateDegree(self):
        for vertex in self.graph:
            self.degree[vertex] = len(self.graph[vertex])

    def getDegree(self, vertex):
        return self.degree[vertex]

    def decreaseDegree(self, vertex, num):
        self.degree[vertex] = self.degree[vertex] - num

    def removeVertex(self, vertex):
        for other_vertex in self.graph:
            if vertex == other_vertex:
                continue
            if vertex in self.graph[other_vertex]:
                self.graph[other_vertex].remove(vertex)
        self.graph.pop(vertex)


def parse(fileName):
    res = []
    with open(fileName, "r") as fp:
        for line in fp:
            line = line.replace(" ", "").replace("\n", "")
            res.append(line.split(","))
    return res


def build(edge):
    graph = Graph()
    for pair in edge:
        vertex_a, vertex_b = pair
        graph.add(vertex_a, vertex_b)
    graph.calculateDegree()
    return graph


def kCore(graph, k):
    lowerThanK = ["not empty"]  # to hold all vertices that don't belong in k-core
    while len(lowerThanK) != 0:  # break when we don't find any vertex that don't belong in k-core
        lowerThanK = []  # initialize or reset the list to store vertices for removal

        for vertex in graph.graph:

            # get rid of all vertex that don't belong in k-core by reducing degree
            if graph.getDegree(vertex) < k:
                graph.decreaseDegree(vertex, 1)
                for neighbor in graph.graph[vertex]:
                    graph.decreaseDegree(neighbor, 1)

                lowerThanK.append(vertex)  # mark for removal from the graph

        for vertex in lowerThanK:  # remove the vertex so that only vertices that belong in k-core exist in the graph
            graph.removeVertex(vertex)

    k_core_vertex = [int(vertex) for vertex in graph.graph]  # whatever vertices left over belongs in k-core
    k_core_vertex.sort()
    k_core_vertex = [str(vertex) for vertex in k_core_vertex]  # whatever vertices left over belongs in k-core

    return k_core_vertex


def getAllKCores(graph):
    k = 1
    cores = kCore(graph, k)
    while len(cores) > 0: # if at any time cores is empty, we know higher cores cannot exist due to its nature
        printCores(cores, k)
        graph = build(edges)  # build the graph again since it got mutated before
        k += 1
        cores = kCore(graph, k)


def printCores(cores, k):
    print(f"Vertices in {k}-cores:")
    print(", ".join(cores))


if __name__ == "__main__":
    fileName = sys.argv[1]
    edges = parse(fileName)
    graph = build(edges)
    getAllKCores(graph)
