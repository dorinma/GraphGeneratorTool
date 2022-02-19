import generator


def fully_random(num_vertices, num_edges, bi_directed):
    edges = generator.fully_random(num_vertices, num_edges)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    print("generator.fully_random")


def fully_connected_dense_graph(num_vertices):
    print("generator.fully_connected_dense_graph")


def fully_connected(num_vertices, num_edges=None):
    return 0


def change_to_bidirected(edges):
    return 0


def flow_network(num_vertices, source_vertex, sink_vertex, num_of_paths):
    return 0


def planar_connection(num_vertices, num_edges, max_value):
    return 0


def bipartite(num_vertices, num_edges, groupA, groupB):
    return 0


def write_to_file_gr(name, edges):
    return 0


def write_to_file_co(name, edges):
    return 0


def write_to_file(name, edges):
    return 0
