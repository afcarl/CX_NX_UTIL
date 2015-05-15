import json
from py2cytoscape import util
import networkx as nx
import cx_nx_util as cxu


g1 = nx.scale_free_graph(4)

#cyjs = util.from_networkx(g1)
#print(json.dumps(cyjs, indent=2))

cx1 = cxu.from_networkx(g1)

# print(json.dumps(cx1, indent=2))

g2 = cxu.to_networkx(cx1)

cx2 = cxu.from_networkx(g2)

# print(json.dumps(cx2, indent=2))

g3 = cxu.to_networkx(cx2)

print(nx.is_isomorphic(g1, g2, edge_match=cxu.edge_id_match))
print(nx.is_isomorphic(g1, g3, edge_match=cxu.edge_id_match))
print(nx.is_isomorphic(g2, g3, edge_match=cxu.edge_id_match))

json_str_1 = '''
[
  {
    "nodes": [
      {
        "@id": "_0"
      },
      {
        "@id": "_1"
      },
      {
        "@id": "_2"
      },
      {
        "@id": "_3"
      }
    ]
  },
  {
    "edges": [
      {
        "source": "_0",
        "target": "_1",
        "@id": "e1"
      },
      {
        "source": "_1",
        "target": "_2",
        "@id": "e2"
      },
      {
        "source": "_2",
        "target": "_0",
        "@id": "e3"
      },
      {
        "source": "_3",
        "target": "_1",
        "@id": "e4"
      }
    ]
  }
]
'''

g4 = cxu.to_networkx(json.loads(json_str_1))

cx4 = cxu.from_networkx(g4)

print(json.dumps(cx4, indent=2))

json_str_2 = '''
[
  {
    "nodes": [
      {
        "@id": "_1"
      },
      {
        "@id": "_0"
      }
    ]
  },
  {
    "edges": [
      {

        "source": "_0",
        "@id": "e1",
        "target": "_1"
      },
      {
        "source": "_2",
        "target": "_0",
        "@id": "e3"
      }
    ]
  },
  {
    "edges": [
      {
        "source": "_1",
        "target": "_2",
        "@id": "e2"
      },
      {
        "source": "_3",
        "target": "_1",
        "@id": "e4"
      }
    ]
  },
  {
    "nodes": [
      {
        "@id": "_3"
      },
      {
        "@id": "_2"
      }
    ]
  }
]
'''

g5 = cxu.to_networkx(json.loads(json_str_2))

cx5 = cxu.from_networkx(g5)

print(nx.is_isomorphic(g4, g5, edge_match=cxu.edge_id_match))

json_str_3 = '''
[
  {
    "edges": [
      {
        "source": "_1",
        "target": "_2",
        "@id": "e2"
      }
    ]
  },
  {
    "nodes": [
      {
        "@id": "_1"
      }
    ]
  },
  {
    "nodes": [
      {
        "@id": "_0"
      }
    ]
  },
  {
    "edges": [
      {
        "source": "_2",
        "target": "_0",
        "@id": "e3"
      }
    ]
  },
  {
    "edges": [
      {
        "source": "_0",
        "target": "_1",
        "@id": "e1"
      }
    ]
  },
  {
    "edges": [
      {
        "source": "_3",
        "target": "_1",
        "@id": "e4"
      }
    ]
  },
  {
    "nodes": [
      {
        "@id": "_3"
      },
      {
        "@id": "_2"
      }
    ]
  },
  {
    "ignore_me": [
      {
        "a": "_3"
      },
      {
        "b": "_2"
      }
    ]
  }
]
'''

g6 = cxu.to_networkx(json.loads(json_str_3))

cx6 = cxu.from_networkx(g6)

print(json.dumps(cx6, indent=2))

print(nx.is_isomorphic(g4, g6, edge_match=cxu.edge_id_match))

print(g6.nodes())
print(g6.edges())


json_str_7 = '''
[
  {
    "nodes": [
      {
        "@id": "_0"
      },
      {
        "@id": "_1"
      },
      {
        "@id": "_2"
      },
      {
        "@id": "_3"
      }
    ]
  },
  {
    "edges": [
      {
        "source": "_0",
        "target": "_1",
        "@id": "e1"
      },
      {
        "source": "_1",
        "target": "_2",
        "@id": "e2"
      },
      {
        "source": "_2",
        "target": "_0",
        "@id": "e3"
      },
      {
        "source": "_3",
        "target": "_1",
        "@id": "e4"
      }
    ]
  },
  {
    "citations": [
      {   "@id": "_0",
          "nodes": [],
          "edges": [ "_0" ],
          "identifier": "doi:10.1016/0092-8674(93)80066-N",
          "description": "Bcl-2 functions in an antioxidant pathway"
      }
    ]
  }
]
'''

g7 = cxu.to_networkx(json.loads(json_str_7))

cx7 = cxu.from_networkx(g7)

print(json.dumps(cx7, indent=2))


