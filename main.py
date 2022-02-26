from tkinter import *

from matplotlib import figure
from matplotlib.pyplot import plot

import ui
import grid_view

root = Tk()
my_gui = ui.GUI(root)
root.mainloop()

# import read_write_io
#
# string_ = read_write_io.read_json()
# grid_view.get_graph_image_by_index_2(string_, 0, 10, 0, 10, "1", "temp", "temp2")
