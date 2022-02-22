from tkinter import *
import ui
import generator

#root = Tk()
#my_gui = ui.GUI(root)
#root.mainloop()

grid = generator.crate_3d_grid(4, 6, 8, 40)
print(generator.movement_3d_grid(grid, 2))