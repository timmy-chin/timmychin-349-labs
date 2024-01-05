import sys
import weighted_graph as wg


def main(argv):
    fp = open(argv[1], "r")
    graph = wg.read_graph(fp)
    mst = getMST(graph)
    dfs_path = []
    dfs(mst, "0", dfs_path)
    path = getHamiltonianPath(dfs_path)
    weight = getHamiltonianWeight(path, graph)
    printResult(path, weight)


def getMST(graph):
    visited = set()
    node = (0, "0", "0")
    queue = [node]
    mst_edges = []

    while len(queue) != 0:
        current = getMin(queue)
        prev_vertex = current[2]
        vertex = current[1]
        if vertex not in visited:
            visited.add(vertex)
            mst_edges.append((prev_vertex, vertex))

            for neighbor in graph.matrix[vertex]:
                if neighbor not in visited:
                    newNode = (graph.matrix[vertex][neighbor], neighbor, vertex)
                    queue.append(newNode)
    mst_edges.remove(("0", "0"))
    return toTree(mst_edges)


def getMin(queue):
    queue.sort()
    return queue.pop(0)


def toTree(mst_edges):
    mst = {}
    for edge in mst_edges:
        vertex_a, vertex_b = edge

        mst[vertex_a] = []
        mst[vertex_b] = []

    for edge in mst_edges:
        vertex_a, vertex_b = edge

        mst[vertex_a].append(vertex_b)
        mst[vertex_a].sort()

    return mst


def dfs(tree, root, path):
    path.append(root)
    kids = tree[root]

    if len(kids) == 0:
        return

    for kid in kids:
        dfs(tree, kid, path)
        path.append(root)


def getHamiltonianPath(dfs_path):
    path = []
    for vertex in dfs_path:
        if vertex not in path:
            path.append(vertex)
    path.append(dfs_path[0])
    return path


def getHamiltonianWeight(path, graph):
    a = 0
    b = 1
    total_weight = 0

    while b < len(path):
        vertex_a = path[a]
        vertex_b = path[b]
        weight = graph[vertex_a][vertex_b]
        total_weight += weight

        a += 1
        b += 1

    return total_weight


def printResult(path, weight):
    string_path = ", ".join(path)
    result = f"Hamiltonian cycle of weight {weight}:\n{string_path}"
    print(result)


if __name__ == "__main__":
    main(sys.argv)
