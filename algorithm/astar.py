from priorityQueue import PriorityQueue , Node 
from utils import * 
from performance import timeit

@timeit
def generate_final_path(path, start, goal):
    """
    a function to filter out the nodes creating a series of connected nodes 
    with lowest cost 
    """
    final_path = []
    child = goal
    parent = ()
    cost = 0
    while(parent!=start):
        temp_dict = {}
        cost = cost + float(path[str(child)].neighbour_cost)
        parent = path[str(child)].parent
        parent = tuple(float(x) for x in parent.strip('()').split(','))
        
        temp_dict["lat"] = parent[0]
        temp_dict["lon"] = parent[1]
        
        final_path.append(temp_dict)
        child = parent

    return final_path, cost

@timeit
def astar_algorithm( start , goal):

    path  = {}
    open_list    = PriorityQueue()
    closed_list  = []

    start_id = get_nodeID_from_lat_lon( start) 
    goal_id  = get_nodeID_from_lat_lon( goal)

    start_node    = Node(start , start_id)
    start_node.h  = compute_heuristic(start , goal)
    start_node.g  = 0

    open_list.insertNode(start_node)
    while not open_list.isEmpty() :

        current_node = open_list.popNode()
        
        if current_node.id == goal_id : 

            print("goal reached")
            break  

        neighbours = get_neighbours( current_node.id  )
        for neighbour_dict in neighbours[current_node.id] : 

            neighbour_id , neighbour_pt , neighbour_cost , neighbour_heuristic = get_neighbour_info(neighbour_dict, goal)

            if neighbour_id in closed_list  : 
                continue
            else: 
                neighbour_node = Node(neighbour_pt , neighbour_id)
                neighbour_node.g = neighbour_cost + current_node.g
                neighbour_node.h = neighbour_heuristic
                neighbour_node.f = neighbour_node.g  + neighbour_node.h

                if neighbour_node in open_list  : 
                    continue

                open_list.insertNode(neighbour_node)

            neighbour_node.parent = str(current_node.pt)
            neighbour_node.neighbour_cost = neighbour_cost
            path[str(neighbour_node.pt)] = neighbour_node 

        closed_list.append(current_node.id)

    # print(path)
    
    return generate_final_path(path , start , goal)

