from matplotlib.figure import Figure

# def get_graph_image_by_index(dict_, min_x, max_x, min_y, max_y, index, x_label, y_label):
#     x = np.arange(start=0.  # upper limit
#                   , stop=6.  # lower limit
#                   , step=0.1  # step-size (distance between the points)
#                   )  # generate points between start and stop with distances of step apart from each other
#
#     plt.figure()  # generates a new figure as in MATLAB
#     plt.subplot()
#     curr = dict_[index]
#     for o in curr["Open"]:
#         plt.plot(o[0], o[1], 'bo', markersize=9)  # plot with color blue, as points
#     plt.plot(curr["Exp"][0], curr["Exp"][1], 'r^', markersize=12)
#     for c in curr["Children"]:
#         plt.plot(c[0], c[1], 'co', markersize=9)
#     plt.xlabel("x")
#     plt.ylabel("y")
#     plt.axis([min_x, max_x, min_y, max_y])  # [xmin, xmax, ymin, ymax]
#     plt.title(str(index))
#     plt.savefig('open_list.png')
#     plt.show()

def get_graph_image_by_index(dict_, min_x, max_x, min_y, max_y, index):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot()
    curr = dict_[index]
    for o in curr["Open"]:
        ax.plot(o[0], o[1], 'bo', markersize=4)  # plot with color blue, as points
    ax.plot(curr["Exp"][0], curr["Exp"][1], 'r^', markersize=6)
    for c in curr["Children"]:
        ax.plot(c[0], c[1], 'co', markersize=4)
    ax.axis([min_x, max_x, min_y, max_y])  # [xmin, xmax, ymin, ymax]
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return fig
