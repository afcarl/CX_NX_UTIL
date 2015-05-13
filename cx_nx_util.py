import networkx as nx

# Special Keys
ID = '@id'

NODES = 'nodes'
EDGES = 'edges'

SOURCE = 'source'
TARGET = 'target'

DATA = 'data'


def __map_table_data(columns, graph_obj):
    data = {}
    for col in columns:
        if col == 0:
            break

        data[col] = graph_obj[col]

    return data


def __create_node(node_id):
    return {ID: str(node_id)}


def __build_multi_edge(edge_tuple):
    source = edge_tuple[0]
    target = edge_tuple[1]
    key = edge_tuple[2]
    data = edge_tuple[3]

    data['source'] = str(source)
    data['target'] = str(target)
    data['interaction'] = str(key)
    return {DATA: data}


def __build_edge(edge_tuple):
    data = edge_tuple[3]
    if 'id' in data:
        return {SOURCE: str(edge_tuple[0]), TARGET: str(edge_tuple[1]), '@id': str(data['id'])}
    else:
        return {SOURCE: str(edge_tuple[0]), TARGET: str(edge_tuple[1])}


def from_networkx(g):
    nodes = g.nodes()
    edge_builder = None
    if isinstance(g, nx.MultiDiGraph) or isinstance(g, nx.MultiGraph):
        edges = g.edges(data=True, keys=True)
        # edge_builder = __build_multi_edge
        edge_builder = __build_edge
    else:
        edges = g.edges(data=True)
        edge_builder = __build_edge

    my_nodes = []
    for node_id in nodes:
        my_nodes.append(__create_node(node_id))

    my_edges = []
    for edge in edges:
        my_edges.append(edge_builder(edge))

    cx = []
    cx.append({NODES: my_nodes})
    cx.append({EDGES: my_edges})

    return cx


def __add_node(g, node):
    g.add_node(node[ID])


def __add_edge(g, edge):
    source = edge[SOURCE]
    target = edge[TARGET]
    if '@id' in edge:
        eid = edge['@id']
        g.add_edge(source, target, id=eid)
    else:
        g.add_edge(source, target)


def to_networkx(cx, directed=True):

    if directed:
        g = nx.MultiDiGraph()
    else:
        g = nx.MultiGraph()

    for x in cx:
        for key, value in x.items():
            if key == NODES:
                for node in value:
                    __add_node(g, node)
            elif key == EDGES:
                for edge in value:
                    __add_edge(g, edge)

    return g


def edge_id_match(e0, e1):
    if 0 in e0:
        d0 = e0[0]
        d1 = e1[0]
    else:
        d0 = e0
        d1 = e1
    if 'id' not in d0 and 'id' not in d1:
        return True
    elif 'id' not in d0 or 'id' not in d1:
        return False
    return d0['id'] == d1['id']