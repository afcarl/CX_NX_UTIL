import networkx as nx

# Special Keys
ID = '@id'

NODES = 'nodes'
EDGES = 'edges'

SOURCE = 'source'
TARGET = 'target'

DATA = 'data'

CITATIONS = 'citations'

# From NetworkX:


def __create_node(node_id):
    return {ID: str(node_id)}


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
    citations=[]
    for node_id in nodes:
        my_nodes.append(__create_node(node_id))
        node_with_data = g.node[node_id]
        print("node wd: " + str(node_with_data))
        if 'data' in node_with_data:
            data = node_with_data['data']
            if CITATIONS in data:
                citations.extend(data[CITATIONS])
                print("    cit: " + str(citations))

    my_edges = []
    for edge in edges:
        my_edges.append(edge_builder(edge))
        if CITATIONS in edge:
            print("e:" + str(edge))

    cx = []
    cx.append({NODES: my_nodes})
    cx.append({EDGES: my_edges})
    if len(citations) > 0:
        cx.append({CITATIONS: citations})

    return cx


# To NetworkX:

def __add_node(g, node):
    g.add_node(node[ID])


def __add_edge(g, edge):
    source = edge[SOURCE]
    target = edge[TARGET]
    #g.add_edge(source, target)
    if '@id' in edge:
        g.add_edge(source, target, id=edge['@id'])
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
            if key == CITATIONS:
                for citation in value:
                    nodes = citation.get('nodes')
                    edges = citation.get('edges')
                    print("citation edges:" + str(edges))
                    if nodes is not None:
                        for node in nodes:
                            my_node = g.node[node]
                            if 'data' not in my_node:
                                my_node['data'] = {}
                            if CITATIONS not in my_node['data']:
                                my_node['data'][CITATIONS] = []
                            my_node['data'][CITATIONS].append(citation)
                    if edges is not None:
                        for edge in edges:
                            my_edge = edge_ids[edge]
                            #print(my_edge)
                            #if 'data' not in my_edge:
                            #    my_edge['data'] = {}
                            #if 'citation' not in my_edge['data']:
                            #    my_edge['data']['citation'] = []
                            #my_edge['data']['citation'].append(citation)
                            #s = my_edge[0]
                            #t = my_edge[1]
                            #g[s][t]['data']['citation'] = citation

    return g


# For comparisons:

def edge_id_match(e0, e1):
    id0 = None
    id1 = None
    if 0 in e0:
        e0 = e0[0]
    if 0 in e1:
        e1 = e1[0]
    if 'id' in e0:
        id0 = e0['id']
    if 'id' in e1:
        id1 = e1['id']

    return id0 == id1