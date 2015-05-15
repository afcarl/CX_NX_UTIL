import json
from py2cytoscape import util
import networkx as nx
import cx_nx_util as cxu


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
      {   "@id": "c0",
          "nodes": [],
          "edges": [ "e1" ],
          "identifier": "doi:c0",
          "description": "c0"
      },
      {   "@id": "c1",
          "nodes": [],
          "edges": [ "e3" ],
          "identifier": "doi:10.1016/0092-8674(93)80066-N",
          "description": "Bcl-2 functions in an antioxidant pathway"
      },
      {   "@id": "c2",
          "nodes": [ "_1" ],
          "identifier": "doi:10.1016/0092-8674(93)7777777",
          "description": "BAD functions in an antioxidant pathway"
      },
      {   "@id": "c3",
          "nodes": [ "_2" ],
          "identifier": "doi:39393.303c3",
          "description": "citation c3"
      }
    ]
  }
]
'''

g7 = cxu.to_networkx(json.loads(json_str_7))
g7p = cxu.to_networkx(json.loads(json_str_7))
print(nx.is_isomorphic(g7, g7p, edge_match=cxu.edge_id_match))


print("nodes:")
print(g7.node['_1'])
print(g7.node['_2'])
print("edges:")
print(type(g7['_0']['_1']))
print(g7['_0']['_1'])
print(g7['_2']['_0'])
print("----")
cx7 = cxu.from_networkx(g7)


print(json.dumps(cx7, indent=2))

g8 = cxu.to_networkx(cx7)


cx8 = cxu.from_networkx(g8)


print(json.dumps(cx8, indent=2))

G = nx.Graph()

G.add_edge("1", "2", dat={'l': "affe"})
G.add_edge("2", "3")
print(str(G.edges(data=True)))