import fractions
import itertools
import math
import random
from collections import deque

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
        edges.add(Edge(vertices[i], vertices[i + 1]))
        edges.add(Edge(vertices[i + 1], vertices[i]))
    num_of_edges = len(edges)
    if num_edges is not None:
        bias = fractions.Fraction(num_edges, num_vertices * num_vertices - 1)
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


def bipartite(num_vertices, num_edges, group_a, group_b):
    group_a = (group_a * num_vertices) // (group_a + group_b)
    group_b = num_vertices - group_a
    group_a_ver = random.sample(range(1, num_vertices + 1), group_a)
    all_ver = list(range(1, num_vertices))
    group_b_ver = []
    for v in all_ver:
        if v not in group_a_ver:
            group_b_ver.append(v)
    edges = set()
    while len(edges) != num_edges:
        edges.add(Edge(group_a_ver[random.randint(0, group_a)], group_b_ver[random.randint(0, group_b)]))
    return edges


def weights_to_edges_random(edges, min_value, max_value):
    weighted_edges = set()
    for edge in edges:
        value = random.randint(min_value, max_value)
        weighted_edges.add(EdgeWithValue(edge.u, edge.v, value))
    return weighted_edges


def weights_to_edges_planar_connection(edges, min_value, max_value):
    weighted_edges = set()
    if min_value == max_value:
        for edge in edges:
            weighted_edges.add(EdgeWithValue(edge.u, edge.v, max_value))
        return weighted_edges
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
        value = min_value + abs(edge.u - edge.v) * weight_for_one_diff
        weighted_edges.add(EdgeWithValue(edge.u, edge.v, value))
    return weighted_edges


def weights_to_edges_coordinate(edges, v_coor_list):
    v_coor_dict = {}
    for v in v_coor_list:
        if len(v) == 4:
            v_coor_dict[v[0]] = (v[1], v[2], v[3])
        else:
            v_coor_dict[v[0]] = (v[1], v[2])
    weighted_edges = set()
    for edge in edges:
        u_coor = v_coor_dict[edge.u]
        v_coor = v_coor_dict[edge.v]
        distance = math.pow(u_coor[0] - v_coor[0], 2) + math.pow(u_coor[1] - v_coor[1], 2)
        if len(u_coor) == 3:
            distance += math.pow(u_coor[2] - v_coor[2], 2)
        distance = math.sqrt(distance)
        weighted_edges.add(EdgeWithValue(edge.u, edge.v, distance))
    return weighted_edges


def query_random(num_vertices, num_pairs):
    query = set()
    while len(query) != num_pairs:
        pair = random.sample(range(1, num_vertices + 1), 2)
        query.add((pair[0], pair[1]))
    return query


def query_all_vertices_pairs(num_vertices):
    query = set()
    for i in range(1, num_vertices + 1):
        for j in range(1, num_vertices + 1):
            if i != j:
                query.add((i, j))
    return query


def query_pairs_at_least_x_edges(num_vertices, edges, x):
    query = set()
    for i in range(1, num_vertices + 1):
        for j in range(1, num_vertices + 1):
            if i != j:
                neighbors = get_neighbors_dict(edges)
                paths = all_paths_source_target_at_least_x(neighbors, i, j, x)
                if len(paths) > 0:
                    query.add((i, j))
    return query


def query_pairs_at_least_x_paths(num_vertices, edges, x):
    query = set()
    for i in range(1, num_vertices + 1):
        for j in range(1, num_vertices + 1):
            if i != j:
                neighbors = get_neighbors_dict(edges)
                paths = all_paths_source_target(neighbors, i, j)
                if len(paths) > x:
                    query.add((i, j))
    return query


def query_to_string(pairs):
    output = []
    if len(pairs) == 0:
        output.append("No such queries.")
    else:
        for pair in pairs:
            output.append(str(pair[0]) + ", " + str(pair[1]) + "\n")
    return output


def gen_coordinate_by_range(num_vertices, long, long_max_diff, lat, lat_max_diff, alt, alt_max_diff):
    coor_list = []
    if alt != 0 and alt_max_diff != 0:
        coor_list.append((1, long, lat, alt))
    else:
        coor_list.append((1, long, lat))
    for i in range(2, num_vertices + 1):
        long_ = long + random.randint(-1 * long_max_diff, long_max_diff)
        lat_ = lat + random.randint(-1 * lat_max_diff, lat_max_diff)
        if alt != 0 and alt_max_diff != 0:
            alt_ = alt + random.randint(-1 * alt_max_diff, alt_max_diff)
            coor_list.append((i, long_, lat_, alt_))
        else:
            coor_list.append((i, long_, lat_))
    return coor_list


def gen_coordinate_by_index(num_vertices, long, long_max_diff, lat, lat_max_diff, alt, alt_max_diff):
    coor_list = []
    for i in range(1, num_vertices + 1):
        long_ = long + random.randint((i - 1) * long_max_diff // num_vertices, i * long_max_diff // num_vertices)
        lat_ = lat + random.randint((i - 1) * lat_max_diff // num_vertices, i * lat_max_diff // num_vertices)
        if alt != 0 and alt_max_diff != 0:
            alt_ = alt + random.randint((i - 1) * alt_max_diff // num_vertices, i * alt_max_diff // num_vertices)
            coor_list.append((i, long_, lat_, alt_))
        else:
            coor_list.append((i, long_, lat_))
    return coor_list


def gr_input_to_string(num_vertices, edges):
    output = ["c\tCreated in graph generator tool by Shahar Bardugo & Dorin Matzrafi\n", "c\n",
              "p\tsp " + str(num_vertices) + " " + str(len(edges)) + "\n",
              "c\tgraph contains " + str(num_vertices) + " nodes and " + str(len(edges)) + " arcs\n", "c\n"]
    for edge in edges:
        output.append("a\t" + str(edge.u) + "\t" + str(edge.v) + "\t" + str(edge.weight) + "\n")
    return output


def co_input_to_string(v_coor_list):
    output = ["c\tCreated in graph generator tool by Shahar Bardugo & Dorin Matzrafi\n", "c\n",
              "p\taux sp co " + str(len(v_coor_list)) + "\n", "c\tgraph contains " + str(len(v_coor_list)) + " nodes\n",
              "c\n"]
    for i in range(0, len(v_coor_list)):
        if len(v_coor_list[i]) == 4:
            output.append("v\t" + str(v_coor_list[i][0]) + "\t" + str(v_coor_list[i][1]) + "\t" + str(v_coor_list[i][2])
                          + "\t" + str(v_coor_list[i][3]) + "\n")
        else:
            output.append(
                "v\t" + str(v_coor_list[i][0]) + "\t" + str(v_coor_list[i][1]) + "\t" + str(v_coor_list[i][2]) + "\n")
    return output


def write_to_file_gr(full_path, edges):
    try:
        file = open(full_path + ".gr", 'w')
        file.writelines(edges)
        file.close()
        print("[INFO] Saved output to " + full_path)
    except:
        print("[ERROR] Could not write .gr file.")


def write_to_file_co(full_path, edges):
    try:
        file = open(full_path + '.co', 'w')
        file.writelines(edges)
        file.close()
        print("[INFO] Saved output to " + full_path)
    except:
        print("[ERROR] Could not write .co file.")


def write_to_file_query(full_path, edges):
    try:
        file = open(full_path, 'w')
        file.writelines(edges)
        file.close()
        print("[INFO] Saved output to " + full_path)
    except:
        print("[ERROR] Could not write query file.")


def get_neighbors_dict(edges):
    neighbors = {}
    for edge in edges:
        if edge.u in neighbors:
            neighbors[edge.u].append(edge.v)
        else:
            neighbors[edge.u] = []
    return neighbors


def all_paths_source_target_at_least_x(neighbors, s, g, x):
    ans = []
    q = deque([(s, [s])])
    while q:
        cur_node, cur_path = q.popleft()
        if cur_node == g:
            if len(cur_path) > x:
                ans.append(cur_path)
                return ans
        nexts = neighbors[cur_node]
        for nextNode in nexts:
            if nextNode not in cur_path:
                q.append((nextNode, cur_path + [nextNode]))
    return ans


def all_paths_source_target(neighbors, s, g):
    ans = []
    q = deque([(s, [s])])
    while q:
        cur_node, cur_path = q.popleft()
        if cur_node == g:
            ans.append(cur_path)
        nexts = neighbors[cur_node]
        for nextNode in nexts:
            if nextNode not in cur_path:
                q.append((nextNode, cur_path + [nextNode]))
    return ans


def crate_2d_grid(x, y, num_blocks):
    d2_grid = [[0 for i in range(x)] for j in range(y)]
    counter = 0
    bias = fractions.Fraction(num_blocks, x*y)
    while counter != num_blocks:
        for i in range(0, y):
            for j in range(0, x):
                if random.random() < bias and counter != num_blocks and d2_grid[i][j] == 0:
                    d2_grid[i][j] = -1
                    counter += 1
    return d2_grid


def crate_3d_grid(x, y, z, num_blocks):
    d3_grid = [[[0 for i in range(x)] for j in range(y)] for k in range(z)]
    counter = 0
    bias = fractions.Fraction(num_blocks, x*y*z)
    while counter != num_blocks:
        for i in range(0, z):
            for j in range(0, y):
                for k in range(0, x):
                    if random.random() < bias and counter != num_blocks and d3_grid[i][j][k] == 0:
                        d3_grid[i][j][k] = -1
                        counter += 1
    return d3_grid


def movement_2d_grid(grid, num_direction_movement):
    movement = {}
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            move = []
            if grid[i][j] != -1:
                x_list = []
                y_list = []
                if i-1 in range(0, len(grid)):
                    x_list.append(i-1)
                if i+1 in range(0, len(grid)):
                    x_list.append(i+1)
                if j-1 in range(0, len(grid[0])):
                    y_list.append(j-1)
                if j+1 in range(0, len(grid[0])):
                    y_list.append(j+1)
                for it in itertools.product([i], y_list):
                    move.append(it)
                for it in itertools.product(x_list, [j]):
                    move.append(it)
                if num_direction_movement == 2:
                    for it in itertools.product(x_list, y_list):
                        move.append(it)
                for move_ in move:
                    if grid[move_[0]][move_[1]] == -1:
                        move.remove(move_)
                movement[(i, j)] = move
    return movement


def movement_3d_grid(grid, num_direction_movement):
    movement = {}
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            for k in range(0, len(grid[0][0])):
                move = []
                if grid[i][j][k] != -1:
                    x_list = []
                    y_list = []
                    z_list = []
                    if i-1 in range(0, len(grid)):
                        x_list.append(i-1)
                    if i+1 in range(0, len(grid)):
                        x_list.append(i+1)
                    if j-1 in range(0, len(grid[0])):
                        y_list.append(j-1)
                    if j+1 in range(0, len(grid[0])):
                        y_list.append(j+1)
                    if k-1 in range(0, len(grid[0][0])):
                        z_list.append(k-1)
                    if k+1 in range(0, len(grid[0][0])):
                        z_list.append(k+1)
                    for it in itertools.product([i], [j], z_list):
                        move.append(it)
                    for it in itertools.product([i], y_list, [k]):
                        move.append(it)
                    for it in itertools.product(x_list, [j], [k]):
                        move.append(it)
                    if num_direction_movement == 2 or num_direction_movement == 3:
                        for it in itertools.product(x_list, y_list, [k]):
                            move.append(it)
                        for it in itertools.product([i], y_list, z_list):
                            move.append(it)
                        for it in itertools.product(x_list, [j], z_list):
                            move.append(it)
                    if num_direction_movement == 3:
                        for it in itertools.product(x_list, y_list, z_list):
                            move.append(it)
                    for move_ in move:
                        if grid[move_[0]][move_[1]][move_[2]] == -1:
                            move.remove(move_)
                    movement[(i, j, k)] = move
    return movement


def grid_2d_vertices(grid):
    coor_ver = {}
    counter = 1
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            coor_ver[(i, j)] = counter
            counter += 1
    return coor_ver


def grid_3d_vertices(grid):
    coor_ver = {}
    counter = 1
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            for k in range(0, len(grid[0][0])):
                coor_ver[(i, j, k)] = counter
                counter += 1
    return coor_ver


def weight_grid_one_per_axis(movement, coor_ver):
    edges = set()
    for u in movement:
        v_list = movement[u]
        for v in v_list:
            weight = abs(u[0] - v[0]) + abs(u[1] - v[1])
            if len(u) == 3:
                weight += abs(u[2] - v[2])
            if weight == 1:
                edges.add(EdgeWithValue(coor_ver[u], coor_ver[v], weight))
            else:
                edges.add(EdgeWithValue(coor_ver[u], coor_ver[v], math.sqrt(weight)))
    return edges


def weight_grid_random(movement, coor_ver, min_value, max_value):
    edges = set()
    for u in movement:
        v_list = movement[u]
        for v in v_list:
            value = random.randint(min_value, max_value)
            edges.add(EdgeWithValue(coor_ver[u], coor_ver[v], value))
    return edges


def co_grid_input_to_string(v_coor_dict):
    output = ["c\tCreated in graph generator tool by Shahar Bardugo & Dorin Matzrafi\n", "c\n",
              "p\taux sp co " + str(len(v_coor_dict)) + "\n", "c\tgraph contains " + str(len(v_coor_dict)) + " nodes\n",
              "c\n"]
    for key in v_coor_dict:
        if len(key) == 3:
            output.append("v\t" + str(v_coor_dict[key]) + "\t" + str(key[0]) + "\t" + str(key[1])
                          + "\t" + str(key[2]) + "\n")
        else:
            output.append(
                "v\t" + str(v_coor_dict[key]) + "\t" + str(key[0]) + "\t" + str(key[1]) + "\n")
    return output
