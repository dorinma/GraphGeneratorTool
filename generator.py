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
    weight = -1

    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight

def gen_graph(num_vertices, num_edges):
    edges = []
    bias = fractions.Fraction(num_edges, num_vertices * num_vertices)
    print (bias)
    while num_edges != 0:
        for i in range(0,num_vertices):
            for j in range(0,num_vertices):
                if i!=j and random.random()<bias and num_edges > 0:
                    distance = random.randint(MIN_VALUE,MAX_VALUE)
                    edges.append(("a "+str(i)+"  "+str(j)+"  "+str(distance)+"\n")) #Edge(i,j,distance)
                    num_edges-=1
    return edges


def write_to_file_gr(edges):
    #f = open("myfile.gr", "x")
    file1 = open('myfile.gr', 'w')
    file1.writelines(edges)
    file1.close()

def write_to_file_co(edges):
    #f = open("myfile.gr", "x")
    file1 = open('myfile.co', 'w')
    file1.writelines(edges)
    file1.close()

def write_to_file(edges):
    #f = open("myfile.gr", "x")
    file1 = open('myfile', 'w')
    file1.writelines(edges)
    file1.close()
