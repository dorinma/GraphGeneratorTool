from tkinter import *
from tkinter import filedialog as fd
import tkinter.messagebox

import adapter

objectives_options = ('1', '2', '3', '4', '5')
objectives_names = ('obj1', 'obj2', 'obj3', 'obj4', 'obj5')
methods_options = ('Fully Random', 'Fully Connected Dense Graph', 'Fully Connected', 'Flow Network',
                   'Planar Connection', 'Grid Connection', 'Bipartite Graph')
weights_options = ('Fully Random', 'Computed Value (planar/grid)', 'Other Calculation')
queries_options = ('Random', 'All Pairs', 'Minimal Edges')
source_directory = "/"
dest_directory = "/"
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
    # print(source_directory)


def get_dest_directory():
    dest_directory = fd.askdirectory()
    # print(dest_directory)


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

    # def disable_close(self):
    #     pass

    def open_objectives_window(self, num):
        self.objectives_window = Toplevel(self.root)
        self.objectives_window.title("Objectives Ranges")
        win_width = int(num) * 25 + 60
        self.objectives_window.geometry("250x" + str(win_width))
        self.objectives_window.resizable(False, False)
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
        print("Generating...")
        vertices = ''
        valid_vertices = False
        try:
            vertices = int(self.t_vertices.get())
        except:
            tkinter.messagebox.showinfo("Invalid Input", "Please insert a valid number of vertices.")
        else:
            if vertices <= 0:
                tkinter.messagebox.showinfo("Invalid Input", "Please insert a valid number of vertices.")
                return
            else:
                valid_vertices = True
        if valid_vertices:
            if self.edges_gen_methods.get() == methods_options[0]:  # Fully Random
                adapter.fully_random(vertices, 0, self.bidir.get() == 1)
            elif self.edges_gen_methods.get() == methods_options[1]:  # Fully Connected Dense Graph
                adapter.fully_connected_dense_graph(vertices)

    def __init__(self, root):
        self.root = root
        self.root.title("Graph Generator")
        self.root.geometry("650x410")
        self.root.resizable(False, False)

        # Objectives
        self.t_min_o1 = Prox()
        self.t_min_o2 = Prox()
        self.t_min_o3 = Prox()
        self.t_min_o4 = Prox()
        self.t_min_o5 = Prox()
        self.t_max_o1 = Prox()
        self.t_max_o2 = Prox()
        self.t_max_o3 = Prox()
        self.t_max_o4 = Prox()
        self.t_max_o5 = Prox()

        self.img = PhotoImage(file="1.png")
        self.img1 = self.img.subsample(1, 1)
        self.c = Canvas(root, bg="black", height=370, width=270)
        self.c.grid(row=0, column=2, rowspan=11, pady=2)
        self.c.create_image(50, 10, image=self.img1)

        self.l_vertices = Label(root, text="Vertices #")
        self.l_vertices.grid(row=row_index, column=0, sticky=W)

        self.t_vertices = Prox(root, width=15)
        self.t_vertices.grid(row=row_index, column=1, padx=8, sticky=W)

        inc_row()

        self.l_objectives = Label(root, text="Objectives #")
        self.l_objectives.grid(row=row_index, column=0, sticky=W)

        self.obj = StringVar(root)
        self.obj.set('- Choose -')
        self.om_objectives = OptionMenu(root, self.obj, *objectives_options, command=self.open_objectives_window)
        self.om_objectives.config(width=9)
        self.om_objectives.grid(row=row_index, column=1, padx=8, sticky=W)

        inc_row()

        self.l_edges_methods = Label(root, text="Edges Generation Method")
        self.l_edges_methods.grid(row=row_index, column=0, sticky=W)

        self.edges_gen_methods = StringVar(root)
        self.edges_gen_methods.set(methods_options[0])
        self.om_edges_methods = OptionMenu(root, self.edges_gen_methods, *methods_options)
        self.om_edges_methods.config(width=25)
        self.om_edges_methods.grid(row=row_index, column=1, padx=8, sticky=W)

        inc_row()

        self.l_edges_weights = Label(root, text="Edges Weights")
        self.l_edges_weights.grid(row=row_index, column=0, sticky=W)

        self.edges_gen_weights = StringVar(root)
        self.edges_gen_weights.set(weights_options[0])
        self.om_edges_weights = OptionMenu(root, self.edges_gen_weights, *weights_options)
        self.om_edges_weights.config(width=25)
        self.om_edges_weights.grid(row=row_index, column=1, padx=8, sticky=W)

        inc_row()
        self.bidir = IntVar()
        self.cb_bidirectional = Checkbutton(root, text="Bi-directional Graph", onvalue=1, offvalue=0,
                                            variable=self.bidir)
        self.cb_bidirectional.grid(row=row_index, column=0, columnspan=2, sticky=W)

        inc_row()

        self.l_queries = Label(root, text="Queries #")
        self.l_queries.grid(row=row_index, column=0, sticky=W)

        self.t_queries = Prox(root, width=15)
        self.t_queries.grid(row=row_index, column=1, padx=8, sticky=W)

        inc_row()

        self.l_queries_method = Label(root, text="Queries Generation Method")
        self.l_queries_method.grid(row=row_index, column=0, sticky=W)

        self.queries = StringVar(root)
        self.queries.set(queries_options[0])
        self.om_queries = OptionMenu(root, self.queries, *queries_options)
        self.om_queries.config(width=25)
        self.om_queries.grid(row=row_index, column=1, padx=8, sticky=W)

        inc_row()

        self.l_ph1 = Label(root, text='')
        self.l_ph1.grid(row=row_index, column=0, columnspan=3)

        inc_row()

        # Buttons
        self.b_clear = Button(root, text="Clear Form", command=self.clear, width=9)
        self.b_clear.grid(row=row_index, column=0, padx=8, sticky=W)

        self.b_clear = Button(root, text="Save To", command=get_dest_directory, width=9)
        self.b_clear.grid(row=row_index, column=1, padx=8, sticky=W)

        inc_row()

        self.l_ph2 = Label(root, text='')
        self.l_ph2.grid(row=row_index, column=0, columnspan=3)

        inc_row()

        self.b_generate = Button(root, text="Generate", command=self.generate_graph, width=9)
        self.b_generate.grid(row=row_index, column=0, padx=8, sticky=W)

        self.b_clear = Button(root, text="Load From", command=get_source_directory, width=9)
        self.b_clear.grid(row=row_index, column=1, padx=8, sticky=W)

        inc_row()
