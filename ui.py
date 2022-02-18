from tkinter import *
from tkinter import filedialog as fd

objectives_options = ('1', '2', '3', '4')

methods_options = (
    'Fully Random', 'Fully Connected Dense Graph', 'Fully Connected', 'Flow Network', 'Planar Connection',
    'Grid Connection', 'Bipartite Graph')

weights_options = ('Fully Random', 'Computed Value (planar/grid)', 'Other Calculation')

queries_options = ('Random', 'All Pairs', 'Minimal Edges')

source_directory = "/"

dest_directory = "/"

row_index = 0


def clear():
    t_vertices.delete(1.0, END)
    obj.set(objectives_options[0])
    edges_gen_methods.set(methods_options[0])
    edges_gen_weights.set(weights_options[0])
    cb_bidirectional.deselect()
    t_queries.delete(1.0, END)
    queries.set(queries_options[0])


def generate():
    print("generating")


def get_source_directory():
    source_directory = fd.askdirectory()
    print(source_directory)


def get_dest_directory():
    dest_directory = fd.askdirectory()
    print(dest_directory)


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


# def get_txt():
#     l_temp.config(text=t_vertices.get(1.0, END))


root = Tk()
root.title("Graph Generator")
root.geometry("650x410")

img = PhotoImage(file="1.png")
img1 = img.subsample(2, 2)
c = Canvas(root, bg="black", height=260, width=220)
c.grid(row=0, column=2, rowspan=7)
c.create_image(50, 10, image=img1)

l_vertices = Label(root, text="Vertices #")
l_vertices.grid(row=row_index, column=0, sticky=W)

# t_vertices = Text(root, height=1, width=12)
t_vertices = Prox(root, width=15)
t_vertices.grid(row=row_index, column=1, padx=8, sticky=W)

row_index += 1

l_objectives = Label(root, text="Objectives #")
l_objectives.grid(row=row_index, column=0, sticky=W)

obj = StringVar(root)
obj.set(objectives_options[0])
om_objectives = OptionMenu(root, obj, *objectives_options)
om_objectives.config(width=25)
om_objectives.grid(row=row_index, column=1, padx=8, sticky=W)

row_index += 1

l_edges_methods = Label(root, text="Edges Generation Method")
l_edges_methods.grid(row=row_index, column=0, sticky=W)

edges_gen_methods = StringVar(root)
edges_gen_methods.set(methods_options[0])
om_edges_methods = OptionMenu(root, edges_gen_methods, *methods_options)
om_edges_methods.config(width=25)
om_edges_methods.grid(row=row_index, column=1, padx=8, sticky=W)

row_index += 1

l_edges_weights = Label(root, text="Edges Weights")
l_edges_weights.grid(row=row_index, column=0, sticky=W)

edges_gen_weights = StringVar(root)
edges_gen_weights.set(weights_options[0])
om_edges_weights = OptionMenu(root, edges_gen_weights, *weights_options)
om_edges_weights.config(width=25)
om_edges_weights.grid(row=row_index, column=1, padx=8, sticky=W)

row_index += 1

cb_bidirectional = Checkbutton(root, text="Bi-directional Graph", onvalue=1, offvalue=0)
cb_bidirectional.grid(row=row_index, column=0, columnspan=2, sticky=W)

row_index += 1

l_queries = Label(root, text="Queries #")
l_queries.grid(row=row_index, column=0, sticky=W)

t_queries = Prox(root, width=15)
t_queries.grid(row=row_index, column=1, padx=8, sticky=W)

row_index += 1

l_queries_method = Label(root, text="Queries Generation Method")
l_queries_method.grid(row=row_index, column=0, sticky=W)

queries = StringVar(root)
queries.set(queries_options[0])
om_queries = OptionMenu(root, queries, *queries_options)
om_queries.config(width=25)
om_queries.grid(row=row_index, column=1, padx=8, sticky=W)

row_index += 1

l_ph1 = Label(root, text='')
l_ph1.grid(row=row_index, column=0, columnspan=3)

row_index += 1

# Buttons
b_clear = Button(root, text="Clear Form", command=clear)
b_clear.grid(row=row_index, column=0, padx=8, sticky=W)

b_clear = Button(root, text="Save To", command=get_dest_directory)
b_clear.grid(row=row_index, column=1, padx=8, sticky=W)

row_index += 1

l_ph2 = Label(root, text='')
l_ph2.grid(row=row_index, column=0, columnspan=3)

row_index += 1

b_generate = Button(root, text="Generate", command=generate)
b_generate.grid(row=row_index, column=0, padx=8, sticky=W)

b_clear = Button(root, text="Load From", command=get_source_directory)
b_clear.grid(row=row_index, column=1, padx=8, sticky=W)

row_index += 1

root.mainloop()
