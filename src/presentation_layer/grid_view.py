import math

from matplotlib.figure import Figure
import os
from glob import glob

INDEX = "Index"
OPEN = "Open"
EXP = "Exp"
CHILDS = "Children"


def get_graph_image_by_index(dict_, index, dest_directory):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot()
    curr = dict_[index]
    for o in curr[OPEN]:
        ax.plot(o[0], o[1], 'co', markersize=4)  # plot with color blue, as points
    ax.plot(curr[EXP][0], curr[EXP][1], 'r^', markersize=6)
    for c in curr[CHILDS]:
        ax.plot(c[0], c[1], 'ms', markersize=4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    max_x, max_y = get_max_axes(dict_)
    min_x, min_y = get_min_axes(dict_)
    ax.axis([min_x - 1, max_x + 1, min_y - 1, max_y + 1])  # [xmin, xmax, ymin, ymax]
    ax.set_title(index)
    fig.savefig(dest_directory + index + ".png")
    return fig


def get_single_graph_image(dict_, file_name, dest_directory):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot()
    if dict_.__contains__(INDEX):  # Wrong json format
        return None
    for o in dict_[OPEN]:
        ax.plot(o[0], o[1], 'co', markersize=4)  # plot with color blue, as points
    ax.plot(dict_[EXP][0], dict_[EXP][1], 'r^', markersize=6)
    for c in dict_[CHILDS]:
        ax.plot(c[0], c[1], 'ms', markersize=4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    max_x, max_y = get_max_axes_single_state(dict_)
    min_x, min_y = get_min_axes_single_state(dict_)
    ax.axis([min_x - 1, max_x + 1, min_y - 1, max_y + 1])  # [xmin, xmax, ymin, ymax]
    ax.set_title(file_name)
    fig.savefig(dest_directory + file_name + ".png")
    return fig


def get_max_axes(_dict):
    max_x, max_y = -math.inf, -math.inf
    for i in _dict:
        x, y = get_max_axes_single_state(_dict[i])
        max_x, max_y = max(x, max_x), max(y, max_y)
    return max_x, max_y


def get_max_axes_single_state(inner_dict):
    max_x, max_y = inner_dict[EXP][0], inner_dict[EXP][1]
    for o in inner_dict[OPEN]:
        max_x = max(max_x, o[0])
        max_y = max(max_y, o[1])
    for c in inner_dict[CHILDS]:
        max_x = max(max_x, c[0])
        max_y = max(max_y, c[1])
    return max_x, max_y


def get_min_axes(_dict):
    min_x, min_y = math.inf, math.inf
    for i in _dict:
        x, y = get_min_axes_single_state(_dict[i])
        min_x, min_y = min(x, min_x), min(y, min_y)
    return min_x, min_y


def get_min_axes_single_state(inner_dict):
    min_x, min_y = inner_dict[EXP][0], inner_dict[EXP][1]
    for o in inner_dict[OPEN]:
        min_x = min(min_x, o[0])
        min_y = min(min_y, o[1])
    for c in inner_dict[CHILDS]:
        min_x = min(min_x, c[0])
        min_y = min(min_y, c[1])
    return min_x, min_y


def create_gif(src_dir, dest_dir):
    files = glob(os.path.join(src_dir, '*.png'))
    import imageio
    out_path = dest_dir + "out_gif.gif"
    with imageio.get_writer(out_path, mode='I', duration=0.5) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)
    print("[INFO] Saved gif to " + out_path)
