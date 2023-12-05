# Naively brute forces the (Decision) Vertex Cover Problem.
# CSC 349, Assignment 7
# Given code, Fall '21
# NOTE: Do not alter this file.


import sys
import itertools
import graph


def vertex_cover(graph_g, k):
    """
    Find a vertex cover of a graph.
    :param graph_g: A graph to be covered
    :param k: A desired cardinality of a vertex cover
    :return: A vertex cover on that many vertices, or None if none exist
    """
    for subset in itertools.combinations(graph_g, k):
        if _is_cover(graph_g, subset):
            return subset

    return None


def _is_cover(graph_g, vertices):
    """
    Determine if a subset of vertices covers a graph.
    :param graph_g: A graph to be covered
    :param vertices: A subset of the graph's vertices
    :return: True if the vertices cover the graph's edges, False otherwise
    """
    for vertex_u in graph_g:
        for vertex_v in graph_g[vertex_u]:
            if vertex_u not in vertices and vertex_v not in vertices:
                return False

    return True


def main(argv):
    with open(argv[1], "r") as graph_file:
        k = int(graph_file.readline())
        graph_g = graph.read_graph(graph_file)

    cover = vertex_cover(graph_g, k)

    if cover is not None:
        print("Vertex cover on %d vertices:" % k)
        print(", ".join(sorted(cover)))
        return 0
    else:
        print("No vertex cover on %d vertices." % k)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
