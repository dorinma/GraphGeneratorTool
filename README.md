# GraphGeneratorTool
This tool made for generating different kinds of graphs by returning 3 kind of files. 

## Gr file

The first file is gr, represent the edges. each row is an edge - 2 vertices, with differnt weight. 

This tool give the option to insert more than one objective, each represent a differnet "price" of the edge like distance or time. 

Each objective need the min value and the max value so the objective be like real data,

and each of them will written to a differnt gr file. 

There are number of options of how to organzied the edges : 

1. Fully Randdom - the user insert the amount of vertices and the amount of edges and the graph will contain edges scattered randomly.

2. Fully Connected Dense Graph - the user insert the amount of vertices and the graph will contain edges between every two vertices. 

3. Fully connected - the user can decide rather he want just the minimal spanning tree or another edges (if so insert the amount),

   so there is a path between every two vertices in the graph. 
   
4. Flow Network - the user insert source vertex, goal vertex and number of paths, and the graph will contain this number of paths

   between those two vertices. 

5. Grid Connection - the user can decide if the grid is 2D or 3D and in how many axes he can move in one step (1,2 for 2D and 1,2,3 for 3D).

   The user can also decide how many blocks will be. The possible moves woul'd be to empty cells and will written to the gr file. 
   
   The user can also decide what would be the edge's weight, random value between min and max he'll give or 1 for each axis he move.
   
6. Bipartite Graph - the user insert a relation between two sets of vertices number of edges. The graph will contain edges from the first set to 

   the other, or the oposit, but not to the same set. 
   
   
Than,There are number of options of how to organzied the edges : (insert min value and max value is throgh config file)

1. Fully Random - As written above every objective need the min value and the max value. every edge will get a random value in this range. 

2. Planar - the edges will apply the triangular inequivalence. The user insert min value and max value and for every 3 edges that connected to triangle 

   the sum of two of then will be larger than the third. 
   
3. Index Differnce - the user insert min value and max value ans the edges will get a value relate the differnce in the indexes of the vertices.

   Thats mean that adjacent vertices will be closer. 
   
4. Coordinates - the value of the edge will be according to the coordinate of the vertices it connected.    

## Co file

The second file is co, represent the vertices. each row is a vertex - index of the vertex and it's coordinates (2 or 3). 



