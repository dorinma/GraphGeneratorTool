import generator
import read_write_io
import time

weights_options = ('Fully Random', 'Planar', 'Predefined Calculation')
# methods_options = ('Fully Random', 'Fully Connected Dense Graph', 'Fully Connected', 'Flow Network',
#                    'Planar Connection', 'Grid Connection', 'Bipartite Graph')
# queries_options = ('Random', 'All Pairs', 'Minimal Edges')
FILE_NAME_GR = "graph_"
FILE_NAME_GRID = "grid_"
FILE_NAME_CO = "coordinates_"
FILE_NAME_Q_RND = "query_random_"
FILE_NAME_Q_ALL = "query_all_pairs_"
FILE_NAME_Q_MIN = "query_min_edges_"


def get_curr_time():
    return round(time.time() * 1000)


def generate_edges_weights(vertices, edges, method, min_e_val, max_e_val):
    if method == weights_options[0]:  # Fully Random
        return generator.weights_to_edges_random(edges, min_e_val, max_e_val)
    elif method == weights_options[1]:  # Planar
        return generator.weights_to_edges_planar_connection(edges, min_e_val, max_e_val)
    else:  # Predefined calculation
        return generator.weights_to_edges_index_diff(edges, vertices, min_e_val, max_e_val)


def generate_queries(vertices, edges, queries, dest_directory):
    time_stamp = str(get_curr_time())
    if queries[0] == 1:  # random
        read_write_io.write_to_file_query(dest_directory + FILE_NAME_Q_RND + time_stamp,
                                          generator.query_to_string(generator.query_random(vertices, queries[1])))
    if queries[2] == 1:  # all pairs
        read_write_io.write_to_file_query(dest_directory + FILE_NAME_Q_ALL + time_stamp,
                                          generator.query_to_string((generator.query_all_vertices_pairs(vertices))))
    if queries[3] == 1:  # min x edges
        read_write_io.write_to_file_query(dest_directory + FILE_NAME_Q_MIN + time_stamp,
                                          generator.query_to_string(
                                              (generator.query_pairs_at_least_x_edges(vertices, edges,
                                                                                      queries[4]))))
    if queries[5] == 1:  # min x paths
        read_write_io.write_to_file_query(dest_directory + FILE_NAME_Q_MIN + time_stamp,
                                          generator.query_to_string(
                                              (generator.query_pairs_at_least_x_paths(vertices, edges,
                                                                                      queries[6]))))


def generate_coordinates_file(vertices, coordinates, rnd_distance, path):
    long, long_max_diff, lat, lat_max_diff, alt, alt_max_diff = coordinates
    if rnd_distance:
        coors = generator.gen_coordinate_by_range(vertices, long, long_max_diff, lat, lat_max_diff, alt, alt_max_diff)
    else:
        coors = generator.gen_coordinate_by_index(vertices, long, long_max_diff, lat, lat_max_diff, alt, alt_max_diff)
    read_write_io.write_to_file_co(path + FILE_NAME_CO + str(get_curr_time()), generator.co_input_to_string(coors))


def weight_edges_and_write_files(vertices, edges, objectives_ranges, edges_weights_method, dest_directory):
    for i in range(0, len(objectives_ranges) - 1, 2):
        if objectives_ranges[i] > -1:  # This objective exists
            weighted_edges = generate_edges_weights(vertices, edges, edges_weights_method, objectives_ranges[i],
                                                    objectives_ranges[i + 1])
            write_to_files(dest_directory, vertices, weighted_edges)


def write_to_files(path, vertices, edges):
    time_stamp = str(get_curr_time())
    read_write_io.write_to_file_gr(path + FILE_NAME_GR + time_stamp, generator.gr_input_to_string(vertices, edges))


def generate_fully_random_graph(vertices, bi_directed, dest_directory, objectives_ranges, coordinates, rnd_distance,
                                edges_weights_method, edges_number):
    edges = fully_random(vertices, edges_number, bi_directed)
    weight_edges_and_write_files(vertices, edges, objectives_ranges, edges_weights_method, dest_directory)
    generate_coordinates_file(vertices, coordinates, rnd_distance, dest_directory)
    return edges


def generate_fully_connected_dense_graph(vertices, bi_directed, dest_directory, objectives_ranges, coordinates,
                                         rnd_distance, edges_weights_method):
    edges = fully_connected_dense_graph(vertices, bi_directed)
    weight_edges_and_write_files(vertices, edges, objectives_ranges, edges_weights_method, dest_directory)
    generate_coordinates_file(vertices, coordinates, rnd_distance, dest_directory)
    return edges


def generate_fully_connected_graph(vertices, bi_directed, dest_directory, objectives_ranges, coordinates, rnd_distance,
                                   edges_weights_method, edges_number):
    if edges_number == -1:
        edges = fully_connected(vertices, bi_directed, None)
    else:
        edges = fully_connected(vertices, bi_directed, edges_number)
    weight_edges_and_write_files(vertices, edges, objectives_ranges, edges_weights_method, dest_directory)
    generate_coordinates_file(vertices, coordinates, rnd_distance, dest_directory)
    return edges


def generate_flow_network(vertices, bi_directed, dest_directory, objectives_ranges, coordinates, rnd_distance,
                          edges_weights_method, source_vertex, sink_vertex, num_of_paths):
    edges = flow_network(vertices, bi_directed, source_vertex, sink_vertex, num_of_paths)
    weight_edges_and_write_files(vertices, edges, objectives_ranges, edges_weights_method, dest_directory)
    generate_coordinates_file(vertices, coordinates, rnd_distance, dest_directory)
    return edges


def generate_bipartite_graph(vertices, bi_directed, dest_directory, objectives_ranges, coordinates, rnd_distance,
                             edges_weights_method, edges_number, rel1, rel2):
    edges = bipartite(vertices, bi_directed, edges_number, rel1, rel2)
    weight_edges_and_write_files(vertices, edges, objectives_ranges, edges_weights_method, dest_directory)
    generate_coordinates_file(vertices, coordinates, rnd_distance, dest_directory)
    return edges


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


def bipartite(num_vertices, bi_directed, num_edges, group1, group2):
    edges = generator.bipartite(num_vertices, num_edges, group1, group2)
    if bi_directed:
        edges = generator.change_to_bidirected(edges)
    return edges


def write_to_file_gr(path, edges):
    read_write_io.write_to_file_gr(path + FILE_NAME_GR + str(get_curr_time()), edges)


def get_objectives():
    return read_write_io.read_config()


def generate_2d_grid(xs, ys, blocks, movement_in_axes, movement_weight, min_weight, max_weight, dest_directory):
    grid = generator.crate_2d_grid(xs, ys, blocks)
    movement = generator.movement_2d_grid(grid, movement_in_axes)
    vertices = generator.grid_2d_vertices(grid)
    if movement_weight == 0:
        edges = generator.weight_grid_one_per_axis(movement, vertices)
    else:
        edges = generator.weight_grid_random(movement, vertices, min_weight, max_weight)
    generate_grid_files(edges, vertices, dest_directory)
    return edges


def generate_3d_grid(xs, ys, zs, blocks, movement_in_axes, movement_weight, min_weight, max_weight, dest_directory):
    grid = generator.crate_3d_grid(xs, ys, zs, blocks)
    movement = generator.movement_3d_grid(grid, movement_in_axes)
    vertices = generator.grid_3d_vertices(grid)
    if movement_weight == 0:
        edges = generator.weight_grid_one_per_axis(movement, vertices)
    else:
        edges = generator.weight_grid_random(movement, vertices, min_weight, max_weight)
    generate_grid_files(edges, vertices, dest_directory)
    return edges


def generate_grid_files(edges, coordinates, dest_directory):
    time_stamp = str(get_curr_time())
    full_path_gr = dest_directory + FILE_NAME_GRID + time_stamp
    full_path_co = dest_directory + FILE_NAME_CO + time_stamp
    read_write_io.write_to_file_gr(full_path_gr, generator.gr_input_to_string(len(coordinates), edges))
    read_write_io.write_to_file_co(full_path_co, generator.co_grid_input_to_string(coordinates))

