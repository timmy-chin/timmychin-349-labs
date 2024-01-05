# Represents an undirected, weighted graph.
# CSC 349, Assignment 8
# Given code, Fall '19
# NOTE: Do not alter this file.


class WeightedGraph:
    """ A collection of vertices connected by weighted edges """

    def __init__(self, vertices = []):
        # The backing adjacency dictionary:
        self.matrix = {vertex: {} for vertex in vertices}

    def __eq__(self, other):
        return type(other) == WeightedGraph and self.matrix == other.matrix

    def __repr__(self):
        return "WeightedGraph({\n    %s\n})" % ",\n    ".join(
                ["%s: %s" % (repr(v), repr(self[v])) for v in self])

    def __len__(self):
        return len(self.matrix)

    def __iter__(self):
        return iter(self.matrix)

    def __contains__(self, item):
        return item in self.matrix

    def __getitem__(self, key):
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value


def add_vertex(graph, vertex):
    """
    Add a vertex to a graph, if it does not exist.
    :param graph: A graph to which to add a vertex
    :param vertex: The vertex to be added
    :return: The vertex's adjacency dictionary
    """
    return graph.matrix.setdefault(vertex, {})


def add_edge(graph, vertex_u, vertex_v, weight):
    """
    Add an edge to a graph, adding vertices first if they do not exist.
    :param graph: A graph to which to add an edge
    :param vertex_u: The edge's first endpoint
    :param vertex_v: The edge's second endpoint
    :param weight: The weight of the edge
    :return: The resulting graph
    """
    add_vertex(graph, vertex_u)[vertex_v] = weight
    add_vertex(graph, vertex_v)[vertex_u] = weight
    return graph


def remove_vertex(graph, vertex):
    """
    Remove a vertex from a graph if it exists, along with all incident edges.
    :param graph: A graph from which to remove a vertex
    :param vertex: The vertex to be removed
    :return: The vertex's former adjacency set
    """
    for neighbor in graph.matrix.get(vertex, {}):
        graph.matrix.get(neighbor, {}).pop(vertex, None)

    return graph.matrix.pop(vertex, {})


def remove_edge(graph, vertex_u, vertex_v):
    """
    Remove an edge from a graph if it exists
    :param graph: A graph from which to remove an edge
    :param vertex_u: The edge's first endpoint
    :param vertex_v: The edge's second endpoint
    :return: The resulting graph
    """
    graph.matrix.get(vertex_u, {}).pop(vertex_v, None)
    graph.matrix.get(vertex_v, {}).pop(vertex_u, None)
    return graph


def read_graph(graph_file):
    """
    Read a graph from a file.
    :param graph_file: An open file containing an edge list
    :return: The corresponding new graph
    """
    graph = WeightedGraph()
    for u, v, w in map(lambda e: e.split(","), graph_file):
        add_edge(graph, u.strip(), v.strip(), int(w))

    return graph
