import sys
from heapq import heappush, heappop, heapify
from math import sqrt
#Using heap module to implement priority queue using heaps for UCS and A*

#directing all print statements to the file output.txt
sys.stdout = open("output.txt", "w")


#Reading contents from the file. Returns a list of all the lines as strings
def readFile(fileName) -> list:
    file = open(fileName,"r")
    lines = file.readlines()
    lines = [i.strip('\n') for i in lines]
    file.close()
    return lines


#Understanding file contents

#Input: array of file elements
# Function takes all the file elements listed as strings, 
#     processes and stores the required information into a dictionary as directed in the problem statement
#Output: Dictionary containing all the reuired information
def getInfo(lines) -> dict:
    details = {}
    details["searchAlgo"] = lines[0]
    details["matrixSize"] = list(map(int,lines[1].split()))
    details["landingSite"] = list(map(int,lines[2].split()))
    details["zLimit"] = int(lines[3])
    details["noOfTargets"] = int(lines[4])
    details["targetList"] = []
    for i in range (details["noOfTargets"]):
        details["targetList"].append(list(map(int, lines[i+5].split())))
    details["matrix"] =  []
    for i in range(details["matrixSize"][1]):
        details["matrix"].append(list(map(int, lines[i+5+details["noOfTargets"]].split())))
    return details


#read the input file and get information before declaring the classes. 
# This is mainly done so that the constraints can be used/applied while creating the objects itself.
lines = readFile("input.txt")
details = getInfo(lines)

#The node class has the name of the node - which is the position in the matrix, and its z value, a list of its neighbors, 
#  the cost, and the previous node that is part of the optimal path. This is used to keep track of the path so that the algorithm can 
#  backtrack and print the optimal path that is found. 
# 
class Node:
    def __init__(self, i, j, z):
        self.visited = False
        self.name = (i,j)
        self.z = z
        self.neighbors = list()
        self.cost = 9999
        self.prev = None
    
class Graph:
    vertices = {}
    def __init__(self, g):
        self.rows = len(g)
        self.cols = len(g[0])
        for i in range(self.rows):
            for j in range(self.cols):
                self.vertices[(j,i)] = Node(j,i,g[i][j])
        self.filterNeighbors()
    """def printGraph(self):
        print(self.vertices)
        for key in sorted(list(self.vertices.keys())):
            print("name - x,y coords: ",key, "z value: ", self.vertices[key].z, "neighbor_list: ", self.vertices[key].neighbors, " cost: ", self.vertices[key].cost)"""
    # gets all the 8 neighbors according to the index values
    def getNeighbors(self,node):
        i = node.name[0]
        j = node.name[1]
        node.neighbors = [(i-1,j),(i,j-1),(i-1,j-1),(i+1,j),(i,j+1),(i+1,j+1),(i+1,j-1),(i-1,j+1)]
        node.neighbors = [i for i in node.neighbors if i[0]>=0 and i[0]<self.cols and i[1]>=0 and i[1]<self.rows]
    # filters the neighbor list using the z-value constraint.
    def filterNeighbors(self):
        for node in self.vertices.values():
            self.getNeighbors(node)
            node.neighbors = [i for i in node.neighbors if abs(node.z - self.vertices[i].z) <= details['zLimit']]


#BREADTH FIRST SEARCH 
def bfs(graph, s, t):
    source_node = graph.vertices[s]
    source_node.cost = 0
    if source_node.name == t:
        return True
    source_node.visited = True
    queue = list()
    queue.append(s)
    
    while len(queue) != 0:
        u = queue.pop(0)
        node_u = graph.vertices[u]
        #Go through list of neighbors
        for i in node_u.neighbors:
            #if not visited, mark as visited, add one for distance, store the previous node, and append into queue
            if graph.vertices[i].visited == False:
                graph.vertices[i].visited = True
                graph.vertices[i].cost = node_u.cost + 1
                graph.vertices[i].prev = u
                queue.append(i)
                #Check for goal state
                if i == t:
                    return True
    return False

def print_optimal_bfs_path(graph, s, t):
    #print("BFS")
    if (bfs(graph, s, t) == False):
        print("FAIL")
        return
    path = list()
    v = t
    path.append(v)
    while(graph.vertices[v].prev != None):
        path.append(graph.vertices[v].prev)
        v = graph.vertices[v].prev
    
    #print("Distance: ", graph.vertices[t].cost)
    path.reverse()
    #print("Path: ", path) 
    f = lambda x: ",".join(map(str,x))
    print(" ".join(f(x) for x in path))




#UNIFORM COST SEARCH 

def get_ucs_cost(s,t):    
    if s[0] != t[0] and s[1] != t[1]:
        return 14
    else:
        return 10

def ucs(graph, s, t):
    source_node = graph.vertices[s]
    source_node.cost = 0
    source_node.visited = True
    if source_node.name == t:
        return True
    queue = list()
    heapify(queue)
    
    #push into the queue node s with cost of source_node ie 0
    heappush(queue, (source_node.cost, source_node.name))  
    
    while len(queue) != 0:
        u = heappop(queue)
        u_name = u[1]
        if u_name == t:
            return True
        node_u = graph.vertices[u_name]
         #Go through list of neighbors
        for i in node_u.neighbors:
            #if not visited, mark as visited, add cost according to indices (10 or 14), mark previous node as u
            if graph.vertices[i].visited == False:
                graph.vertices[i].visited = True
                graph.vertices[i].cost = node_u.cost + get_ucs_cost(node_u.name, i)
                graph.vertices[i].prev = node_u.name
                heappush(queue, (graph.vertices[i].cost,i))
                if i == t:
                    return True
            #if it is marked as visited, check if the cost is higher than current node
            else:
                if graph.vertices[i].cost > node_u.cost + get_ucs_cost(node_u.name, i):
                    graph.vertices[i].cost = node_u.cost + get_ucs_cost(node_u.name, i)
                    graph.vertices[i].prev = node_u.name
                    if i == t:
                        return True
    return False
        
    
def print_optimal_ucs_path(graph, s, t):
    #print("UCS")
    if (ucs(graph, s, t) == False):
        print("FAIL")
        return
    path = list()
    v = t
    path.append(v)
    while(graph.vertices[v].prev != None):
        path.append(graph.vertices[v].prev)
        v = graph.vertices[v].prev
        if v == t:
            break
    #print("Distance: ", graph.vertices[t].cost)
    path.reverse()
    #print("Path: ", path) 
    f = lambda x: ",".join(map(str,x))
    print(" ".join(f(x) for x in path))    
    


#A * SEARCH 


#cost = ucs cost + elevation difference
def a_star_cost_g(graph, s, t):    
    if s[0] != t[0] and s[1] != t[1]:
        cost = 14 + abs(graph.vertices[s].z - graph.vertices[t].z)
        return cost
    else:
        cost = 10 + abs(graph.vertices[s].z - graph.vertices[t].z)
        return cost

#heauristic function : straight line distance between node n and target.     
def heuristic(node, target):
    sld = sqrt( (node[0] - target[0])**2 + (node[1] - target[1])**2 )
    return sld
    
   
#same as UCS, but the ordering of the priority queue changes.    
def a_star(graph, s, t):
    source_node = graph.vertices[s]
    #the cost is always the function g(n)
    source_node.cost = 0
    source_node.visited = True
    if source_node.name == t:
        return True
    queue = list()
    heapify(queue)
    
    #push into the queue node s with cost of source_node + the heuristic function, 
    #    so this way the queue is ordered by the func f(n) = g(n) + h(n) 
    heappush(queue, (source_node.cost + heuristic(s, t), source_node.name))  
    
    while len(queue) != 0:
        u = heappop(queue)
        u_name = u[1]
        if u_name == t:
            return True
        node_u = graph.vertices[u_name]
         #Go through list of neighbors
        for i in node_u.neighbors:
            #if not visited, mark as visited, add cost according to indices (10 or 14), mark previous node as u
            if graph.vertices[i].visited == False:
                graph.vertices[i].visited = True
                graph.vertices[i].cost = node_u.cost + a_star_cost_g(graph, node_u.name, i)
                graph.vertices[i].prev = node_u.name
                heappush(queue, (graph.vertices[i].cost + heuristic(i, t),i))
                if i == t:
                    return True
            #if it is marked as visited, check if the cost is higher than current node. If it is, change the path
            else:
                if graph.vertices[i].cost > node_u.cost + a_star_cost_g(graph, node_u.name, i):
                    graph.vertices[i].cost = node_u.cost + a_star_cost_g(graph, node_u.name, i)
                    graph.vertices[i].prev = node_u.name
                    if i == t:
                        return True
    return False
        
    
def print_optimal_a_star_path(graph, s, t):
    #print("A *")
    if (a_star(graph, s, t) == False):
        print("FAIL")
        return
    path = list()
    v = t
    path.append(v)
    while(graph.vertices[v].prev != None):
        path.append(graph.vertices[v].prev)
        v = graph.vertices[v].prev
        if v == t:
            break
    #print("Distance: ", graph.vertices[t].cost)
    path.reverse()
    #print("Path: ", path) 
    f = lambda x: ",".join(map(str,x))
    print(" ".join(f(x) for x in path)) 

    	   

#main function
def main():
	if(details['searchAlgo'] == 'BFS'):
		for i in range(details['noOfTargets']):
			graph = Graph(details['matrix'])
			print_optimal_bfs_path(graph, tuple(details['landingSite']), tuple(details['targetList'][i]))
	elif(details['searchAlgo'] == 'UCS'):
		for i in range(details['noOfTargets']):
			graph = Graph(details['matrix'])
			print_optimal_ucs_path(graph, tuple(details['landingSite']), tuple(details['targetList'][i]))
	elif(details['searchAlgo'] == 'A*'):
		for i in range(details['noOfTargets']):
			graph = Graph(details['matrix'])
			print_optimal_a_star_path(graph, tuple(details['landingSite']), tuple(details['targetList'][i]))



if __name__ == "__main__":
	main()
