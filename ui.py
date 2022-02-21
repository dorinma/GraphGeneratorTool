from tkinter import *
from tkinter import filedialog as fd
import tkinter.messagebox
import os

import adapter

objectives_options = ('1', '2', '3', '4', '5')
methods_options = ('Fully Random', 'Fully Connected Dense Graph', 'Fully Connected', 'Flow Network',
                   'Grid Connection', 'Bipartite Graph')
weights_options = ('Fully Random', 'Planar', 'Other Calculation')
queries_options = ('Random', 'All Pairs', 'Minimal Edges')
source_directory, dest_directory = os.getcwd() + "\\out\\", os.getcwd() + "\\out\\"
row_index = 0


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


class GUI:

    def clear(self):
        self.t_vertices.delete(0, 'end')
        self.obj.set(objectives_options[0])
        self.edges_gen_methods.set(methods_options[0])
        self.edges_gen_weights.set(weights_options[0])
        self.cb_bidirectional.deselect()
        self.t_queries.delete(0, 'end')
        self.queries.set(queries_options[0])

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
        if self.t_min_o1.get() == '' or self.t_max_o1.get() == '':
            if num > 1 and self.t_min_o2.get() == '' or self.t_max_o2.get() == '':
                if num > 2 and self.t_min_o3.get() == '' or self.t_max_o3.get() == '':
                    if num > 3 and self.t_min_o4.get() == '' or self.t_max_o4.get() == '':
                        if num > 4 and self.t_min_o5.get() == '' or self.t_max_o5.get() == '':
                            tkinter.messagebox.showinfo("Info", "Please fill all fields then press \"Save\".",
                                                        parent=self.objectives_window)
                    else:
                        tkinter.messagebox.showinfo("Info", "Please fill all fields then press \"Save\".",
                                                    parent=self.objectives_window)
                else:
                    tkinter.messagebox.showinfo("Info", "Please fill all fields then press \"Save\".",
                                                parent=self.objectives_window)
            else:
                tkinter.messagebox.showinfo("Info", "Please fill all fields then press \"Save\".",
                                            parent=self.objectives_window)
        else:
            tkinter.messagebox.showinfo("Info", "Please fill all fields then press \"Save\".",
                                        parent=self.objectives_window)

    def open_objectives_window(self, num):
        self.objectives_window = Toplevel(self.root)
        self.objectives_window.title("Objectives")
        win_width = int(num) * 25 + 60
        self.objectives_window.geometry("250x" + str(win_width))
        self.objectives_window.resizable(False, False)
        self.objectives_number = num
        # self.objectives_window.protocol("WM_DELETE_WINDOW", self.disable_close)

        row = 0
        Label(self.objectives_window, text="Insert min & max values for each objective:").grid(row=row, column=0,
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

    def generate_graph(self):
        global dest_directory

        if self.validate_input():
            print("[DEBUG] Generating...")
            vertices_num = int(self.t_vertices.get())
            if self.edges_gen_methods.get() == methods_options[0]:  # Fully Random
                edges_number = self.edges_number_full_random
                if self.edges_percentage:
                    edges_number = int((vertices_num * vertices_num) * self.edges_percentage_full_random / 100)
                adapter.generate_fully_random_graph(vertices_num, self.bidir.get() == 1, dest_directory,
                                                    self.edges_gen_methods.get(), edges_number)
            elif self.edges_gen_methods.get() == methods_options[1]:  # Fully Connected Dense Graph
                adapter.generate_fully_connected_dense_graph(vertices_num, self.bidir.get() == 1, dest_directory,
                                                             self.edges_gen_methods.get())
            elif self.edges_gen_methods.get() == methods_options[2]:  # Fully Connected Graph
                adapter.generate_fully_connected_graph(vertices_num, self.bidir.get() == 1, dest_directory,
                                                       self.edges_gen_methods.get(), self.edges_number_connected)
            elif self.edges_gen_methods.get() == methods_options[3]:  # Flow Network
                adapter.generate_flow_network(vertices_num, self.bidir.get() == 1, dest_directory,
                                              self.edges_gen_methods.get(), self.edges_flow_src, self.edges_flow_dst,
                                              self.edges_flow_paths)
            elif self.edges_gen_methods.get() == methods_options[5]:  # Bipartite Graph
                adapter.generate_bipartite_graph(vertices_num, self.bidir.get() == 1, dest_directory,
                                                 self.edges_gen_methods.get(), self.edges_number_bipartite,
                                                 self.edges_bipartite1, self.edges_bipartite2)
            else:  # Grid
                return

    def validate_input(self):
        if self.validate_vertices() and self.validate_params() and self.validate_objectives_ranges():
            return True
        else:
            return False

    def validate_vertices(self):
        vertices = ''
        try:
            vertices = int(self.t_vertices.get())
        except:
            tkinter.messagebox.showinfo("Invalid Input", "Please insert a valid number of vertices.")
            return False
        else:
            if vertices <= 0:
                tkinter.messagebox.showinfo("Invalid Input", "Please insert a valid number of vertices.")
                return False
            else:
                return True

    def validate_params(self):
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
            # t.remove('\n')
            # print(int(t[0]))
            # print(int(t[1]))
            # try:
            #     values = self.t_edge_relation.get(1.0, END).split(":")
            #     if len(values) == 2 and int(values[0]) > 0 and int(values[1]) > 0:
            #         return True
            # except:
            #     return False

    def validate_objectives_ranges(self):
        return True
    #     valid = [True] * self.objectives_number
    #     try:
    #         if self.t_min_o1 != '' and self.t_max_o1 != '':
    #             self.min_o1 = int(self.t_min_o1.get())
    #             self.max_o1 = int(self.t_max_o1.get())
    #             if self.objectives_number > 1:
    #                 if self.t_min_o2 != '' and self.t_max_o2 != '':
    #                     self.min_o2 = int(self.t_min_o2.get())
    #                     self.max_o2 = int(self.t_max_o2.get())
    #                     if self.objectives_number > 2:
    #                         if self.t_min_o3 != '' and self.t_max_o3 != '':
    #                             self.min_o3 = int(self.t_min_o3.get())
    #                             self.max_o3 = int(self.t_max_o3.get())
    #                             if self.objectives_number > 3:
    #                                 if self.t_min_o4 != '' and self.t_max_o4 != '':
    #                                     self.min_o4 = int(self.t_min_o4.get())
    #                                     self.max_o4 = int(self.t_max_o4.get())
    #                                     if self.objectives_number > 4:
    #                                         if self.t_min_o5 != '' and self.t_max_o5 != '':
    #                                             self.min_o5 = int(self.t_min_o5.get())
    #                                             self.max_o5 = int(self.t_max_o5.get())
    #                                         else:
    #                                             return False
    #                                 else:
    #                                     return False
    #                         else:
    #                             return False
    #                 else:
    #                     return False
    #         else:
    #             return False
    #     except:
    #         return False

    def get_fully_random_params(self):
        if self.edges_method_full_rnd_perc.get() == 0:  #
            self.edges_number_full_random = int(self.t_edges_number.get())
        else:
            self.edges_percentage_full_random = int(self.t_edges_percentage.get())
            self.edges_percentage = True
        self.edges_method_window.destroy()

    def get_fully_connected_params(self):
        if self.edges_method_full_connected.get() == 1:  # MST + more
            self.edges_number_connected = self.t_add_edges_to_mst.get()
        self.edges_method_window.destroy()

    def get_flow_params(self):
        self.edges_flow_src = self.t_edge_src.get()
        self.edges_flow_dst = self.t_edge_dst.get()
        self.edges_flow_paths = self.t_edge_paths_num.get()
        self.edges_method_window.destroy()

    def get_bipartite_params(self):
        self.edges_bipartite_txt = self.t_edge_relation.get("1.0", END)
        self.edges_method_window.destroy()

    def __init__(self, root):
        self.root = root
        self.root.title("Graph Generator")
        self.root.geometry("650x410")
        self.root.resizable(False, False)

        # Objectives
        self.objectives_number = 1
        self.t_min_o1 = Prox()
        self.t_min_o2 = Prox()
        self.t_min_o3 = Prox()
        self.t_min_o4 = Prox()
        self.t_min_o5 = Prox()
        self.min_o1, self.min_o2, self.min_o3, self.min_o4, self.min_o5 = 0, 0, 0, 0, 0
        self.t_max_o1 = Prox()
        self.t_max_o2 = Prox()
        self.t_max_o3 = Prox()
        self.t_max_o4 = Prox()
        self.t_max_o5 = Prox()
        self.max_o1, self.max_o2, self.max_o3, self.max_o4, self.max_o5 = 0, 0, 0, 0, 0

        # self.t_edges_number = Prox()
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

        self.img = PhotoImage(file="1.png")
        self.img1 = self.img.subsample(1, 1)
        self.c = Canvas(root, bg="black", height=370, width=270)
        self.c.grid(row=0, column=3, rowspan=13, pady=2)
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

        Label(root, text="Queries #").grid(row=row_index, column=0, sticky=W)

        self.t_queries = Prox(root, width=15)
        self.t_queries.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        inc_row()

        Label(root, text="Queries Generation Method").grid(row=row_index, column=0, sticky=W)

        self.queries = StringVar(root)
        self.queries.set(queries_options[0])
        self.om_queries = OptionMenu(root, self.queries, *queries_options)
        self.om_queries.config(width=25)
        self.om_queries.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        inc_row()

        Label(root, text='').grid(row=row_index, column=0, columnspan=3)

        inc_row()

        # Buttons
        self.b_clear = Button(root, text="Clear Form", command=self.clear, width=9)
        self.b_clear.grid(row=row_index, column=0, padx=8, sticky=W)

        self.b_clear = Button(root, text="Save To", command=get_dest_directory, width=9)
        self.b_clear.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        inc_row()

        Label(root, text='').grid(row=row_index, column=0, columnspan=3)

        inc_row()

        self.b_generate = Button(root, text="Generate", command=self.generate_graph, width=9)
        self.b_generate.grid(row=row_index, column=0, padx=8, sticky=W)

        self.b_clear = Button(root, text="Load From", command=get_source_directory, width=9)
        self.b_clear.grid(row=row_index, column=1, padx=8, sticky=W, columnspan=2)

        inc_row()
