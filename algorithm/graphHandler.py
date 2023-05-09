import osmnx as ox 
from xml.dom import minidom



def generate_graphml_from_xml(xml_filepath , graphml_filepath):
    """
    convert OSM/xml file to graphml file which is more convenient
    in terms of speed but not security wise. 
    """
    try: 
        xml_graph  = ox.graph_from_xml(xml_filepath)
        ox.save_graphml(xml_graph , graphml_filepath)

    except FileNotFoundError:
        print("xml file does not exist")


def parse_xmldoc_from_graphml(graphml_filepath):
    """
    convert the graphml file to xmldoc
    very slow in practice 
    """
    try :
        return minidom.parse(graphml_filepath)
        
    except FileNotFoundError:
        print("graphml file path does not exist")
