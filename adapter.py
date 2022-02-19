import generator

methods_options = ('Fully Random', 'Fully Connected Dense Graph', 'Fully Connected', 'Flow Network',
                   'Planar Connection', 'Grid Connection', 'Bipartite Graph')
weights_options = ('Fully Random', 'Planar', 'Other Calculation')
# queries_options = ('Random', 'All Pairs', 'Minimal Edges')


def generate_edges_weights(vertices, edges, method, min_e_val, max_e_val):
    if method == weights_options[0]:    # Fully Random
        return generator.weights_to_edges_random(edges, min_e_val, max_e_val)
    # elif method == weights_options[1]:  # Planar
    #     return generator.weights_to_edges_planar(edges, min_e_val, max_e_val)
    else:   # Other calculation
        return generator.weights_to_edges_index_diff(edges, vertices, min_e_val, max_e_val)


def generate_fully_random_graph(vertices, min_e_val, max_e_val, bi_directed, dest_directory, edges_weights_method,
                                edges_number):
    edges = fully_random(vertices, edges_number, bi_directed)
    weighted_edges = generate_edges_weights(vertices, edges, edges_weights_method, min_e_val, max_e_val)
    generator.write_to_file_gr(dest_directory + "tmp", generator.gr_input_toString(vertices, weighted_edges))


def generate_fully_connected_dense_graph(vertices, min_e_val, max_e_val, bi_directed, dest_directory,
                                         edges_weights_method):
    edges = fully_connected_dense_graph(vertices, bi_directed)
    weighted_edges = generate_edges_weights(vertices, edges, edges_weights_method, min_e_val, max_e_val)
    generator.write_to_file_gr(dest_directory + "tmp", generator.gr_input_toString(vertices, weighted_edges))


def generate_fully_connected_graph(vertices, min_e_val, max_e_val, bi_directed, dest_directory, edges_weights_method,
                                   edges_number):
    if edges_number == -1:
        edges = fully_connected(vertices, bi_directed, None)
    else:
        edges = fully_connected(vertices, bi_directed, edges_number)
    weighted_edges = generate_edges_weights(vertices, edges, edges_weights_method, min_e_val, max_e_val)
    generator.write_to_file_gr(dest_directory + "tmp", generator.gr_input_toString(vertices, weighted_edges))


def generate_flow_network(vertices, min_e_val, max_e_val, bi_directed, dest_directory, edges_weights_method,
                          source_vertex, sink_vertex, num_of_paths):
    edges = flow_network(vertices, bi_directed, source_vertex, sink_vertex, num_of_paths)
    weighted_edges = generate_edges_weights(vertices, edges, edges_weights_method, min_e_val, max_e_val)
    generator.write_to_file_gr(dest_directory + "tmp", generator.gr_input_toString(vertices, weighted_edges))


def generate_bipartite_graph(vertices, min_e_val, max_e_val, bi_directed, dest_directory, edges_weights_method,
                             edges_number, rel1, rel2):
    edges = bipartite(vertices, bi_directed, edges_number, rel1, rel2)
    weighted_edges = generate_edges_weights(vertices, edges, edges_weights_method, min_e_val, max_e_val)
    generator.write_to_file_gr(dest_directory + "tmp", generator.gr_input_toString(vertices, weighted_edges))


def fully_random(num_vertices, num_edges, bi_directed):
    edges = generator.fully_random(num_vertices, num_edges)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    return edges


def fully_connected_dense_graph(num_vertices, bi_directed):
    edges = generator.fully_connected_dense_graph(num_vertices)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    return edges


def fully_connected(num_vertices, bi_directed, num_edges):
    edges = generator.fully_connected(num_vertices, num_edges)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    return edges


def flow_network(num_vertices, bi_directed, source_vertex, sink_vertex, num_of_paths):
    edges = generator.flow_network(num_vertices, source_vertex, sink_vertex, num_of_paths)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    return edges


def planar_connection(num_vertices, num_edges, max_value):
    return 0


def bipartite(num_vertices, bi_directed, num_edges, group1, group2):
    edges = generator.bipartite(num_vertices, num_edges, group1, group2)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    return edges


def write_to_file_gr(name, edges):
    return 0


def write_to_file_co(name, edges):
    return 0


def write_to_file(name, edges):
    return 0
