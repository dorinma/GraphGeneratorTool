import fractions
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
        output.append("v\t" + str(v_coor_list[i][0]) + "\t" + str(v_coor_list[i][1]) + "\t" + str(v_coor_list[i][2]) +
                      "\t" + str(v_coor_list[i][3]) + "\n")
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