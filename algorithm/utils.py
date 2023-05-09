import numpy as np 
import networkx as nx 
from graphHandler import *
from performance import *
import folium

graphml_file = '../map_data/file.graphml'
graph        = nx.read_graphml(graphml_file)
graph_nodes  =  graph.nodes

EARTH_RADIUS_IN_KM = 6371 # estimate of earth radius subject to change

def get_points_from_graph():
    """
    return list of points in the form of [[lat,lon], OSMid]
    """
    points = []
    for i , node_id in enumerate(graph_nodes):
        points.append([[float(graph.nodes[node_id]['y']) , float(graph.nodes[node_id]['x'])], node_id])
    return points

# sin function in degrees
def sin(angle_in_deg):
    return np.sin(np.deg2rad(angle_in_deg))

# cos function in degrees
def cos(angle_in_deg):
    return np.cos(np.deg2rad(angle_in_deg))

# a function to calculate distance between two points 
# on a sphere given their lat and lon 
def haversine(pt1 , pt2):
    alpha_1  , gamma_1 = pt1
    alpha_2  , gamma_2 = pt2
    term1 = sin((alpha_2 - alpha_1)/2)**2
    term2 = sin((gamma_2 - gamma_1)/2)**2
    term3 = cos(alpha_2) * cos(alpha_1)
    term4 = np.sqrt(term1 + term2 * term3)
    distance = 2 * EARTH_RADIUS_IN_KM * np.arcsin(term4)
    return distance

# wrapper function to haversine function which
# used as a heurstic for A* algorithm
def compute_heuristic(pt1 , pt2):
    return haversine(pt1 , pt2)


# linear search method
# better if you want to query one or two points
@timeit
def get_nearest_node(pt):
    node_id = None
    min_distance = float("inf")
    node_pt = (None ,  None)
    for i , node in enumerate(graph_nodes):
        tmp = (float(graph.nodes[node]['y']) , float(graph.nodes[node]['x']))
        distance = haversine(pt , tmp)
        if min_distance > distance : 
            node_pt = tmp
            min_distance = distance
            node_id = node
    return node_pt , node_id

@timeit
def get_nodeID_from_lat_lon(pt):

    for node in graph_nodes:

        if float(graph_nodes[node]['y']) == pt[0] and \
           float(graph_nodes[node]['x']) == pt[1] : 

           return node

def get_lat_lon_from_nodeID(node_id):

    lat = float(graph_nodes[node_id]['y'])
    lon = float(graph_nodes[node_id]['x'])

    return (lat , lon)


def get_neighbours( node_id ):

    neighbours = {}
    neighbour_lst = []
    for neighbour_id , attributes in graph.adj[node_id].items()  : 

        neighbour_info           = { }
        neighbour_lat_lon        = get_lat_lon_from_nodeID(neighbour_id)
        neighbour_cost           = float(attributes[0]['length'])

        neighbour_info[neighbour_id] = { "lat"  : neighbour_lat_lon[0] , 
                                         "lon"  : neighbour_lat_lon[1] ,
                                         "cost" : neighbour_cost       }
        neighbour_lst.append(neighbour_info)
        
    neighbours[node_id] = neighbour_lst

    return neighbours

def get_neighbour_info( neighbour_dict ,  goal):

    node_id =  0 
    neighbour_pt = None
    neighbour_cost  = 0

    for key , value in neighbour_dict.items() :

        node_id = key 
        neighbour_pt = (float(value['lat']) , float(value['lon']))
        neighbour_cost = float(value['cost'])
        neighbour_heuristic = compute_heuristic(neighbour_pt , goal)

    return node_id , neighbour_pt , neighbour_cost , neighbour_heuristic

def export_html(start , goal, path ,  filename):
    map_ = folium.Map(start, zoom_start=13)
    map_.add_child(folium.Marker(start , icon=folium.Icon(color='red')))
    map_.add_child(folium.Marker(goal , icon=folium.Icon(color='green')))
    points = []
    for pt in path[1:]:
        points.append([pt['lat'], pt['lon']])
    folium.PolyLine(points, color='red').add_to(map_)

    map_.save(filename)
