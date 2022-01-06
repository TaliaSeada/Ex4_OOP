import unittest

from Client.StraightLineFormula import StraightLineFormula
from implementation.DiGraph import DiGraph
from implementation.Node import Edge
from implementation.Node import Node


class MyTestCase(unittest.TestCase):
    def test_Graph(self):
        graph = DiGraph()

        node = Node(0)
        node1 = Node(1)
        node2 = Node(2)

        # addNode
        self.assertTrue(graph.add_node(0))
        self.assertTrue(graph.add_node(1))
        self.assertTrue(graph.add_node(2))
        self.assertTrue(graph.add_node(3))
        self.assertFalse(graph.add_node(3))

        # removeNode
        self.assertTrue(graph.remove_node(3))
        self.assertFalse(graph.remove_node(3))

        formula = StraightLineFormula()
        edge = Edge(node.getKey(), 1.0, node1.getKey(), formula)
        edge1 = Edge(node1.getKey(), 2.0, node2.getKey(), formula)
        edge2 = Edge(node2.getKey(), 3.0, node.getKey(), formula)

        edge3 = Edge(node1.getKey(), 1.0, node.getKey(), formula)
        edge4 = Edge(node2.getKey(), 2.0, node1.getKey(), formula)

        # addEdge
        self.assertTrue(graph.add_edge(node.getKey(), node1.getKey(), 1.0))
        self.assertTrue(graph.add_edge(node1.getKey(), node2.getKey(), 2.0))
        self.assertTrue(graph.add_edge(node2.getKey(), node.getKey(), 3.0))
        self.assertTrue(graph.add_edge(node1.getKey(), node.getKey(), 1.0))
        self.assertTrue(graph.add_edge(node2.getKey(), node1.getKey(), 2.0))

        self.assertTrue(graph.add_edge(0, 2, 3.0))
        self.assertFalse(graph.add_edge(0, 2, 3.0))

        # removeEdge
        self.assertTrue(graph.remove_edge(0, 2))
        self.assertFalse(graph.remove_edge(0, 2))

        nodes = {0: node, 1: node1, 2: node2}

        # mc
        self.assertEqual(graph.get_mc(), 12)

        # all edges
        allIn = {node1.getKey(): edge3.getWeight(), node2.getKey(): edge2.getWeight()}
        self.assertEqual(allIn, graph.all_in_edges_of_node(node.getKey()))

        allOut = {node1.getKey(): edge.getWeight()}
        self.assertEqual(allOut, graph.all_out_edges_of_node(node.getKey()))

        # getters
        self.assertNotEqual(graph, None)
        v_size = graph.v_size()
        self.assertEqual(v_size, 3)
        e_size = graph.e_size()
        self.assertEqual(e_size, 5)
        v = graph.get_all_v()
        # self.assertEqual(v, nodes)
        for i in v:
            self.assertTrue(nodes.__contains__(i))


if __name__ == '__main__':
    unittest.main()
