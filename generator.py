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
        return '<Person {}>'.format(self.u, self.v)


def fully_random(num_vertices, num_edges):
    edges = set()
    bias = fractions.Fraction(num_edges, num_vertices * num_vertices)
    while len(edges) != num_edges:
        for i in range(1,num_vertices+1):
            for j in range(1,num_vertices+1):
                if i != j and random.random() < bias and len(edges) != num_edges:
                    edges.add(Edge(i, j))
    return edges


def fully_connected_dense_graph(num_vertices):
    edges = set()
    for i in range(1, num_vertices+1):
        for j in range(1, num_vertices+1):
            if i != j:
                edges.add(Edge(i, j))
    return edges


def fully_connected(num_vertices, num_edges = None):
    edges = set()
    for i in range(1,num_vertices):
        edges.append(Edge(i, i+1))
    if num_edges is not None and num_edges > len(edges):
        bias = fractions.Fraction(num_edges, num_vertices * num_vertices)
        while len(edges) != num_edges:
            for i in range(1, num_vertices + 1):
                for j in range(1, num_vertices + 1):
                    if i != j and random.random() < bias and len(edges) != num_edges:
                        edges.add(Edge(i, j))
    return edges


def change_to_bidirected(edges):
    new_edges = set()
    for edge in edges:
        new_edges.add(Edge(edge.v, edge.u))
        new_edges.add(Edge(edge.u, edge.v))
    return new_edges





def write_to_file_gr(name, edges):
    #f = open("myfile.gr", "x")
    try:
        file1 = open(name + '.gr', 'w')
        file1.writelines(edges)
        file1.close()
    except:
        print("error")

def write_to_file_co(name, edges):
    #f = open("myfile.gr", "x")
    try:
        file1 = open(name + '.co', 'w')
        file1.writelines(edges)
        file1.close()
    except:
        print("error")


def write_to_file(name, edges):
    #f = open("myfile.gr", "x")
    try:
        file1 = open(name, 'w')
        file1.writelines(edges)
        file1.close()
    except:
        print("error")
