import sys


class Graph:
    def __init__(self, edge):
        self.graph = {}
        self.edge = edge

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
            self.graph[vertex_a] = {vertex_b}
        else:
            vertex_a_edges = self.graph[vertex_a]
            if vertex_b not in vertex_a_edges:
                vertex_a_edges.add(vertex_b)
        if vertex_b not in self.graph:
            self.graph[vertex_b] = {vertex_a}
        else:
            vertex_b_edges = self.graph[vertex_b]
            if vertex_a not in vertex_b_edges:
                vertex_b_edges.add(vertex_a)

    def removeEdge(self, edge):
        vertex_a = edge[0]
        vertex_b = edge[1]

        self.graph[vertex_a].remove(vertex_b)
        self.graph[vertex_b].remove(vertex_a)

    def addEdge(self, edge):
        vertex_a = edge[0]
        vertex_b = edge[1]

        self.graph[vertex_a].add(vertex_b)
        self.graph[vertex_b].add(vertex_a)

    def explore(self):
        allPath = []
        explored = set()
        for vertex in self.graph:
            if vertex not in explored:
                pathSet = self.path(vertex)
                allPath.append(pathSet)
                for v in pathSet:
                    explored.add(v)
        return allPath

    def path(self, root, explored=None):
        if explored is None:
            explored = set()

        path = set()
        if root not in explored:
            explored.add(root)
            path.add(root)
            neighbors = self.graph[root]
            for neighbor in neighbors:
                if neighbor not in explored:
                    subSet = self.path(neighbor, explored)
                    for subVertex in subSet:
                        path.add(subVertex)
        return path


def build(edge):
    graph = Graph(edge)
    for pair in edge:
        vertex_a, vertex_b = pair
        graph.add(vertex_a, vertex_b)
    return graph


def parse(fileName):
    res = []
    with open(fileName, "r") as fp:
        for line in fp:
            line = line.replace(" ", "").replace("\n", "")
            res.append(line.split(","))
    return res


def bridge(graph):
    res = []
    originalPath = graph.explore()
    for edge in graph.edge:
        graph.removeEdge(edge)
        newPath = graph.explore()
        if originalPath != newPath:
            res.append(edge)
        graph.addEdge(edge)
    return res


def printBridges(bridges):
    if len(bridges) == 0:
        print("Contains no bridges.")
    else:
        print(f"Contains {len(bridges)} bridge(s):")

    numLst = [[int(bridgeNum[0]), int(bridgeNum[1])] for bridgeNum in bridges]
    for num in numLst:
        num.sort()
    numLst.sort()

    for bridge in numLst:
        print(f"{str(bridge[0])}, {str(bridge[1])}")


if __name__ == "__main__":
    fileName = sys.argv[1]
    edges = parse(fileName)
    graph = build(edges)
    bridges = bridge(graph)
    printBridges(bridges)


