import fractions
import random

NUM_VERTICES = 100
NUM_EDGES = 500
IS_DIRECTED = False
IS_RND_VERTICES_DISTANCE = True
MIN_VALUE = 50
MAX_VALUE = 200


class Edge:
    u = -1
    v = -1

    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __eq__(self, other):
        return self.u == other.u and self.v == other.v

    def __hash__(self):
        return hash(self.u + self.v)

    def __repr__(self):
        return '<Edge {}>'.format(self.u, self.v)


class EdgeWithValue:
    u = -1
    v = -1
    weight = -1

    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight

    def __eq__(self, other):
        return self.u == other.u and self.v == other.v

    def __hash__(self):
        return hash(self.u + self.v)

    def __repr__(self):
        return '<EdgeWithValue {}>'.format(self.u, self.v)


def fully_random(num_vertices, num_edges):
    edges = set()
    bias = fractions.Fraction(num_edges, num_vertices * (num_vertices - 1))
    while len(edges) != num_edges:
        for i in range(1, num_vertices + 1):
            for j in range(1, num_vertices + 1):
                if i != j and random.random() < bias and len(edges) != num_edges:
                    edges.add(Edge(i, j))
    return edges


def fully_connected_dense_graph(num_vertices):
    edges = set()
    for i in range(1, num_vertices + 1):
        for j in range(1, num_vertices + 1):
            if i != j:
                edges.add(Edge(i, j))
    return edges


def fully_connected(num_vertices, num_edges=None):
    edges = set()
    vertices = random.sample(range(1, num_vertices + 1), num_vertices)
    for i in range(0, (len(vertices) - 1)):
        edges.add(Edge(vertices[i], vertices[i+1]))
        edges.add(Edge(vertices[i+1], vertices[i]))
    num_of_edges = len(edges)
    if num_edges is not None:
        bias = fractions.Fraction(num_edges, num_vertices * num_vertices)
        while len(edges) != num_edges + num_of_edges:
            for i in range(1, num_vertices + 1):
                for j in range(1, num_vertices + 1):
                    if i != j and random.random() < bias and len(edges) != num_edges + num_of_edges:
                        edges.add(Edge(i, j))
    return edges


def change_to_bidirected(edges):
    new_edges = set()
    for edge in edges:
        new_edges.add(Edge(edge.v, edge.u))
        new_edges.add(Edge(edge.u, edge.v))
    return new_edges


def flow_network(num_vertices, source_vertex, sink_vertex, num_of_paths):
    edges = set()
    for i in range(0, num_of_paths):
        path_length = random.randint(0, num_vertices - 3)
        vertices = random.sample(range(1, num_vertices), path_length)
        for k in range(0, len(vertices) - 1):
            if k == 0 and vertices[k] != source_vertex:
                edges.add(Edge(source_vertex, vertices[k]))
            elif k == len(vertices) - 1 and vertices[k] != sink_vertex:
                edges.add(Edge(vertices[k], sink_vertex))
            else:
                edges.add(Edge(vertices[k], vertices[k + 1]))
    return edges


def bipartite(num_vertices, num_edges, groupA, groupB):
    groupA = (groupA * num_vertices) // (groupA + groupB)
    groupB = num_vertices - groupA
    groupA_ver = random.sample(range(1, num_vertices + 1), groupA)
    all_ver = list(range(1, num_vertices))
    groupB_ver = []
    for v in all_ver:
        if v not in groupA_ver:
            groupB_ver.append(v)
    edges = set()
    while len(edges) != num_edges:
        edges.add(Edge(groupA_ver[random.randint(0, groupA)], groupB_ver[random.randint(0, groupB)]))
    return edges


def weights_to_edges_random(edges, min_value, max_value):
    weighted_edges = set()
    for edge in edges:
        value = random.randint(min_value,max_value)
        weighted_edges.add(EdgeWithValue(edge.u,edge.v,value))
    return weighted_edges


def weights_to_edges_planar_connection(edges, min_value, max_value):
    if min_value <= max_value // 2:
        min_value = max_value // 2
    max_value -= 2
    weighted_edges = set()
    for edge in edges:
        value = random.randint(min_value, max_value)
        weighted_edges.add(EdgeWithValue(edge.u, edge.v, value))
    return weighted_edges


def weights_to_edges_index_diff(edges, num_vertices, min_value, max_value):
    weighted_edges = set()
    for edge in edges:
        weight_for_one_diff = (max_value - min_value) // num_vertices
        value = min_value + abs(edge.u - edge.v)*weight_for_one_diff
        weighted_edges.add(EdgeWithValue(edge.u, edge.v, value))
    return weighted_edges


def query_random(num_vertices, num_pairs):
    query = set()
    while len(query) != num_pairs:
        pair = random.sample(range(1, num_vertices + 1), 2)
        query.add(tuple(pair))
    return query


def query_all_vertices_pairs(num_vertices):
    query = set()
    for i in range(1,num_vertices + 1):
        for j in range(1, num_vertices + 1):
            if i != j:
                query.add(tuple[i, j])
    return query


def query_toString(pairs):
    output = []
    for pair in pairs:
        output.append(str(pair[0]) + ", " + str(pair[1]))
    return output




def gr_input_toString(num_vertices, edges):
    output = ["c\tCreated in graph generator tool by Shahar Bardugo & Dorin Matzrafi\n", "c\n",
              "c\tgraph contains " + str(num_vertices) + " nodes and " + str(len(edges)) + " arcs\n", "c\n"]
    for edge in edges:
        output.append("a\t" + str(edge.u) + "\t" + str(edge.v) + "\t" + str(edge.weight) + "\n")
    return output


def write_to_file_gr(name, edges):
    file1 = open(name + ".gr", 'w')
    file1.writelines(edges)
    file1.close()


def write_to_file_co(name, edges):
    file1 = open(name + '.co', 'w')
    file1.writelines(edges)
    file1.close()


def write_to_file(name, edges):
    file1 = open(name, 'w')
    file1.writelines(edges)
    file1.close()

