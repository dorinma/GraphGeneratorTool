from tkinter import *
from tkinter import filedialog as fd
import tkinter.messagebox
import os
import matplotlib as mpl
from matplotlib.figure import Figure

mpl.use('TkAgg')
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from matplotlib.backend_bases import key_press_handler

import adapter
import grid_params
import grid_view

objectives_options = ('1', '2', '3', '4', '5')
methods_options = ('Fully Random', 'Fully Connected Dense Graph', 'Fully Connected', 'Flow Network',
                   'Grid Connection', 'Bipartite Graph')
weights_options_graphs = ('Fully Random', 'Planar', 'Predefined Calculation', 'By Coordinates')
# weights_options_grid = ('By axis (1)', 'Random')
# queries_options = ('All Pairs', 'Random', 'Minimal Edges', 'Minimal Paths')
source_directory, dest_directory = os.getcwd() + "\\out\\", os.getcwd() + "\\out\\"
row_index = 0
LONG = -74005973
LAT = 40712775
ALT = 10
COOR_DIFF = 1000
ALT_DIFF = 100
MSG_TITLE_MISSING_PARAMS = "Missing Parameters"
MSG_TITLE_INVALID_INPUT = "Invalid Input"


class Prox(Entry):
    """ AN Entry widget that only accepts digits """

    def __init__(self, master=None, **kwargs):
        self.var = StringVar(master)
        self.var.trace('w', self.validate)
        Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.get, self.set = self.var.get, self.var.set

    def validate(self, *args):
        value = self.get()
        if not value.isdigit():
            self.set(''.join(x for x in value if x.isdigit()))


def get_source_directory():
    source_directory = fd.askdirectory()


def get_dest_directory():
    global dest_directory
    dest_directory = fd.askdirectory() + "/"


def inc_row():
    global row_index
    row_index += 1


def validate_objective_range(min_, max_):
    if min_ > max_:
        return False
    else:
        return True


# Custom toolbar
class CustomToolbar(NavigationToolbar2Tk):
    def load_figure(self):
        filetypes = (
            ('json files', '*.json'),
            ('All files', '*.*')
        )
        path_str = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        if path_str:
            new_state = adapter.get_single_input_graph(os.path.normpath(path_str))
            self.gui.display_grid(new_state, -1, os.path.splitext(os.path.basename(path_str))[0])

    def __init__(self, canvas_, parent_, gui):
        self.gui = gui
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            (None, None, None, None),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
            ('Load', 'Load the figure', 'subplots', 'load_figure'),
        )
        NavigationToolbar2Tk.__init__(self, canvas_, parent_, pack_toolbar=False)


class GUI:

    def clear(self):
        self.t_vertices.delete(0, 'end')
        self.edges_gen_methods.set(methods_options[0])
        self.edges_weights_method.set(weights_options_graphs[0])
        self.cb_bidirectional.deselect()

    def open_edges_method_window(self, method):
        if method == methods_options[1]:  # Fully Connected Dense Graph - no params
            self.om_edges_weights.config(state='normal')
            return
        elif method == methods_options[4]:  # Grid - another window
            self.om_edges_weights.config(state='disabled')
            self.open_grid_window()
            return
        else:
            self.om_edges_weights.config(state='normal')

        self.edges_method_window = Toplevel(self.root)
        self.edges_method_window.title("Method Params")
        self.edges_method_window.geometry("280x150")
        self.edges_method_window.resizable(False, False)

        row = 0
        Label(self.edges_method_window, text="Insert parameters").grid(row=row, column=0, pady=2, padx=6, columnspan=2,
                                                                       sticky=W)
        row += 1
        if method == methods_options[0]:  # Fully Random
            Label(self.edges_method_window, text="Choose one from below:").grid(row=row, column=0, padx=6, pady=2,
                                                                                columnspan=3, sticky=W)
            row += 1

            self.edges_method_full_rnd_perc = IntVar()
            self.rb_edges_num = Radiobutton(self.edges_method_window, text="Number of edges", value=0,
                                            variable=self.edges_method_full_rnd_perc, command=self.rb_num_percentage)
            self.rb_edges_num.grid(row=row, column=0, padx=6, pady=2, sticky=W)

            self.t_edges_number = Prox(self.edges_method_window, width=12)
            self.t_edges_number.grid(row=row, column=1, padx=2, pady=6, sticky=NW, columnspan=2)
            row += 1

            self.rb_edges_percentage = Radiobutton(self.edges_method_window, text="Percentage (from full graph)",
                                                   value=1, variable=self.edges_method_full_rnd_perc,
                                                   command=self.rb_num_percentage)
            self.rb_edges_percentage.grid(row=row, column=0, padx=6, pady=2, sticky=W)

            self.t_edges_percentage = Prox(self.edges_method_window, width=5, state='readonly')
            self.t_edges_percentage.grid(row=row, column=1, padx=2, pady=6, sticky=NW)
            Label(self.edges_method_window, text="%").grid(row=row, column=2, pady=2, sticky=W)
            row += 1

            self.b_set_edges_m1 = Button(self.edges_method_window, text="Set", width=10,
                                         command=self.get_fully_random_params)
            self.b_set_edges_m1.grid(row=row, column=1, padx=2, pady=2, sticky=W, columnspan=2)

        elif method == methods_options[2]:  # Fully Connected
            Label(self.edges_method_window, text="Choose one from below:").grid(row=row, column=0, padx=6, pady=2,
                                                                                columnspan=5, sticky=W)
            row += 1

            self.edges_method_full_connected = IntVar()
            self.rb_mst = Radiobutton(self.edges_method_window, text="MST", value=0, command=self.rb_add_edges,
                                      variable=self.edges_method_full_connected)
            self.rb_mst.grid(row=row, column=0, padx=6, pady=2, sticky=W)
            row += 1

            self.rb_add_edges = Radiobutton(self.edges_method_window, text="Additional Edges (to MST)", value=1,
                                            variable=self.edges_method_full_connected, command=self.rb_add_edges)
            self.rb_add_edges.grid(row=row, column=0, padx=6, pady=2, sticky=W)

            self.t_add_edges_to_mst = Prox(self.edges_method_window, width=12, state='readonly')
            self.t_add_edges_to_mst.grid(row=row, column=1, rowspan=2, padx=2, pady=6, sticky=NW)
            row += 1

            self.b_set_edges_m2 = Button(self.edges_method_window, text="Set", width=10,
                                         command=self.get_fully_connected_params)
            self.b_set_edges_m2.grid(row=row, column=1, padx=2, pady=2, sticky=W)

        elif method == methods_options[3]:  # Flow Network
            Label(self.edges_method_window, text="Choose vertices' indexes:").grid(row=row, column=0, padx=6, pady=2,
                                                                                   columnspan=2, sticky=W)
            row += 1

            Label(self.edges_method_window, text="Source:").grid(row=row, column=0, padx=6, pady=2, sticky=W)
            self.t_edge_src = Prox(self.edges_method_window, width=10)
            self.t_edge_src.grid(row=row, column=1, padx=6, pady=2, sticky=E)
            row += 1

            Label(self.edges_method_window, text="Destination:").grid(row=row, column=0, padx=6, pady=2, sticky=W)
            self.t_edge_dst = Prox(self.edges_method_window, width=10)
            self.t_edge_dst.grid(row=row, column=1, padx=6, pady=2, sticky=E)
            row += 1

            Label(self.edges_method_window, text="Number of paths:").grid(row=row, column=0, padx=6, pady=2, sticky=W)
            self.t_edge_paths_num = Prox(self.edges_method_window, width=10)
            self.t_edge_paths_num.grid(row=row, column=1, padx=6, pady=2, sticky=E)

            self.b_set_edges_m3 = Button(self.edges_method_window, text="Set", width=8, command=self.get_flow_params)
            self.b_set_edges_m3.grid(row=row, column=2, padx=4, pady=2)

        elif method == methods_options[5]:  # Bipartite Graph
            Label(self.edges_method_window, text="Relation between sets of vertices:").grid(row=row, column=0, padx=6,
                                                                                            pady=2, sticky=W)

            self.t_edge_relation = Text(self.edges_method_window, height=1, width=6)
            self.t_edge_relation.grid(row=row, column=2, padx=6, pady=2, sticky=E)

            row += 1

            Label(self.edges_method_window, text="[e.g. 1:1, 1:2]").grid(row=row, column=0, padx=6, pady=2,
                                                                         columnspan=2, sticky=W)

            row += 1

            Label(self.edges_method_window, text="Number of edges between sets:").grid(row=row, column=0, padx=6,
                                                                                       pady=2, columnspan=2, sticky=W)
            self.t_edges_between_groups = Prox(self.edges_method_window, width=10)
            self.t_edges_between_groups.grid(row=row, column=2, padx=6, pady=2, sticky=E)

            row += 1

            self.b_set_edges_m3 = Button(self.edges_method_window, text="Set", width=8,
                                         command=self.get_bipartite_params)
            self.b_set_edges_m3.grid(row=row, column=2, padx=4, pady=2, sticky=E)

    def rb_grid_dims(self):
        if self.rb_grid_dim.get() == 0:  # 2D
            self.t_zs.config(state='readonly')
            self.rb_grid_move_3.config(state='disabled')
        else:
            self.t_zs.config(state='normal')
            self.rb_grid_move_3.config(state='normal')

    def rb_grid_edges(self):
        if self.rb_grid_edges_method.get() == 0:  # Const weight
            self.t_grid_rnd_weight_min.config(state='readonly')
            self.t_grid_rnd_weight_max.config(state='readonly')
        else:
            self.t_grid_rnd_weight_min.config(state='normal')
            self.t_grid_rnd_weight_max.config(state='normal')

    def set_grid_params(self):
        if not self.validate_and_set_grid_params():
            tkinter.messagebox.showinfo(title=MSG_TITLE_MISSING_PARAMS,
                                        message='Please make sure all fields are not empty.', parent=self.grid_window)
        else:
            self.valid_grid_values = True
            self.grid_window.destroy()

    def validate_and_set_grid_params(self):
        dim = 2
        cost_min, cost_max = -1, -1
        if self.rb_grid_dim.get() == 1:
            dim = 3
        if self.t_xs.get() == '' or self.t_ys.get() == '' or (dim == 3 and self.t_zs.get() == ''):
            return False
        else:
            xs, ys = int(self.t_xs.get()), int(self.t_ys.get())
            if dim == 3:
                zs = int(self.t_zs.get())
            else:
                zs = 0
            if self.t_grid_blocks.get() != '':
                blocks = int(self.t_grid_blocks.get())
            else:
                blocks = 0
            axes_movement = self.rb_grid_move_axes.get() + 1
            movement_cost = self.rb_grid_edges_method.get()  # 0 for const weight, 1 for random
            if movement_cost == 1:
                if self.t_grid_rnd_weight_min.get() != '' and self.t_grid_rnd_weight_min.get() != '':
                    cost_min, cost_max = int(self.t_grid_rnd_weight_min.get()), int(self.t_grid_rnd_weight_max.get())
                else:
                    return False
            self.grid_params.set_values(dim, xs, ys, zs, blocks, axes_movement, movement_cost, cost_min, cost_max)
            return True

    def open_grid_window(self):
        self.grid_window = Toplevel(self.root)
        self.grid_window.title("Grid Parameters")
        self.grid_window.geometry("340x330")
        self.grid_window.resizable(False, False)

        row = 0

        self.rb_grid_dim = IntVar()
        self.rb_grid2d = Radiobutton(self.grid_window, text="2D", value=0, variable=self.rb_grid_dim,
                                     command=self.rb_grid_dims)
        self.rb_grid2d.grid(row=row, column=0, padx=5, pady=5, sticky=E)

        self.rb_grid3d = Radiobutton(self.grid_window, text="3D", value=1, variable=self.rb_grid_dim,
                                     command=self.rb_grid_dims)
        self.rb_grid3d.grid(row=row, column=1, pady=5, sticky=W)

        Label(self.grid_window, text="Movement in # axes").grid(row=row, column=2, pady=2, padx=5, sticky=EW,
                                                                columnspan=2)

        row += 1

        Label(self.grid_window, text="Xs:").grid(row=row, column=0, pady=2, padx=5, sticky=W)

        self.t_xs = Prox(self.grid_window, width=10)
        self.t_xs.grid(row=row, column=1, padx=8, pady=2, sticky=W)

        self.rb_grid_move_axes = IntVar()
        self.rb_grid_move_1 = Radiobutton(self.grid_window, text="1", value=0, variable=self.rb_grid_move_axes,
                                          command=self.rb_grid_edges)
        self.rb_grid_move_1.grid(row=row, column=2, padx=5, sticky=EW, columnspan=2)

        row += 1

        Label(self.grid_window, text="Ys:").grid(row=row, column=0, pady=2, padx=5, sticky=W)

        self.t_ys = Prox(self.grid_window, width=10)
        self.t_ys.grid(row=row, column=1, padx=8, pady=2, sticky=W)

        self.rb_grid_move_2 = Radiobutton(self.grid_window, text="2", value=1, variable=self.rb_grid_move_axes,
                                          command=self.rb_grid_edges)
        self.rb_grid_move_2.grid(row=row, column=2, padx=5, sticky=EW, columnspan=2)

        row += 1

        Label(self.grid_window, text="Zs:").grid(row=row, column=0, pady=2, padx=5, sticky=W)

        self.t_zs = Prox(self.grid_window, width=10, state='readonly')
        self.t_zs.grid(row=row, column=1, padx=8, pady=2, sticky=W)

        self.rb_grid_move_3 = Radiobutton(self.grid_window, text="3", value=2, variable=self.rb_grid_move_axes,
                                          command=self.rb_grid_edges, state='disabled')
        self.rb_grid_move_3.grid(row=row, column=2, padx=5, sticky=EW, columnspan=2)

        row += 1

        Label(self.grid_window, text="").grid(row=row, column=0, columnspan=2)

        row += 1

        Label(self.grid_window, text="Blocks #").grid(row=row, column=0, padx=5, sticky=W)

        self.t_grid_blocks = Prox(self.grid_window, width=10)
        self.t_grid_blocks.grid(row=row, column=1, padx=8, pady=4, sticky=W)

        row += 1

        Label(self.grid_window, text="").grid(row=row, column=0, columnspan=3)

        row += 1

        Label(self.grid_window, text="Edges Weights:").grid(row=row, column=0, pady=4, padx=5, sticky=W, columnspan=2)

        row += 1

        self.rb_grid_edges_method = IntVar()
        self.rb_grid_const_wight = Radiobutton(self.grid_window, text="By axis (1 per move)", value=0,
                                               variable=self.rb_grid_edges_method, command=self.rb_grid_edges)
        self.rb_grid_const_wight.grid(row=row, column=0, padx=5, sticky=W, columnspan=2)

        row += 1

        self.rb_grid_rnd_weight = Radiobutton(self.grid_window, text="Random", value=1,
                                              variable=self.rb_grid_edges_method, command=self.rb_grid_edges)
        self.rb_grid_rnd_weight.grid(row=row, column=0, padx=5, sticky=W, columnspan=2)

        Label(self.grid_window, text="Min weight:").grid(row=row, column=2, pady=4, padx=5, sticky=W)

        self.t_grid_rnd_weight_min = Prox(self.grid_window, width=10, state='readonly')
        self.t_grid_rnd_weight_min.grid(row=row, column=3, padx=8, pady=4, sticky=W)

        row += 1

        Label(self.grid_window, text="Max weight:").grid(row=row, column=2, pady=4, padx=5, sticky=W)

        self.t_grid_rnd_weight_max = Prox(self.grid_window, width=10, state='readonly')
        self.t_grid_rnd_weight_max.grid(row=row, column=3, padx=8, pady=4, sticky=W)

        row += 1

        self.b_set_grid_params = Button(self.grid_window, text="Set", command=self.set_grid_params, width=10)
        self.b_set_grid_params.grid(row=row, column=0, padx=8, pady=2, sticky=E)

    def rb_add_edges(self):
        if self.edges_method_full_connected.get() == 1:
            self.t_add_edges_to_mst.config(state='normal')
        else:  # MST
            self.t_add_edges_to_mst.config(state='readonly')

    def rb_num_percentage(self):
        if self.edges_method_full_rnd_perc.get() == 0:
            self.t_edges_percentage.config(state='readonly')
            self.t_edges_number.config(state='normal')
        else:
            self.t_edges_percentage.config(state='normal')
            self.t_edges_number.config(state='readonly')

    def set_objectives_default(self):
        self.objectives = adapter.get_objectives()

    def set_objectives(self, index):
        count = 1 + index
        # First objective
        self.objective_val_window = Toplevel(self.root)
        self.objective_val_window.title(str(count))
        self.objective_val_window.geometry("240x100")
        self.objective_val_window.resizable(False, False)
        self.objective_val_window.protocol("WM_DELETE_WINDOW", self.set_objectives_close_window)
        row = 0
        curr_obj = list(self.objectives.keys())[index]
        Label(self.objective_val_window, text=curr_obj).grid(row=row, column=0, columnspan=3, pady=4, sticky=W)
        row += 1
        Label(self.objective_val_window, text="Min:").grid(row=row, column=0, pady=4, padx=4)
        t_min_o = Prox(self.objective_val_window, width=10)
        t_min_o.grid(row=row, column=1, pady=4)

        Label(self.objective_val_window, text="Max:").grid(row=row, column=2, pady=4, padx=4)
        t_max_o = Prox(self.objective_val_window, width=10)
        t_max_o.grid(row=row, column=3, pady=4)
        row += 1
        Button(self.objective_val_window, text="Keep default", width=12,
               command=lambda: self.save_objective_new_values(index, curr_obj, '-1', '-1')).grid(row=row, column=0,
                                                                                                 pady=2, padx=4,
                                                                                                 columnspan=2,
                                                                                                 sticky=W)
        Button(self.objective_val_window, text="Save", width=8,
               command=lambda: self.save_objective_new_values(index, curr_obj, t_min_o.get(),
                                                              t_max_o.get())).grid(row=row, column=3, pady=2, padx=4)

    def set_objectives_close_window(self):
        answer = tkinter.messagebox.askokcancel(
            title='Confirm exit',
            message='This will stop setting the objectives values. Exit?', parent=self.objective_val_window)
        if answer:
            self.objective_val_window.destroy()

    def save_objective_new_values(self, index, key, min_, max_):
        min_int, max_int = int(min_), int(max_)
        if min_int <= max_int:
            if min_int != -1 and max_int != -1:
                self.objectives[key] = (min_int, max_int)
            self.objective_val_window.destroy()
            if index < len(self.objectives.keys()) - 1:
                self.set_objectives(index + 1)
        else:
            tkinter.messagebox.showinfo("Illegal Values", "Min value must be lower/ equal to max.",
                                        parent=self.objective_val_window)

    def rb_query_min_edges(self):
        self.t_min_edges_between.config(state='normal')
        self.t_min_paths_between.config(state='readonly')
        self.t_queries_num.config(state='readonly')

    def rb_query_min_paths(self):
        self.t_min_paths_between.config(state='normal')
        self.t_min_edges_between.config(state='readonly')
        self.t_queries_num.config(state='readonly')

    def rb_query_number(self):
        self.t_queries_num.config(state='normal')
        self.t_min_paths_between.config(state='readonly')
        self.t_min_edges_between.config(state='readonly')

    def rb_query_all_pairs(self):
        self.t_queries_num.config(state='readonly')
        self.t_min_paths_between.config(state='readonly')
        self.t_min_edges_between.config(state='readonly')

    def validate_queries(self):
        valid = True
        if self.query_method.get() == 1:  # random
            if self.t_queries_num.get() != '':
                queries_num = int(self.t_queries_num.get())
                if queries_num <= 0:
                    valid = False
                else:  # valid number
                    self.queries_param = queries_num
            else:
                valid = False
        if self.query_method.get() == 2:  # min edges between source & target #3 min paths, 0 all pairs
            if self.t_min_edges_between.get() != '':
                min_edges = int(self.t_min_edges_between.get())
                if min_edges <= 0:
                    valid = False
                else:  # valid number
                    self.queries_param = min_edges
            else:
                valid = False
        if self.query_method.get() == 3:  # min paths between source & target
            if self.t_min_edges_between.get() != '':
                min_paths = int(self.t_min_edges_between.get())
                if min_paths <= 0:
                    valid = False
                else:  # valid number
                    self.queries_param = min_paths
            else:
                valid = False
        if not valid:
            tkinter.messagebox.showinfo(MSG_TITLE_MISSING_PARAMS, "Missing queries number or min edges between source "
                                                                  "and target.")
        return valid

    def generate_queries(self):
        if self.validate_queries():
            files = [('All Files', '*.*')]
            file_name = fd.asksaveasfile(filetypes=files)
            if file_name:
                file_path = os.path.normpath(file_name.name)
                print("[DEBUG] Generating queries...")
                adapter.generate_queries(self.vertices, self.edges_generated, self.query_method.get(),
                                         self.queries_param, file_path)

    def create_gif(self):
        dir = fd.askdirectory()
        if dir:
            grid_view.create_gif(dir)

    def save_graph_to(self):
        global dest_directory

        files = [('gr files', '*.gr'),
                 ('All Files', '*.*')]
        file_path = fd.asksaveasfile(filetypes=files)
        dest_directory = file_path
        self.generate_graph()
        # Need to change implementation in adapter.py: take 'dest_directory' as full path including file name,
        # remove file name from implemented methods and send different name for each objective.

    def generate_graph(self):
        global dest_directory

        if self.edges_gen_methods.get() == methods_options[4]:  # Grid
            if self.validate_input_grid():
                if not self.valid_grid_values:
                    tkinter.messagebox.showinfo(MSG_TITLE_MISSING_PARAMS, message='Missing some grid params.')
                    return
                else:
                    if self.grid_params.get_grid_dim() == 2:
                        adapter.generate_2d_grid(self.grid_params.xs, self.grid_params.ys, self.grid_params.blocks,
                                                 self.grid_params.axes_movement, self.grid_params.movement_cost,
                                                 self.grid_params.cost_min, self.grid_params.cost_max, dest_directory)
                    else:
                        adapter.generate_3d_grid(self.grid_params.xs, self.grid_params.ys, self.grid_params.zs,
                                                 self.grid_params.blocks, self.grid_params.axes_movement,
                                                 self.grid_params.movement_cost, self.grid_params.cost_min,
                                                 self.grid_params.cost_max, dest_directory)
        else:
            if self.validate_input_graphs():
                print("[DEBUG] Generating graph...")
                vertices_num = int(self.t_vertices.get())
                coordinates = [self.long, self.long_diff, self.lat, self.lat_diff, self.alt, self.alt_diff]
                rnd_distance = self.rb_coor.get() == 0  # Random
                if self.edges_gen_methods.get() == methods_options[0]:  # Fully Random
                    edges_number = self.edges_number_full_random
                    if self.edges_percentage:
                        edges_number = int((vertices_num * vertices_num) * self.edges_percentage_full_random / 100)
                    self.edges_generated = adapter.generate_fully_random_graph(vertices_num, self.bidir.get() == 1,
                                                                               dest_directory, self.objectives,
                                                                               coordinates, rnd_distance,
                                                                               self.edges_weights_method.get(),
                                                                               edges_number)
                elif self.edges_gen_methods.get() == methods_options[1]:  # Fully Connected Dense Graph
                    self.edges_generated = adapter.generate_fully_connected_dense_graph(vertices_num,
                                                                                        self.bidir.get() == 1,
                                                                                        dest_directory, self.objectives,
                                                                                        coordinates, rnd_distance,
                                                                                        self.edges_weights_method.get())
                elif self.edges_gen_methods.get() == methods_options[2]:  # Fully Connected Graph
                    self.edges_generated = adapter.generate_fully_connected_graph(vertices_num, self.bidir.get() == 1,
                                                                                  dest_directory, self.objectives,
                                                                                  coordinates, rnd_distance,
                                                                                  self.edges_weights_method.get(),
                                                                                  self.edges_number_connected)
                elif self.edges_gen_methods.get() == methods_options[3]:  # Flow Network
                    self.edges_generated = adapter.generate_flow_network(vertices_num, self.bidir.get() == 1,
                                                                         dest_directory, self.objectives,
                                                                         coordinates, rnd_distance,
                                                                         self.edges_weights_method.get(),
                                                                         self.edges_flow_src, self.edges_flow_dst,
                                                                         self.edges_flow_paths)
                elif self.edges_gen_methods.get() == methods_options[5]:  # Bipartite Graph
                    self.edges_generated = adapter.generate_bipartite_graph(vertices_num, self.bidir.get() == 1,
                                                                            dest_directory, self.objectives,
                                                                            coordinates, rnd_distance,
                                                                            self.edges_weights_method.get(),
                                                                            self.edges_number_bipartite,
                                                                            self.edges_bipartite1,
                                                                            self.edges_bipartite2)

    def validate_input_graphs(self):
        if self.validate_vertices() and self.validate_coordinates():
            if not self.validate_params_edges_gen_method():
                tkinter.messagebox.showinfo(MSG_TITLE_INVALID_INPUT, "Invalid parameters for edges generation method.")
                return False
            else:
                return True
        else:
            return False

    def validate_input_grid(self):
        if not self.validate_params_edges_gen_method():
            tkinter.messagebox.showinfo(MSG_TITLE_INVALID_INPUT, "Invalid parameters for edges generation method.")
            return False
        else:
            return True

    def validate_coordinates(self):
        try:
            self.long = int(self.t_long.get('1.0', END))
            self.long_diff = int(self.t_long_diff.get('1.0', END))
            self.lat = int(self.t_lat.get('1.0', END))
            self.lat_diff = int(self.t_lat_diff.get('1.0', END))
            self.alt = int(self.t_alt.get('1.0', END))
            self.alt_diff = int(self.t_alt_diff.get('1.0', END))
            return True
        except:
            return False

    def validate_vertices(self):
        try:
            self.vertices = int(self.t_vertices.get())
        except:
            tkinter.messagebox.showinfo(MSG_TITLE_INVALID_INPUT, "Please insert a valid number of vertices.")
            return False
        if self.vertices <= 0:
            tkinter.messagebox.showinfo(MSG_TITLE_INVALID_INPUT, "Please insert a valid number of vertices.")
            return False
        else:
            return True

    def validate_params_edges_gen_method(self):
        if self.edges_gen_methods.get() == methods_options[0]:  # Fully Random - number/ percentage
            if self.edges_percentage and (self.edges_percentage_full_random <= 0 or self.edges_percentage_full_random >
                                          100):
                return False
            elif (not self.edges_percentage) and self.edges_number_full_random <= 0:
                return False
            return True
        elif self.edges_gen_methods.get() == methods_options[2]:  # Fully Connected Graph - add edges/ none
            if self.edges_method_full_connected.get() == 1 and self.edges_number_connected == 0:  # Additional edges
                return False
            else:
                return True
        elif self.edges_gen_methods.get() == methods_options[3]:  # Flow Network - src, dst, paths#
            if self.edges_flow_src > 0 and self.edges_flow_dst > 0 and self.edges_flow_paths > 0:
                return True
            else:
                return False
        elif self.edges_gen_methods.get() == methods_options[4]:  # Grid - grid params
            if self.grid_params.xs == 0:  # no parameters inserted
                return False
            else:
                return True
        elif self.edges_gen_methods.get() == methods_options[5]:  # Bipartite Graph - x:y
            try:
                values = str(self.edges_bipartite_txt).split(":")
                if len(values) == 2 and int(values[0]) > 0 and int(values[1]) > 0:
                    self.edges_bipartite1 = int(values[0])
                    self.edges_bipartite1 = int(values[1])
                    if self.t_edges_between_groups.get() != '':
                        self.edges_number_bipartite = int(self.t_edges_between_groups.get())
                        return True
                    else:
                        return False
                else:
                    return False
            except:
                return False
        else:  # Fully Connected Dense Graph - no params
            return True

    def get_fully_random_params(self):
        try:
            if self.edges_method_full_rnd_perc.get() == 0:  #
                self.edges_number_full_random = int(self.t_edges_number.get())
            else:
                self.edges_percentage_full_random = int(self.t_edges_percentage.get())
                self.edges_percentage = True
            self.edges_method_window.destroy()
        except:
            tkinter.messagebox.showinfo(title=MSG_TITLE_MISSING_PARAMS,
                                        message='Please make sure all fields are not empty.',
                                        parent=self.edges_method_window)

    def get_fully_connected_params(self):
        try:
            if self.edges_method_full_connected.get() == 1:  # MST + more
                self.edges_number_connected = int(self.t_add_edges_to_mst.get())
            self.edges_method_window.destroy()
        except:
            tkinter.messagebox.showinfo(title=MSG_TITLE_MISSING_PARAMS,
                                        message='Please make sure all fields are not empty.',
                                        parent=self.edges_method_window)

    def get_flow_params(self):
        try:
            self.edges_flow_src = int(self.t_edge_src.get())
            self.edges_flow_dst = int(self.t_edge_dst.get())
            self.edges_flow_paths = int(self.t_edge_paths_num.get())
            self.edges_method_window.destroy()
        except:
            tkinter.messagebox.showinfo(title=MSG_TITLE_MISSING_PARAMS,
                                        message='Please make sure all fields are not empty.',
                                        parent=self.edges_method_window)

    def get_bipartite_params(self):
        if self.t_edge_relation.get("1.0", END) != '\n':
            self.edges_bipartite_txt = self.t_edge_relation.get("1.0", END)
            try:
                values = str(self.edges_bipartite_txt).split(":")
                if len(values) == 2 and int(values[0]) > 0 and int(values[1]) > 0:
                    self.edges_bipartite1 = int(values[0])
                    self.edges_bipartite1 = int(values[1])
                    if self.t_edges_between_groups.get() != '':
                        self.edges_number_bipartite = int(self.t_edges_between_groups.get())
                    self.edges_method_window.destroy()
                else:
                    tkinter.messagebox.showinfo(title=MSG_TITLE_MISSING_PARAMS,
                                                message='Please make sure all fields are not empty.',
                                                parent=self.edges_method_window)
            except:
                tkinter.messagebox.showinfo(MSG_TITLE_INVALID_INPUT, "Invalid parameters.",
                                            parent=self.edges_method_window)
        else:
            tkinter.messagebox.showinfo(MSG_TITLE_INVALID_INPUT, "Invalid parameters.", parent=self.edges_method_window)

    def get_next_img(self):
        self.b_prev_img.config(state='normal')
        self.img_index += 1
        self.display_grid(self.json_dict, self.img_index)

    def get_prev_img(self):
        self.b_next_img.config(state='normal')
        if self.img_index == 2:  # indexes start from 1
            self.b_prev_img.config(state='disabled')
        self.img_index -= 1
        self.display_grid(self.json_dict, self.img_index)
        return

    def get_img_by_index(self):
        if self.t_img_goto.get() != '':
            index = int(self.t_img_goto.get())
            self.display_grid(self.json_dict, index)
            return
        else:
            tkinter.messagebox.showinfo("Missing Params", "Please insert a valid index to show.")

    def load_new_json(self):
        filetypes = (
            ('json files', '*.json'),
            ('All files', '*.*')
        )
        path_str = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        self.json_dict = adapter.get_input_graphs(os.path.normpath(path_str))
        self.display_grid(self.json_dict, 1)

    def disable_all_no_objectives(self):
        self.edges_weights_method.set(weights_options_graphs[3])
        self.om_edges_weights['menu'].entryconfigure(weights_options_graphs[0], state='disabled')
        self.om_edges_weights['menu'].entryconfigure(weights_options_graphs[1], state='disabled')
        self.om_edges_weights['menu'].entryconfigure(weights_options_graphs[2], state='disabled')
        self.rb_obj_set_values.config(state='disabled')
        self.rb_obj_default.config(state='disabled')

    def display_grid(self, json_dict, index, file_name=None):
        global dest_directory
        if index == -1:
            fig = grid_view.get_single_graph_image(json_dict, file_name, dest_directory)
        else:
            if json_dict.__contains__(str(index)):
                fig = grid_view.get_graph_image_by_index(json_dict, str(index), dest_directory)
            else:
                fig = Figure(figsize=(5, 4), dpi=100)
        if fig:
            canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
            canvas.draw()

            self.toolbar.destroy()
            self.toolbar = CustomToolbar(canvas, self.root, self)
            # self.toolbar.grid_remove()
            self.toolbar.update()
            canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
            canvas.mpl_connect("key_press_event", key_press_handler)

            canvas.get_tk_widget().grid(row=0, column=3, pady=2, padx=4, rowspan=18, columnspan=4)

            self.toolbar.grid(row=18, column=3, columnspan=4, pady=2, padx=4)
            if not json_dict.__contains__(str(index + 1)):
                self.b_next_img.config(state='disabled')
            else:
                self.b_next_img.config(state='normal')
        else:
            tkinter.messagebox.showinfo(MSG_TITLE_INVALID_INPUT, "No such graph.")

    def __init__(self, root):
        self.root = root
        self.root.title("Graph Generator")
        self.root.geometry("890x595")  # (width, height)
        # self.root.resizable(False, False)

        # Variables
        self.objectives = adapter.get_objectives()
        self.edges_number_full_random, self.edges_percentage_full_random, self.edges_number_connected, \
        self.edges_flow_src, self.edges_flow_dst, self.edges_flow_paths, self.edges_bipartite1, \
        self.edges_bipartite2, self.edges_bipartite_txt, self.edges_number_bipartite, self.vertices = 0, 0, 0, 0, \
                                                                                                      0, 0, 0, 0, \
                                                                                                      0, 0, 0
        self.edges_percentage = False
        self.long = LONG
        self.long_diff = COOR_DIFF
        self.lat = LAT
        self.lat_diff = COOR_DIFF
        self.alt = ALT
        self.alt_diff = ALT_DIFF
        self.edges_generated = []
        self.valid_grid_values = False
        self.grid_params = grid_params.Grid()
        self.img_index = 1
        self.queries_param = -1
        self.json_dict = adapter.get_input_graphs()

        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
        self.toolbar = CustomToolbar(canvas, self.root, self)

        self.b_next_img = Button(root, text="Next", command=self.get_next_img, width=10)

        self.display_grid(self.json_dict, self.img_index)

        Label(root, text="Vertices #").grid(row=row_index, column=0, pady=4, sticky=W)

        self.t_vertices = Prox(root, width=15)
        self.t_vertices.grid(row=row_index, column=1, padx=8, pady=4, sticky=W, columnspan=2)

        inc_row()

        Label(root, text="Objectives Values").grid(row=row_index, column=0, sticky=W)

        self.rb_obj_values = IntVar()
        self.rb_obj_default = Radiobutton(root, text="Default", value=0, variable=self.rb_obj_values,
                                          command=self.set_objectives_default)
        self.rb_obj_default.grid(row=row_index, column=1, padx=5, sticky=W)

        self.rb_obj_set_values = Radiobutton(root, text="Set Values", value=1, variable=self.rb_obj_values,
                                             command=lambda: self.set_objectives(0))
        self.rb_obj_set_values.grid(row=row_index, column=2, sticky=W)

        inc_row()

        Label(root, text="Edges Generation Method").grid(row=row_index, column=0, sticky=W)

        self.edges_gen_methods = StringVar(root)
        self.edges_gen_methods.set('- Select -')
        self.om_edges_methods = OptionMenu(root, self.edges_gen_methods, *methods_options,
                                           command=self.open_edges_method_window)
        self.om_edges_methods.config(width=25)
        self.om_edges_methods.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        inc_row()

        Label(root, text="Edges Weights").grid(row=row_index, column=0, sticky=W)

        self.edges_weights_method = StringVar(root)
        self.edges_weights_method.set(weights_options_graphs[0])
        self.om_edges_weights = OptionMenu(root, self.edges_weights_method, *weights_options_graphs)
        self.om_edges_weights.config(width=25)
        self.om_edges_weights.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        inc_row()

        self.bidir = IntVar()
        self.cb_bidirectional = Checkbutton(root, text="Bi-directional Graph", onvalue=1, offvalue=0,
                                            variable=self.bidir)
        self.cb_bidirectional.grid(row=row_index, column=0, columnspan=2, sticky=W)

        inc_row()

        Label(root, text="Coordinates").grid(row=row_index, column=0, sticky=NW, pady=4)

        Label(root, text="Longitude").grid(row=row_index, column=1, padx=8, sticky=W, pady=3)

        self.t_long = Text(root, height=1, width=11)
        self.t_long.insert(1.0, str(self.long))
        self.t_long.grid(row=row_index, column=2, padx=8, sticky=W, pady=3)

        inc_row()

        Label(root, text="Long diff").grid(row=row_index, column=1, padx=8, sticky=W)

        self.t_long_diff = Text(root, height=1, width=11)
        self.t_long_diff.insert(1.0, str(self.long_diff))
        self.t_long_diff.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        Label(root, text="Latitude").grid(row=row_index, column=1, padx=8, sticky=W)

        self.t_lat = Text(root, height=1, width=11)
        self.t_lat.insert(1.0, str(self.lat))
        self.t_lat.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        Label(root, text="Generate:").grid(row=row_index, column=0, sticky=W)

        Label(root, text="Lat diff").grid(row=row_index, column=1, padx=8, sticky=W)

        self.t_lat_diff = Text(root, height=1, width=11)
        self.t_lat_diff.insert(1.0, str(self.lat_diff))
        self.t_lat_diff.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        self.rb_coor = IntVar()
        self.rb_edges_num = Radiobutton(root, text="Randomly", value=0, variable=self.rb_coor)
        self.rb_edges_num.grid(row=row_index, column=0, sticky=W)

        Label(root, text="Altitude").grid(row=row_index, column=1, padx=8, sticky=W)

        self.t_alt = Text(root, height=1, width=11)
        self.t_alt.insert(1.0, str(self.alt))
        self.t_alt.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        self.rb_edges_num = Radiobutton(root, text="By Index", value=1, variable=self.rb_coor)
        self.rb_edges_num.grid(row=row_index, column=0, sticky=NW, rowspan=4)

        Label(root, text="Alt diff").grid(row=row_index, column=1, padx=8, sticky=W)

        self.t_alt_diff = Text(root, height=1, width=11)
        self.t_alt_diff.insert(1.0, str(self.alt_diff))
        self.t_alt_diff.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        Label(root, text='').grid(row=row_index, column=0, columnspan=3)

        inc_row()

        Label(root, text="Queries Generation Method").grid(row=row_index, column=0, sticky=NW, rowspan=4, pady=3)

        self.query_method = IntVar()
        self.rb_query_all_pairs = Radiobutton(root, text="All Pairs", value=0, variable=self.query_method,
                                              command=self.rb_query_all_pairs)
        self.rb_query_all_pairs.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        inc_row()

        self.rb_query_rnd = Radiobutton(root, text="Random (#)", value=1, variable=self.query_method,
                                        command=self.rb_query_number)
        self.rb_query_rnd.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        self.t_queries_num = Prox(root, width=10, state='readonly')
        self.t_queries_num.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        self.rb_query_min_edges = Radiobutton(root, text="Min Edges:", value=2, variable=self.query_method,
                                              command=self.rb_query_min_edges)
        self.rb_query_min_edges.grid(row=row_index, column=1, padx=8, sticky=W)

        self.t_min_edges_between = Prox(root, width=10, state='readonly')
        self.t_min_edges_between.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        self.rb_query_min_paths = Radiobutton(root, text="Min Paths:", value=3, variable=self.query_method,
                                              command=self.rb_query_min_paths)
        self.rb_query_min_paths.grid(row=row_index, column=1, padx=8, sticky=W)

        self.t_min_paths_between = Prox(root, width=10, state='readonly')
        self.t_min_paths_between.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        self.b_generate_queries = Button(root, text="Generate Query", width=27, command=self.generate_queries)
        self.b_generate_queries.grid(row=row_index, column=1, padx=8, pady=2, columnspan=2)

        inc_row()

        Label(root, text='').grid(row=row_index, column=0, columnspan=3)

        inc_row()

        self.b_clear = Button(root, text="Clear Form", command=self.clear, width=9)
        self.b_clear.grid(row=row_index, column=0, padx=8, pady=2, sticky=W)

        self.b_clear = Button(root, text="Load From", command=get_source_directory, width=10)
        self.b_clear.grid(row=row_index, column=2, padx=8, pady=2, sticky=E)

        inc_row()

        Label(root, text='').grid(row=row_index, column=0, columnspan=2)

        self.b_clear = Button(root, text="Save To", command=get_dest_directory, width=10)
        self.b_clear.grid(row=row_index, column=2, padx=8, pady=2, sticky=E)

        self.b_prev_img = Button(root, text="Prev", command=self.get_prev_img, width=10, state='disabled')
        self.b_prev_img.grid(row=row_index, column=4, padx=8, pady=2, sticky=E)

        self.b_next_img.grid(row=row_index, column=5, padx=8, pady=2, sticky=W)

        inc_row()

        self.b_save_graph = Button(root, text="Save Graph", command=self.save_graph_to, width=10, state='disabled')
        self.b_save_graph.grid(row=row_index, column=0, padx=8, pady=2, sticky=W)

        self.b_img_goto = Button(root, text="Go To:", command=self.get_img_by_index, width=7)
        self.b_img_goto.grid(row=row_index, column=3, padx=2, pady=2, sticky=E)

        self.t_img_goto = Prox(root, width=6)
        self.t_img_goto.grid(row=row_index, column=4, padx=2, sticky=W)

        self.b_load_json = Button(root, text="Load File", command=self.load_new_json, width=10)
        self.b_load_json.grid(row=row_index, column=6, columnspan=2, padx=6, pady=2, sticky=E)

        inc_row()

        self.b_generate = Button(root, text="Generate graph", command=self.generate_graph, width=16, bg='black',
                                 fg='white')
        self.b_generate.grid(row=row_index, column=0, columnspan=3, padx=8, pady=2)

        self.b_generate = Button(root, text="Create gif", command=self.create_gif, width=14)
        self.b_generate.grid(row=row_index, column=6, columnspan=2, padx=6, pady=2, sticky=E)

        # Objectives validation
        if len(self.objectives) == 0:
            tkinter.messagebox.showinfo("Read config failed", "Could not read objectives file, please check it and "
                                                              "re-run the program.")
            self.disable_all_no_objectives()
