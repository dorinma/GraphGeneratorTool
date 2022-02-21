from tkinter import *
from tkinter import filedialog as fd
import tkinter.messagebox
import os

import adapter

objectives_options = ('1', '2', '3', '4', '5')
methods_options = ('Fully Random', 'Fully Connected Dense Graph', 'Fully Connected', 'Flow Network',
                   'Grid Connection', 'Bipartite Graph')
weights_options = ('Fully Random', 'Planar', 'Predefined Calculation')
queries_options = ('Random', 'All Pairs', 'Minimal Edges')
source_directory, dest_directory = os.getcwd() + "\\out\\", os.getcwd() + "\\out\\"
row_index = 0
LONG = -74005973
LAT = 40712775
ALT = 10
COOR_DIFF = 1000
ALT_DIFF = 100


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


def validate_objective_range(min, max):
    if min > max:
        return False
    else:
        return True


class GUI:

    def clear(self):
        self.t_vertices.delete(0, 'end')
        self.obj.set(objectives_options[0])
        self.edges_gen_methods.set(methods_options[0])
        self.edges_gen_weights.set(weights_options[0])
        self.cb_bidirectional.deselect()

    # def disable_close(self):
    #     pass

    def open_edges_method_window(self, method):
        if method == methods_options[1]:  # Fully Connected Dense Graph - no params
            return

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
            Label(self.edges_method_window, text="Relation between sets of vertices, ").grid(row=row, column=0, padx=6,
                                                                                             pady=2, columnspan=2,
                                                                                             sticky=W)
            row += 1

            Label(self.edges_method_window, text="e.g. 1:1, 1:2 -").grid(row=row, column=0, padx=6, pady=2,
                                                                         columnspan=2,
                                                                         sticky=W)
            self.t_edge_relation = Text(self.edges_method_window, height=1, width=10)
            self.t_edge_relation.grid(row=row, column=1, padx=6, pady=2, sticky=E)
            # row += 1

            self.b_set_edges_m3 = Button(self.edges_method_window, text="Set", width=8,
                                         command=self.get_bipartite_params)
            self.b_set_edges_m3.grid(row=row, column=2, padx=4, pady=2, sticky=E)

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

    def save_objectives(self, number):
        num = int(number)
        missing_params = False
        # 1 objective
        if self.t_min_o1.get() == '' or self.t_max_o1.get() == '':
            missing_params = True
        else:
            self.min_o1 = int(self.t_min_o1.get())
            self.max_o1 = int(self.t_max_o1.get())

        if num > 1:
            # 2nd objective
            if self.t_min_o2.get() == '' or self.t_max_o2.get() == '':
                missing_params = True
            else:
                self.min_o2 = int(self.t_min_o2.get())
                self.max_o2 = int(self.t_max_o2.get())
            if num > 2:
                # 3rd objective
                if self.t_min_o3.get() == '' or self.t_max_o3.get() == '':
                    missing_params = True
                else:
                    self.min_o3 = int(self.t_min_o3.get())
                    self.max_o3 = int(self.t_max_o3.get())
                if num > 3:
                    # 4th objective
                    if self.t_min_o4.get() == '' or self.t_max_o4.get() == '':
                        missing_params = True
                    else:
                        self.min_o4 = int(self.t_min_o4.get())
                        self.max_o4 = int(self.t_max_o4.get())
                    if num > 4:
                        # 5th objective
                        if self.t_min_o5.get() == '' or self.t_max_o5.get() == '':
                            missing_params = True
                        else:
                            self.min_o5 = int(self.t_min_o5.get())
                            self.max_o5 = int(self.t_max_o5.get())
        if missing_params:
            tkinter.messagebox.showinfo("Missing parameters", "Please fill all fields then press \"Save\".",
                                        parent=self.objectives_window)
        elif validate_objective_range(self.min_o1, self.max_o1) and validate_objective_range(self.min_o2, self.max_o2) \
                and validate_objective_range(self.min_o3, self.max_o3) and validate_objective_range(self.min_o4,
                                                                                                    self.max_o4) \
                and validate_objective_range(self.min_o5, self.max_o5):
            self.objectives_window.destroy()
        else:
            tkinter.messagebox.showinfo("Illegal Values", "Min value must be lower/ equal to max for all objectives.",
                                        parent=self.objectives_window)

    def open_objectives_window(self, num):
        self.objectives_window = Toplevel(self.root)
        self.objectives_window.title("Objectives")
        win_width = int(num) * 25 + 60
        self.objectives_window.geometry("250x" + str(win_width))
        self.objectives_window.resizable(False, False)
        self.objectives_number = num
        self.min_o1, self.min_o2, self.min_o3, self.min_o4, self.min_o5 = -1, -1, -1, -1, -1
        self.max_o1, self.max_o2, self.max_o3, self.max_o4, self.max_o5 = -1, -1, -1, -1, -1
        # self.objectives_window.protocol("WM_DELETE_WINDOW", self.disable_close)

        row = 0
        Label(self.objectives_window, text="Insert min & max value for each objective:").grid(row=row, column=0,
                                                                                              pady=2, columnspan=5)
        row += 1
        Label(self.objectives_window, text="#1").grid(row=row, column=0, padx=4, pady=2)
        Label(self.objectives_window, text="min").grid(row=row, column=1, padx=6, pady=2)
        self.t_min_o1 = Prox(self.objectives_window, width=10)
        self.t_min_o1.grid(row=row, column=2)
        Label(self.objectives_window, text="max").grid(row=row, column=3, padx=4, pady=2)
        self.t_max_o1 = Prox(self.objectives_window, width=10)
        self.t_max_o1.grid(row=row, column=4)

        if int(num) > 1:
            row += 1
            Label(self.objectives_window, text="#2").grid(row=row, column=0, padx=4, pady=2)
            Label(self.objectives_window, text="min").grid(row=row, column=1, padx=6, pady=2)
            self.t_min_o2 = Prox(self.objectives_window, width=10)
            self.t_min_o2.grid(row=row, column=2)
            Label(self.objectives_window, text="max").grid(row=row, column=3, padx=4, pady=2)
            self.t_max_o2 = Prox(self.objectives_window, width=10)
            self.t_max_o2.grid(row=row, column=4)

            if int(num) > 2:
                row += 1
                Label(self.objectives_window, text="#3").grid(row=row, column=0, padx=4, pady=2)
                Label(self.objectives_window, text="min").grid(row=row, column=1, padx=6, pady=2)
                self.t_min_o3 = Prox(self.objectives_window, width=10)
                self.t_min_o3.grid(row=row, column=2)
                Label(self.objectives_window, text="max").grid(row=row, column=3, padx=4, pady=2)
                self.t_max_o3 = Prox(self.objectives_window, width=10)
                self.t_max_o3.grid(row=row, column=4)

                if int(num) > 3:
                    row += 1
                    Label(self.objectives_window, text="#4").grid(row=row, column=0, padx=4, pady=2)
                    Label(self.objectives_window, text="min").grid(row=row, column=1, padx=6, pady=2)
                    self.t_min_o4 = Prox(self.objectives_window, width=10)
                    self.t_min_o4.grid(row=row, column=2)
                    Label(self.objectives_window, text="max").grid(row=row, column=3, padx=4, pady=2)
                    self.t_max_o4 = Prox(self.objectives_window, width=10)
                    self.t_max_o4.grid(row=row, column=4)

                    if int(num) > 4:
                        row += 1
                        Label(self.objectives_window, text="#5").grid(row=row, column=0, padx=4, pady=2)
                        Label(self.objectives_window, text="min").grid(row=row, column=1, padx=6, pady=2)
                        self.t_min_o5 = Prox(self.objectives_window, width=10)
                        self.t_min_o5.grid(row=row, column=2)
                        Label(self.objectives_window, text="max").grid(row=row, column=3, padx=4, pady=2)
                        self.t_max_o5 = Prox(self.objectives_window, width=10)
                        self.t_max_o5.grid(row=row, column=4)
        row += 1
        Button(self.objectives_window, text="Save", command=lambda: self.save_objectives(num)).grid(row=row, column=0,
                                                                                                    columnspan=5,
                                                                                                    pady=2,
                                                                                                    sticky=E)

    def cb_query_min_edges(self):
        if self.query_min_edges.get() == 1:
            self.t_min_edges_between.config(state='normal')
        else:
            self.t_min_edges_between.config(state='readonly')

    def cb_query_number(self):
        if self.query_rnd.get() == 1:
            self.t_queries_num.config(state='normal')
        else:
            self.t_queries_num.config(state='readonly')

    def validate_queries(self):
        queries_num, min_edges = 0, 0
        valid = True
        if self.selected_queries[0] == 1:  # random
            if self.t_queries_num.get() != '':
                queries_num = int(self.t_queries_num.get())
                if queries_num <= 0:
                    valid = False
            else:
                valid = False
        if self.selected_queries[3] == 1:  # min edges between source & target
            if self.t_min_edges_between.get() != '':
                min_edges = int(self.t_min_edges_between.get())
                if min_edges <= 0:
                    valid = False
            else:
                valid = False
        if not valid:
            tkinter.messagebox.showinfo("Missing parameters", "Missing queries number or min edges between source and "
                                                              "target.")
        else:
            self.selected_queries[1] = queries_num
            self.selected_queries[4] = min_edges
        return valid

    def generate_queries(self):
        global dest_directory
        self.selected_queries = [self.query_rnd.get(), -1, self.query_all.get(), self.query_min_edges.get(), -1]
        if self.validate_queries():
            print("[DEBUG] Generating queries...")
            adapter.generate_queries(self.vertices, self.edges_generated, self.selected_queries, dest_directory)

    def generate_graph(self):
        global dest_directory

        objectives_ranges = [self.min_o1, self.max_o1, self.min_o2, self.max_o2, self.min_o3, self.max_o3,
                             self.min_o4, self.max_o4, self.min_o5, self.max_o5]
        if objectives_ranges[0] == -1:
            tkinter.messagebox.showinfo("Invalid Input", "Insert objective values.")
            return
        if self.validate_input():
            print("[DEBUG] Generating graph...")
            vertices_num = int(self.t_vertices.get())
            coordinates = [self.long, self.long_diff, self.lat, self.lat_diff, self.alt, self.alt_diff]
            rnd_distance = self.rb_coor.get() == 0  # Random
            if self.edges_gen_methods.get() == methods_options[0]:  # Fully Random
                edges_number = self.edges_number_full_random
                if self.edges_percentage:
                    edges_number = int((vertices_num * vertices_num) * self.edges_percentage_full_random / 100)
                self.edges_generated = adapter.generate_fully_random_graph(vertices_num, self.bidir.get() == 1,
                                                                           dest_directory,
                                                                           objectives_ranges,
                                                                           self.edges_gen_methods.get(), edges_number)
            elif self.edges_gen_methods.get() == methods_options[1]:  # Fully Connected Dense Graph
                self.edges_generated = adapter.generate_fully_connected_dense_graph(vertices_num, self.bidir.get() == 1,
                                                                                    dest_directory,
                                                                                    objectives_ranges,
                                                                                    self.edges_gen_methods.get())
            elif self.edges_gen_methods.get() == methods_options[2]:  # Fully Connected Graph
                self.edges_generated = adapter.generate_fully_connected_graph(vertices_num, self.bidir.get() == 1,
                                                                              dest_directory,
                                                                              objectives_ranges,
                                                                              self.edges_gen_methods.get(),
                                                                              self.edges_number_connected)
            elif self.edges_gen_methods.get() == methods_options[3]:  # Flow Network
                self.edges_generated = adapter.generate_flow_network(vertices_num, self.bidir.get() == 1,
                                                                     dest_directory, objectives_ranges,
                                                                     self.edges_gen_methods.get(), self.edges_flow_src,
                                                                     self.edges_flow_dst, self.edges_flow_paths)
            elif self.edges_gen_methods.get() == methods_options[5]:  # Bipartite Graph
                self.edges_generated = adapter.generate_bipartite_graph(vertices_num, self.bidir.get() == 1,
                                                                        dest_directory, objectives_ranges,
                                                                        self.edges_gen_methods.get(),
                                                                        self.edges_number_bipartite,
                                                                        self.edges_bipartite1, self.edges_bipartite2)
            else:  # Grid
                return

    def validate_input(self):
        if self.validate_vertices() and self.validate_coordinates():
            if not self.validate_params_edges_gen_method():
                tkinter.messagebox.showinfo("Invalid Input", "Invalid parameters for edges generation method.")
                return False
            else:
                return True
        else:
            return False

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
            tkinter.messagebox.showinfo("Invalid Input", "Please insert a valid number of vertices.")
            return False
        else:
            if self.vertices <= 0:
                tkinter.messagebox.showinfo("Invalid Input", "Please insert a valid number of vertices.")
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
        elif self.edges_gen_methods.get() == methods_options[3]:  # Flow Network - src, dst, paths #
            if self.edges_flow_src > 0 and self.edges_flow_dst > 0 and self.edges_flow_paths > 0:
                return True
            else:
                return False
        elif self.edges_gen_methods.get() == methods_options[5]:  # Bipartite Graph - x:y
            try:
                values = str(self.edges_bipartite_txt).split(":")
                if len(values) == 2 and int(values[0]) > 0 and int(values[1]) > 0:
                    self.edges_bipartite1 = int(values[0])
                    self.edges_bipartite1 = int(values[1])
                    return True
            except:
                return False

    def get_fully_random_params(self):
        if self.edges_method_full_rnd_perc.get() == 0:  #
            self.edges_number_full_random = int(self.t_edges_number.get())
        else:
            self.edges_percentage_full_random = int(self.t_edges_percentage.get())
            self.edges_percentage = True
        self.edges_method_window.destroy()

    def get_fully_connected_params(self):
        if self.edges_method_full_connected.get() == 1:  # MST + more
            self.edges_number_connected = int(self.t_add_edges_to_mst.get())
        self.edges_method_window.destroy()

    def get_flow_params(self):
        self.edges_flow_src = int(self.t_edge_src.get())
        self.edges_flow_dst = int(self.t_edge_dst.get())
        self.edges_flow_paths = int(self.t_edge_paths_num.get())
        self.edges_method_window.destroy()

    def get_bipartite_params(self):
        self.edges_bipartite_txt = self.t_edge_relation.get("1.0", END)
        self.edges_method_window.destroy()

    def __init__(self, root):
        self.root = root
        self.root.title("Graph Generator")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # Objectives
        self.objectives_number = 1
        self.t_min_o1 = Prox()
        self.t_min_o2 = Prox()
        self.t_min_o3 = Prox()
        self.t_min_o4 = Prox()
        self.t_min_o5 = Prox()
        self.min_o1, self.min_o2, self.min_o3, self.min_o4, self.min_o5 = -1, -1, -1, -1, -1
        self.t_max_o1 = Prox()
        self.t_max_o2 = Prox()
        self.t_max_o3 = Prox()
        self.t_max_o4 = Prox()
        self.t_max_o5 = Prox()
        self.max_o1, self.max_o2, self.max_o3, self.max_o4, self.max_o5 = -1, -1, -1, -1, -1

        self.edges_number_full_random = 0
        self.edges_percentage_full_random = 0
        self.edges_percentage = False
        self.edges_number_connected = 0
        self.edges_flow_src = 0
        self.edges_flow_dst = 0
        self.edges_flow_paths = 0
        self.edges_bipartite1 = 0
        self.edges_bipartite2 = 0
        self.edges_bipartite_txt = 0
        self.edges_number_bipartite = 0
        self.selected_queries = [0, 0, 0, 0, 0]
        self.long = LONG
        self.long_diff = COOR_DIFF
        self.lat = LAT
        self.lat_diff = COOR_DIFF
        self.alt = ALT
        self.alt_diff = ALT_DIFF
        self.vertices = 0
        self.edges_generated = []

        self.img = PhotoImage(file="tmp/1.png")
        self.img1 = self.img.subsample(1, 1)
        self.c = Canvas(root, bg="black", height=470, width=270)
        self.c.grid(row=0, column=3, rowspan=20, pady=2)
        self.c.create_image(50, 10, image=self.img1)

        Label(root, text="Vertices #").grid(row=row_index, column=0, sticky=W)

        self.t_vertices = Prox(root, width=15)
        self.t_vertices.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        inc_row()

        Label(root, text="Objectives #").grid(row=row_index, column=0, sticky=W)

        self.obj = StringVar(root)
        self.obj.set('- Select -')
        self.om_objectives = OptionMenu(root, self.obj, *objectives_options, command=self.open_objectives_window)
        self.om_objectives.config(width=9)
        self.om_objectives.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

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

        self.edges_gen_weights = StringVar(root)
        self.edges_gen_weights.set(weights_options[0])
        self.om_edges_weights = OptionMenu(root, self.edges_gen_weights, *weights_options)
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

        Label(root, text="Queries Generation Method").grid(row=row_index, column=0, sticky=NW, rowspan=3, pady=5)

        self.query_rnd = IntVar()
        self.cb_query_rnd = Checkbutton(root, text="Random (#)", onvalue=1, offvalue=0, variable=self.query_rnd,
                                        command=self.cb_query_number)
        self.cb_query_rnd.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        self.t_queries_num = Prox(root, width=10, state='readonly')
        self.t_queries_num.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        self.query_all = IntVar()
        self.cb_query_rnd = Checkbutton(root, text="All Pairs", onvalue=1, offvalue=0, variable=self.query_all)
        self.cb_query_rnd.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        inc_row()

        self.query_min_edges = IntVar()
        self.cb_query_rnd = Checkbutton(root, text="Min Edges:", onvalue=1, offvalue=0, variable=self.query_min_edges,
                                        command=self.cb_query_min_edges)
        self.cb_query_rnd.grid(row=row_index, column=1, padx=8, sticky=W)

        self.t_min_edges_between = Prox(root, width=10, state='readonly')
        self.t_min_edges_between.grid(row=row_index, column=2, padx=8, sticky=W)

        inc_row()

        self.b_generate_queries = Button(root, text="Generate Queries", width=27, command=self.generate_queries)
        self.b_generate_queries.grid(row=row_index, column=1, padx=8, pady=2, columnspan=2)

        Label(root, text='').grid(row=row_index, column=0, columnspan=3)

        inc_row()

        # Buttons
        self.b_clear = Button(root, text="Clear Form", command=self.clear, width=9)
        self.b_clear.grid(row=row_index, column=0, padx=8, pady=2, sticky=W)

        self.b_clear = Button(root, text="Load From", command=get_source_directory, width=10)
        self.b_clear.grid(row=row_index, column=2, padx=8, pady=2, sticky=E)

        inc_row()
        Label(root, text='').grid(row=row_index, column=0, columnspan=2)

        self.b_clear = Button(root, text="Save To", command=get_dest_directory, width=10)
        self.b_clear.grid(row=row_index, column=2, padx=8, pady=2, sticky=E)

        inc_row()

        self.b_generate = Button(root, text="Generate", command=self.generate_graph, width=9)
        self.b_generate.grid(row=row_index, column=0, padx=8, sticky=W)

        inc_row()
