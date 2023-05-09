import math

class Node :
    """
    a simple data type class for A* algorithm to 
    mainpulate and keep track of the data each node used 
    in the computation 
    """
    def __init__(self , pt  , node_id):

        self.pt  = pt                   # (latitude,longitude)  
        self.id  = node_id              # the OSM node id from the db
        self.parent  = None             # parent of the node while traversing
        self.h   = float('inf')         # the heurisitic value of the node (estimate of
                                        # the remaining distance to the goal)
        self.g   = 0                    # the node cost (the actual distance travelled from start)
        self.f   = self.g + self.h      # total node cost which used in the computation
        self.neighbour_cost = 0         # not very essential variable to store the cost as a neighbour

    def __eq__(self , other):

        return self.id == other.id 

    def __hash__(self):
        return hash((self.f, self.id))


class PriorityQueue:
    """
    a customised data structure for A* algorithm
    it is also compatible with the Node datatype.
    This PriorityQueue class is implemented with
    min-heap
    """
    def __init__(self):

        # one element is used for the convention of left and right 
        # childs while poping 
        self.queue  = [None]      # array to keep track of elements 
        self.insert_counter = 0   # for equal-priority conflict

    def __contains__(self, node):
        # custom contains function which additionally check for the cost (g)
        for qnode,_ in self.queue[1:] : 

            if qnode.id == node.id and  node.g > qnode.g : 
                return True
            
        return False

    def _is_lower_than(self , node_1 , node_2):
        # priority check function based on the total cost of the node (f)
        # if both node has equal f then we look at the insert counter the earlier the higher priority
        return node_1[0].f < node_2[0].f or (node_2[0].f == node_1[0].f and node_1[1] <  node_2[1])

    def _heapify(self , new_node_index ):
        # convert the array to heap 
        while new_node_index > 1 : 
            new_node  =  self.queue[new_node_index]
            parent_index  = math.floor(new_node_index / 2)
            parent_node  = self.queue[parent_index]

            if self._is_lower_than(parent_node , new_node):
                break 

            temp_node = parent_node
            self.queue[parent_index] = new_node
            self.queue[new_node_index] = temp_node 

            new_node_index = parent_index


    def insertNode(self ,node):
        
        new_node_index = len(self.queue)
        self.insert_counter += 1 
        self.queue.append((node , self.insert_counter))
        self._heapify(new_node_index)

    def popNode(self):
        if len(self.queue) == 1 : 
            raise LookupError("queue is empty")

        result  =  self.queue[1][0]
        empty_space_idx = 1 

        while empty_space_idx * 2 < len(self.queue) : 

            right_child_idx  = empty_space_idx * 2 + 1
            left_child_idx   = empty_space_idx * 2 

            if (
                len(self.queue) <= right_child_idx
                or self._is_lower_than(self.queue[left_child_idx] , self.queue[right_child_idx])
                ):
                self.queue[empty_space_idx] = self.queue[left_child_idx]
                empty_space_idx = left_child_idx
            else:
                self.queue[empty_space_idx] = self.queue[right_child_idx]
                empty_space_idx = right_child_idx

        last_node_idx = len(self.queue) - 1
        self.queue[empty_space_idx] = self.queue[last_node_idx]
        self._heapify(empty_space_idx)

        self.queue.pop()
        return result

    def isEmpty(self):
        return len(self.queue) == 1 

    def peek(self):
        
        if len(self.queue) > 1 : 
            return self.queue[1][0]
        else:
            return None 

