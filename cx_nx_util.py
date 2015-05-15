import networkx as nx

# Special Keys
ID = '@id'

NODES = 'nodes'
EDGES = 'edges'

SOURCE = 'source'
TARGET = 'target'

DATA = 'data'

# From NetworkX:

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
    edge_builder = None
    if isinstance(g, nx.MultiDiGraph) or isinstance(g, nx.MultiGraph):
        edges = g.edges(data=True, keys=True)
        # edge_builder = __build_multi_edge
        edge_builder = __build_edge
    else:
        edges = g.edges(data=True)
        edge_builder = __build_edge

    nodes = g.nodes()
    my_nodes = []
    for node_id in nodes:
        my_nodes.append(__create_node(node_id))

    my_edges = []
    for edge in edges:
        my_edges.append(edge_builder(edge))
        if 'citation' in edge:
            print( type(edge) )
            print("|" + str(edge))

    cx = []
    cx.append({NODES: my_nodes})
    cx.append({EDGES: my_edges})

    return cx


# To NetworkX:

def __add_node(g, node):
    g.add_node(node[ID])


def __add_edge(g, edge):
    source = edge[SOURCE]
    target = edge[TARGET]
    if '@id' in edge:
        g.add_edge(source, target)
        g[source][target]['data'] = dict(id=edge['@id'])
    else:
        g.add_edge(source, target)


def to_networkx(cx, directed=True):

    if directed:
        g = nx.MultiDiGraph()
    else:
        g = nx.MultiGraph()

    edge_ids = {}

    for x in cx:
        for key, value in x.items():
            if key == NODES:
                for node in value:
                    __add_node(g, node)
            elif key == EDGES:
                for edge in value:
                    __add_edge(g, edge)
                    if '@id' in edge:
                        edge_ids[edge['@id']] = (edge[SOURCE], edge[TARGET]) # TODO this should go into __add_edge.

    for x in cx:
        for key, value in x.items():
            if key == 'citations':
                for citation in value:
                    nodes = citation.get('nodes')
                    edges = citation.get('edges')
                    if nodes is not None:
                        for node in nodes:
                            g.node[node]['citation'] = citation
                    if edges is not None:
                        for edge in edges:
                            my_edge = edge_ids[edge]
                            s = my_edge[0]
                            t = my_edge[1]
                            g[s][t]['citation'] = citation

    return g


# For comparisons:

def edge_id_match(e0, e1):
    id0 = None
    id1 = None
    if 'data' in e0 and 'id' in e0['data']:
        id0 = e0['data']['id']
    if 'data' in e1 and 'id' in e1['data']:
        id1 = e1['data']['id']
    return id0 == id1