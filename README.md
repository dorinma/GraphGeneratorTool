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
   
4. Flow Network -    

## Co file

The second file is co, represent the vertices. each row is a vertex - index of the vertex and it's coordinates (2 or 3). 



