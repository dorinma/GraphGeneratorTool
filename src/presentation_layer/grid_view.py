from matplotlib.figure import Figure
import os
from glob import glob


def get_graph_image_by_index(dict_, index, dest_directory):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot()
    curr = dict_[index]
    for o in curr["Open"]:
        ax.plot(o[0], o[1], 'co', markersize=4)  # plot with color blue, as points
    ax.plot(curr["Exp"][0], curr["Exp"][1], 'r^', markersize=6)
    for c in curr["Children"]:
        ax.plot(c[0], c[1], 'ms', markersize=4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(index)
    fig.savefig(dest_directory + index + ".png")
    return fig


def get_single_graph_image(dict_, file_name, dest_directory):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot()
    if dict_.__contains__("Index"):  # Wrong json format
        return None
    for o in dict_["Open"]:
        ax.plot(o[0], o[1], 'co', markersize=4)  # plot with color blue, as points
    ax.plot(dict_["Exp"][0], dict_["Exp"][1], 'r^', markersize=6)
    for c in dict_["Children"]:
        ax.plot(c[0], c[1], 'ms', markersize=4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(file_name)
    fig.savefig(dest_directory + file_name + ".png")
    return fig


def create_gif(dir):
    files = glob(os.path.join(dir, '*.png'))
    import imageio
    out_path = os.path.dirname(os.getcwd()) + "\\out\\" +  "out_gif.gif"
    with imageio.get_writer(out_path, mode='I', duration=0.5) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)
    print("[INFO] Saved gif to " + out_path)
