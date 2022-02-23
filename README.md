# Graph Generator Tool
This tool generates graphs and writes them to three kinds of files: .gr, .co and queries.

The user can choose the method to create and weight the edges. Each method will be explained below, along with the parametes needed for it.

The costs of the edges can be defined by number of objectives, defined in a configuration file. The program does not support non-positive values.

For the program to run successfully, there must be two non-empty files in the resources directory: input.json and config.txt.

### input.json
This file is the source of the graphs displayed on the screen. It describes the states during the run of a search algorithm over a graph, and it is written as follows, where "1" is the index of the state, "Open" is the vertices in the open list, "Exp" is the next vertex to expand and "Children" are the neighbors of the Exp vertex.
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

### config.txt
This file must contain at least one record (line). Each line describes an objective, and must contain a name (could be anything) and minimal and maximal value for this objective (must be non-negative numbers). The fields are aeperated by a tab. Example for such file:
```yaml
Time	0	20
Cost	0	200
```

# Files Generated:

## .gr file
A .gr file represents the edges of the graph. Each row is an edge contains two vertices and the edge's weight by the specified objective.

For each objective the program will generate a single .gr file.

### Edges generation methods:

1. Fully Random - insert the amount of vertices and edges and the graph generated will contain edges scattered randomly.

2. Fully Connected Dense Graph - insert the amount of vertices and the graph will contain edges between every two vertices. 

3. Fully connected - the user can decide wether he wants the minimal spanning tree or the MST with additional edges (if so also insert the amount), so there is a path between every two vertices in the graph. 
   
4. Flow Network - insert source vertex, goal vertex and number of paths, and the graph will contain this number of paths between these two vertices. 

5. Grid Connection - the user can decide if the grid is in 2D or 3D and in how many axes the movement will be allowed (1/2 for 2D and 1/2/3 for 3D).
The user can decide how many blocks will appear in the grid. //The possible moves would be to empty cells and will written to the gr file. //?
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
   
4. By Coordinates - the value of the edge will be according to the coordinates of the vertices it is connected to. ////?

## .co file

The second file is co, represent the vertices. each row is a vertex - index of the vertex and it's coordinates (2 or 3). 



