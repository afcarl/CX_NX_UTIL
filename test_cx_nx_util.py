import unittest
import cx_nx_util as cxu
import networkx as nx
import json


class TestCxNxUtil(unittest.TestCase):

    def test_basic_roundtrip(self):
        g1 = nx.scale_free_graph(10)
        cx1 = cxu.from_networkx(g1)
        g2 = cxu.to_networkx(cx1)
        self.assertTrue(nx.is_isomorphic(g1, g2, edge_match=cxu.edge_id_match))

    def test_edge_match(self):
        json_str_1a = '''
        [
          {
            "nodes": [
              {
                "@id": "_0"
              },
              {
                "@id": "_1"
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
              }
            ]
          }
        ]
        '''

        json_str_1b = '''
        [
          {
            "edges": [
              {
                "source": "_1",
                "target": "_2",
                "@id": "e2"
              },
              {
                "source": "_0",
                "target": "_1",
                "@id": "e1"
              }
            ]
          },
          {
            "nodes": [
              {
                "@id": "_1"
              },
              {
                "@id": "_0"
              }
            ]
          }
        ]
        '''

        g1a = cxu.to_networkx(json.loads(json_str_1a))
        g1b = cxu.to_networkx(json.loads(json_str_1b))

        # Has different edge id.
        json_str_2 = '''
        [
          {
            "nodes": [
              {
                "@id": "_0"
              },
              {
                "@id": "_1"
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
                "@id": "qwerty"
              }
            ]
          }
        ]
        '''

        g2 = cxu.to_networkx(json.loads(json_str_2))

        # Has no edge ids.
        json_str_3 = '''
        [
          {
            "nodes": [
              {
                "@id": "_0"
              },
              {
                "@id": "_1"
              }
            ]
          },
          {
            "edges": [
              {
                "source": "_0",
                "target": "_1"
              },
              {
                "source": "_1",
                "target": "_2"
              }
            ]
          }
        ]
        '''

        g3a = cxu.to_networkx(json.loads(json_str_3))
        g3b = cxu.to_networkx(json.loads(json_str_3))

        # Same edge ids.
        self.assertTrue(nx.is_isomorphic(g1a, g1b, edge_match=cxu.edge_id_match))
        # Different edge ids.
        self.assertFalse(nx.is_isomorphic(g1a, g2, edge_match=cxu.edge_id_match))
        # Some missing edge ids.
        self.assertFalse(nx.is_isomorphic(g1a, g3a, edge_match=cxu.edge_id_match))
        # No edge ids.
        self.assertTrue(nx.is_isomorphic(g3a, g3b, edge_match=cxu.edge_id_match))

    def test_ordered_and_unordered(self):
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

        g1 = cxu.to_networkx(json.loads(json_str_1))

        json_str_2 = '''
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
            "ignore_me": [
              {
                "x": "33993"
              },
              {
                "y": "2393"
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
            "ignore_me_too": [
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

        g2 = cxu.to_networkx(json.loads(json_str_2))
        self.assertTrue(nx.is_isomorphic(g1, g2, edge_match=cxu.edge_id_match))



if __name__ == '__main__':
    unittest.main()
