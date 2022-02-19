import generator

methods_options = ('Fully Random', 'Fully Connected Dense Graph', 'Fully Connected', 'Flow Network',
                   'Planar Connection', 'Grid Connection', 'Bipartite Graph')
weights_options = ('Fully Random', 'Planar', 'Other Calculation')
# queries_options = ('Random', 'All Pairs', 'Minimal Edges')

def temp_testing(num_vertices, bi_directed):
    edges = generator.fully_connected_dense_graph(num_vertices)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    edges = generator.weights_to_edges_index_diff(edges, num_vertices, 100, 200)
    str_edges = generator.gr_input_toString(num_vertices, edges)
    generator.write_to_file_gr("test", str_edges)
    print("TESTING")


def generate_fully_random_graph(vertices, bi_directed, edges_number, edges_weights_method, min_e_val, max_e_val,
                                dest_directory):
    edges = fully_random(vertices, edges_number, bi_directed)
    weighted_edges = generate_edges_weights(vertices, edges, edges_weights_method, min_e_val, max_e_val)
    generator.write_to_file_gr(dest_directory + "/tmp", generator.gr_input_toString(vertices, weighted_edges))


def generate_edges_weights(vertices, edges, method, min_e_val, max_e_val):
    if method == weights_options[0]:    # Fully Random
        return generator.weights_to_edges_random(edges, min_e_val, max_e_val)
    # elif method == weights_options[1]:  # Planar
    #     return generator.weights_to_edges_planar(edges, min_e_val, max_e_val)
    else:   # Other calculation
        return generator.weights_to_edges_index_diff(edges, vertices, min_e_val, max_e_val)


def fully_random(num_vertices, num_edges, bi_directed):
    edges = generator.fully_random(num_vertices, num_edges)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    return edges
    # print("generator.fully_random")


def fully_connected_dense_graph(num_vertices, bi_directed):
    edges = generator.fully_connected_dense_graph(num_vertices)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    return edges
    # print("generator.fully_connected_dense_graph")


def fully_connected(num_vertices, bi_directed, num_edges=None):
    edges = generator.fully_connected(num_vertices)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    return edges


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
