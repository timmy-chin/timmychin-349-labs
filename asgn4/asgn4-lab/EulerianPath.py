import sys


class Graph:
    def __init__(self, edge):
        self.graph = {}
        self.InDeg = {}
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
            self.graph[vertex_b] = set()

    def removeEdge(self, edge):
        vertex_b = edge[1]
        self.InDeg[vertex_b] -= 1

    def findInDeg(self):
        for source_vertex in self.graph:
            self.InDeg[source_vertex] = 0
            for other_vertex in self.graph:
                if other_vertex == source_vertex:
                    continue
                other_edges = self.graph[other_vertex]
                if source_vertex in other_edges:
                    self.InDeg[source_vertex] = self.InDeg.get(source_vertex, 0) + 1

    def getOutDeg(self, vertex_a):
        return len(self.graph[vertex_a])

    def getInDeg(self, vertex_a):
        return self.InDeg[vertex_a]


def build(edge):
    graph = Graph(edge)
    for pair in edge:
        vertex_a, vertex_b = pair
        graph.add(vertex_a, vertex_b)
    graph.findInDeg()
    return graph


def parse(fileName):
    res = []
    with open(fileName, "r") as fp:
        for line in fp:
            line = line.replace(" ", "").replace("\n", "")
            res.append(line.split(","))
    return res


def isOdd(num):
    return num % 2 != 0


def isEven(num):
    return num % 2 == 0


def validateEulerian(graph: Graph):
    # s = t
    if len(graph.graph) == 1:
        for vertex in graph.graph:
            return vertex, vertex

    s_vertice = []
    t_vertice = []

    for vertex in graph.graph:
        inDeg = graph.getInDeg(vertex)
        outDeg = graph.getOutDeg(vertex)
        if inDeg < outDeg:
            s_vertice.append(vertex)
        elif inDeg > outDeg:
            t_vertice.append(vertex)

    # all even, cycle found
    if len(s_vertice) == 0 and len(t_vertice) == 0:
        return True

    # found s and t
    elif validateSTVertices(graph, s_vertice, t_vertice):
        return s_vertice[0], t_vertice[0]

    else:
        return False


def validateSTVertices(graph: Graph, s_vertices, t_vertices):
    if len(s_vertices) == 1 and len(t_vertices) == 1:
        s_inDeg = graph.getInDeg(s_vertices[0])
        s_outDeg = graph.getOutDeg(s_vertices[0])
        t_inDeg = graph.getInDeg(t_vertices[0])
        t_outDeg = graph.getOutDeg(t_vertices[0])

        return s_inDeg + 1 == s_outDeg and t_inDeg == t_outDeg + 1

    return False


def EulerianPath(graph: Graph, s_vertex, t_vertex):
    if graph.getInDeg(s_vertex) == 0 and graph.getOutDeg(s_vertex) == 0:
        return s_vertex

    neighbors = graph.graph[s_vertex]
    if len(neighbors) > 0:
        v_vertex = neighbors.pop()
        graph.removeEdge((s_vertex, v_vertex))
        path = EulerianPath(graph, v_vertex, t_vertex)
        if graph.getInDeg(s_vertex) == 0 and graph.getOutDeg(s_vertex) == 0:
            return f"{s_vertex}, {path}"
        else:
            return EulerianPath(graph, s_vertex, s_vertex) + ", " + path


def printEulerianPath(graph: Graph):
    res = validateEulerian(graph)
    if res == True:
        print("Directed Eulerian cycle:")
        print(EulerianPath(graph, "0", "0"))
    elif not res:
        print("No directed Eulerian paths or cycles.")
    else:
        s_vertex, t_vertex = res
        print("Directed Eulerian path:")
        print(EulerianPath(graph, s_vertex, t_vertex))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify a file")
    else:
        fileName = sys.argv[1]
        edges = parse(fileName)
        graph = build(edges)
        printEulerianPath(graph)
