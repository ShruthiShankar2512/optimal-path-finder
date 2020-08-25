## Path Finding Algorithms - USC CSCI561 (Foundations of AI)
The rules of the problem are mentioned in detail in `hw1.pdf`.   

The program 'shortest_path.py' takes the terrain map as input, and returns the most optimal path between any two files using 3 algorithms - Breadth First Search, Uniform Cost Search and A* Algorithm.

### Restrictions/Modifications to the algorithms:
The terrain map can be imagined as a surface in a 3- dimensional space. It is represented using a mesh-grid with a Z value assigned to each cell that identifies the elevation of the planet at the location of the cell. At each cell, the rover can move to each of 8 possible neighbor cells: North, North-East, East, South-East, South, South-West, West, and North-West. Actions are assumed to be deterministic and error-free (the rover will always end up at the intended neighbor cell).
The rover is not designed to climb across steep hills and thus moving to a neighboring cell which requires the rover to climb up or down a surface which is steeper than a particular threshold value is not allowed. This maximum slope (expressed as a difference in Z elevation between adjacent cells) will be given as an input along with the topographical map.   
 Our objective is first to avoid steep areas and thus we want to minimize the path from A to B under those constraints. Thus, our goal is, roughly, finding the shortest path among the safe paths. What defines the safety of a path is the maximum slope between any two adjacent cells along that path.


#### Costs associated with each algorithm's movement:
* Breadth-first search (BFS)
In BFS, each move from one cell to any of its 8 neighbors counts for a unit path cost of 1.

* Uniform-cost search (UCS)
When running UCS, you should compute unit path costs in 2D. Assume that cells’ center coordinates projected to the 2D ground plane are spaced by a 2D distance of 10 North-South and East-West. That is, a North or South or East or West move from a cell to one of its 4-connected neighbors incurs a unit path cost of 10, while a diagonal move to a neighbor incurs a unit path cost of 14 as an approximation to 10√𝟐 when running UCS.

* A* search (A*).
When running A*, you should compute an approximate integer unit path cost of each move in 3D, by summing the horizontal move distance as in the UCS case (unit cost of 10 when moving North to South or East to West, and unit cost of 14 when moving diagonally), plus the absolute difference in elevation between the two cells. For example, moving diagonally from one cell with Z=20 to adjacent North-East cell with elevation Z=18 would cost 14+|20-18|=16. Moving from a cell with Z=-23 to adjacent cell to the West with Z=-30 would cost 10+|-23+30|=17.   
**Admissible Heuristic used for this algorithm:** Straight line distance between a node and the target.
