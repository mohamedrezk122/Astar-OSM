from utils import *
import time
from performance import timeit
from median import median_of_medians

class TreeNode:
    """
    a node class to hold the data of the point list elements (to construct the tree )    
    """
    def __init__(self, value , node_id, axis, parent):

        self.value   = value      # (lat, lon)
        self.id      = node_id    # OSMid
        self.axis    = axis       # axis at which the node partitioned abput
        self.parent  = None       # parent node , (useful in backtracking)
        self.left    = None       # left subtree
        self.right   = None       # right subtree

class KDTree:
    """
    Kdtree data structure which partition the plane into 
    segments to search/ query for nearest neighbour in O(log(n))
    however the tree takes O(nlog(n)) to be constructed with median of medians
    (linear time selection) algorithm, or O(nlog^2n) with naive median finding with 
    sorting the point list 
    """

    def __init__(self,points,  distance_function , dim ):


        self.epsilon           = 5e-3  # 5 meter vicinity to reduce search space
        self.dim               = dim 
        self.distance_function = distance_function
        self.points            = points
        start_time             = time.time()
        self.root              = self.construct(self.points)
        print("Tree formation time" , time.time()-start_time)

    def _isLeaf(self ,  node) :
        return node.left is  None and node.right is None 

        
    def construct(self, points , axis = 0, parent=None):

        if not points:
            return

        """
        naive median finding algorithm, it sorts the 
        points based on some axis in O(nlogn) time and pick the middle
        takes 0.13 seconds for 35k nodes 
        """
        points.sort(key= lambda point : point[0][axis])
        median = len(points) // 2

        root = TreeNode(tuple(points[median][0]) , points[median][1], axis=axis, parent=parent )
        axis = (axis + 1) % self.dim
        root.left  = self.construct(points[:median], axis, parent =root)
        root.right = self.construct(points[median+1:], axis, parent=root) 

        return root

    def _nearest_neighbours(self, node , point, candidates, min_distance=float('inf'), k=1):

        if node is None : 
            return 

        distance = self.distance_function(node.value, point)

        if distance < min_distance :
            candidates.append([distance , node])
            candidates.sort(key=lambda p: p[0])
            min_distance = candidates[0][0]
            if min_distance <= self.epsilon :
                # print("pruned")
                return

        # removing candidates that are far from the query point
        if len(candidates)  > k :
            # print("removing candidates")
            candidates.pop()

        if self._isLeaf(node) :
            return 

        daxis = node.value[node.axis] - point[node.axis]
        if daxis > 0 :
            self._nearest_neighbours(node.left , point , candidates , min_distance , k)
        else:
            self._nearest_neighbours(node.right , point , candidates , min_distance , k)

        return

    @timeit
    def get_nearest_node(self, point):
        candidates = []
        self._nearest_neighbours(self.root , point , candidates, k =1 )
        return candidates

