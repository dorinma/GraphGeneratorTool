import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import cm
import imageio


# {index: {open: [], exp: < x, y >, childs: []...}
# dict = {}
# open = [(1,2), (2,4), (3,6)]
# exp = (6,8)
# childs = [(2,3), (3,4), (4,5)]
# dict["open"] = open
# dict["exp"] = exp
# dict["childs"] = childs


def get_graph_image_by_index(dict_, min_x, max_x, min_y, max_y, index, x_label, y_label):
    x = np.arange(start=0.  # upper limit
                  , stop=6.  # lower limit
                  , step=0.1  # step-size (distance between the points)
                  )  # generate points between start and stop with distances of step apart from each other

    plt.figure()  # generates a new figure as in MATLAB
    plt.subplot()
    dict = dict_[index]
    for o in dict["open"]:
        plt.plot(o[0], o[1], 'bo', markersize=9)  # plot with color blue, as points
    plt.plot(dict["exp"][0], dict["exp"][1], 'r^', markersize=12)
    for c in dict["childs"]:
        plt.plot(c[0], c[1], 'co', markersize=9)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.axis([min_x, max_x, min_y, max_y])  # [xmin, xmax, ymin, ymax]
    plt.title(str(index))
    plt.savefig('open_list.png')
    plt.show()


def create_gif():
    filenames = ["config/myplot.png", "config/myplot2.png", "config/myplot3.png"]
    import imageio
    with imageio.get_writer(os.getcwd() + "\\out\\" + "movie.gif", mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
