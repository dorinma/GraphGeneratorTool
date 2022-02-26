# Graph Generator Tool
This tool generates graphs and writes them to three kinds of files: .gr, .co and queries.
The user can choose the method to create and weight the edges. Each method will be explained below, along with the parametes needed for it.
The costs of the edges can be determined by number of objectives, defined in a configuration file. The program does not support non-positive values.

This tool also allows displaying graphs represented in a file described below, more on this under 'Graphs Display'.

For the program to run successfully, there must be a non-empty file in the resources directory: config.txt. There is also an input.json file in the same directory, used for displaying graphs on the screen. This file may be empty but in this case no graph will be shown.

### config.txt
This file must contain at least one record (line). Each line describes an objective, and will contain a name (could be anything) and minimal and maximal values for this objective (non-negative numbers). The fields are seperated by a tab. Example for such file:
```yaml
Time	0	20
Cost	0	200
```

### input.json
This file is the source of the graphs displayed on the screen. It describes the states during the run of a search algorithm over a graph, and it is written as follows, where "1" is the index of the state, "Open" are the vertices in the open list, "Exp" is the next vertex to expand and "Children" are the neighbors of the Exp vertex. The indexes must start from "1".
```yaml
{
  "1": {
    "Open": [[1, 2], [2, 4], [3, 6]],
    "Exp": [6, 8],
    "Children": [[2, 3], [3, 4], [4, 5]]
  },
  "2": {
    "Open": [[1, 2], [2, 4], [3, 6], [6, 8]],
    "Exp": [2, 3],
    "Children": [[3, 4], [4, 5]]
  }
}
```

# Graphs Generation:

## Files Generated:

## .gr file
A .gr file represents the edges of the graph. Each row is an edge contains two vertices and the edge's weight by the specified objective.

For each objective the program will generate a single .gr file.

### Edges generation methods:

1. Fully Random - insert the amount of vertices and edges and the graph generated will contain edges scattered randomly.

2. Fully Connected Dense Graph - insert the amount of vertices and the graph will contain edges between every two vertices. 

3. Fully connected - the user can decide wether he wants the minimal spanning tree or the MST with additional edges (if so also insert the amount), so there is a path between every two vertices in the graph. 
   
4. Flow Network - insert source vertex, goal vertex and number of paths, and the graph will contain this number of paths between these two vertices. 

5. Grid Connection - the user can decide if the grid is in 2D or 3D and in how many axes the movement will be allowed (1/2 for 2D and 1/2/3 for 3D).
The user can decide how many blocks will appear in the grid. The possible moves will be only to empty cells, where there are no blocks, and will be written to the .gr file.
The user can also decide what would be the edges' weights: random values between min and max he'll insert or 1 for each axis he moves in.
   
6. Bipartite Graph - insert a relation between two sets of vertices and number of edges between sets. The graph will contain edges from the first set to 
the other (or the oposit direction) but not to the same set. 
   
   
### Edges weight methods:

Then there are several options of how to weight the edges, when the minimal and maximal values for the weight are given in the config file.

1. Fully Random - as written above, every objective has min and the max values, and every edge will get a random value within this range. 

2. Planar - the edges will apply the triangular inequivalence. The user inserts min and max values and for every three edges that are connected in a triangle: 
the sum of two of them will be larger than the third. 
   
3. Index Differnce - insert min and max values and the edges will get a value relate to the differnce between the indexes of the vertices, meaning that adjacent 
vertices will get a higher weight. 
   
4. By Coordinates - the value of the edge will be according to the coordinates of the vertices it is connected to (the actual distance between them).

## .co file

The second file generated is a .co file, representing the vertices. Each row describes a vertex: its index and coordinates (2 or 3). 

### Coordinates generation methods:

1. Randomly - the default coordinated shown are N.Y. coordinates (longitude, latitude and altitude), and the values for the possible distance differnece from them.

   The user can change both kinds of valus, and each vertex will get coordinates randomly within this range. 
   
   If only two coordinates are needed, one can insert 0 for the alt & alt diff fields.
   
2. By Index - the values are the same as describe above. Each vertex will get coordinates in this range, when in this case close vertices (by index) will get closer 

   coordinates. 
   
3. For the grid case, the coordinates file will be according to the x, y, z.   

## query file

The third file generated is query (with no type). Each row represents a pair of vertices- source and target. 

### Queries generation methods:

1. All Pairs - all combinations of every two vertices in the graph. 

2. Random - insert number of pairs and get this number of pairs choosen randomly. 

3. Min Edges - insert the number of mininal edges between source & target vertices. The pairs generated will be pairs of vertices that have paths with at least this number of edges between them. 
   
4. Min Paths - insert the number of minimal paths between source & target vertices. The pairs generated will be pairs of vertices that have at least this number of paths between them. 


# Graphs Display:

On the right side of the screen there is a canves containing graph visualisation of graphs generated from input.json file (was mentioned above). When running, the program will read the .json file from the 'config' folder and display the first graph described there. There are options to navigate graphs within this file. 

Also, there are possibilities to display another single graph or to read an entire .json file and navigate graphs within this new file. Each graph that is displayed on the screen will also be saved as a .png image to the 'out' folder under its name (index/ file name if single graph). Later on, the user can create a gif of these images: he will choose a directory and the program will create gif from all images (of type .png) in this directory by their order of appearance. The gif will also be saved in the 'out' folder.

