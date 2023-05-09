from astar import * 
from utils import *
from graphHandler import * 
import folium
from kdtree import *
import time

start = (30.3243732 , 31.6886483) 
goal  = (30.3569825 , 31.7031567)


goal_1  = (30.3255239 , 31.6904758)

start2 = (30.3113419 , 31.6907916)
goal2 = (30.3043925 , 31.7485731)



points = get_points_from_graph()

kdtree = KDTree(points, haversine , 2)
nearest_start = kdtree.get_nearest_node(start)[0][1].value
nearest_goal  = kdtree.get_nearest_node(goal)[0][1].value


path ,  cost = astar_algorithm(nearest_start, nearest_goal)


print("cost", cost)


export_html(nearest_start , nearest_goal , path , "../map_previews/test6")
