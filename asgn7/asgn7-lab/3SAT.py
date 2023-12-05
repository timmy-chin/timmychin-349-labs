import sys

import graph, vertex_cover as vc


def getProposition(fileName):
    fp = open(fileName, "r")
    return fp.readline().replace("\n", "")


def groupClause(proposition):
    proposition = proposition.replace("(", "").replace(")", "").replace(" ", "")
    clauses = proposition.split("&")
    for i in range(len(clauses)):
        clauses[i] = clauses[i].split("|")
    return clauses


def makeGraph(clauses):
    G = graph.Graph()
    makeVertex(clauses, G)
    makeEdge(clauses, G)
    return G


def makeVertex(clauses, G):
    for i, clause in enumerate(clauses):
        for j, literal in enumerate(clause):
            graph.add_vertex(G, f"{literal}{i}{j}")


def makeEdge(clauses, G):
    for i, clause in enumerate(clauses):
        for j, literal in enumerate(clause):
            makeConnection(G, clauses, literal, i, j)


def makeConnection(G, clauses, literalA, i, j):
    vertexA = f"{literalA}{i}{j}"
    for x, clause in enumerate(clauses):
        for y, literalB in enumerate(clause):
            if i == x and j == y:  # same literal
                continue
            if i == x:  # in the same clause
                vertexB = f"{literalB}{x}{y}"
                graph.add_edge(G, vertexA, vertexB)
            elif "~" + literalA == literalB or literalA == "~" + literalB:  # is the negation
                vertexB = f"{literalB}{x}{y}"
                graph.add_edge(G, vertexA, vertexB)


def getVertexCover(G, clauses):
    V = len(clauses) * 3
    k = V - len(clauses)
    cover = vc.vertex_cover(G, k)
    return cover


def findExcluded(G, cover):
    excluded = []
    for vertex in G.matrix:
        if vertex not in cover:
            excluded.append(vertex)
    return excluded


def customSort(item):
    return item.replace("~", "")


def removeNumber(vertices):
    for i, vertex in enumerate(vertices):
        vertex_lst = list(vertex)
        while True:
            if vertex_lst and vertex_lst[-1].isdigit():
                vertex_lst.pop(-1)
            else:
                break
        vertices[i] = "".join(vertex_lst)


def printResult(G, cover):
    if cover is None:
        print("No satisfying assignments.")
    else:
        excluded = findExcluded(G, cover)
        excluded = sorted(excluded, key=customSort)
        removeNumber(excluded)
        print("Satisfying assignment:")
        print(", ".join(excluded))


def main(fileName):
    proposition = getProposition(fileName)
    clauses = groupClause(proposition)
    G = makeGraph(clauses)
    cover = getVertexCover(G, clauses)
    printResult(G, cover)


if __name__ == "__main__":
    main(sys.argv[1])
