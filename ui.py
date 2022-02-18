from tkinter import *
from tkinter import filedialog as fd

objectives_options = ('1', '2', '3', '4')

methods_options = ('Fully Random', 'Fully Connected Dense Graph', 'Fully Connected', 'Flow Network', 'Planar Connection',
                   'Grid Connection', 'Bipartite Graph')

weights_options = ('Fully Random', 'Computed Value (planar/grid)', 'Other Calculation')

queries_options = ('Random', 'All Pairs', 'Minimal Edges')


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

# def get_txt():
#     l_temp.config(text=t_vertices.get(1.0, END))


root = Tk()
root.title("Graph Generator")
root.geometry("550x500")

img = PhotoImage(file="1.png")
img1 = img.subsample(2, 2)
c = Canvas(root, bg="black", height=260, width=220)
c.grid(row=0, column=2, rowspan=6)
c.create_image(50, 10, image=img1)

l_vertices = Label(root, text="Vertices #")
l_vertices.grid(row=0, column=0, sticky=W, pady=2)

t_vertices = Text(root, height=1, width=12)
t_vertices.grid(row=0, column=1, pady=2, padx=8)

l_objectives = Label(root, text="Objectives #")
l_objectives.grid(row=1, column=0, sticky=W, pady=2)

obj = StringVar(root)
obj.set(objectives_options[0])
om_objectives = OptionMenu(root, obj, *objectives_options)
om_objectives.grid(row=1, column=1, pady=2, padx=8)

l_edges_methods = Label(root, text="Edges Generation Method")
l_edges_methods.grid(row=2, column=0, sticky=W, pady=2)

edges_gen_methods = StringVar(root)
edges_gen_methods.set(methods_options[0])
om_edges_methods = OptionMenu(root, edges_gen_methods, *methods_options)
om_edges_methods.grid(row=2, column=1, pady=2, padx=8)

l_edges_weights = Label(root, text="Edges Weights")
l_edges_weights.grid(row=3, column=0, sticky=W, pady=2)

edges_gen_weights = StringVar(root)
edges_gen_weights.set(weights_options[0])
om_edges_weights = OptionMenu(root, edges_gen_weights, *weights_options)
om_edges_weights.grid(row=3, column=1, pady=2, padx=8)

cb_bidirectional = Checkbutton(root, text="Bi-directional Graph", onvalue=1, offvalue=0)
cb_bidirectional.grid(row=4, column=0, columnspan=2)

l_queries = Label(root, text="Queries #")
l_queries.grid(row=5, column=0, sticky=W, pady=2)

t_queries = Text(root, height=1, width=12)
t_queries.grid(row=5, column=1, pady=2, padx=8)

l_queries_method = Label(root, text="Queries Generation Method")
l_queries_method.grid(row=6, column=0, sticky=W, pady=2)

queries = StringVar(root)
queries.set(queries_options[0])
om_queries = OptionMenu(root, queries, *queries_options)
om_queries.grid(row=6, column=1, pady=2, padx=8)

# Buttons
b_clear = Button(root, text="Clear Form", command=clear)
b_clear.grid(row=10, column=0, pady=2)

b_generate = Button(root, text="Generate", command=generate)
b_generate.grid(row=10, column=1, pady=2)

root.mainloop()
