import random
import unittest

from implementation.DiGraph import DiGraph
from implementation.GraphAlgo import GraphAlgo


def createCities(size: int, g: GraphAlgo):
    cities = []
    maxKey = max(g.get_graph().get_all_v().keys())
    minKey = min(g.get_graph().get_all_v().keys())
    while len(cities) < size:
        city = random.randint(minKey, maxKey)
        if city not in cities:
            cities.append(city)
    return cities


class MyTestCase(unittest.TestCase):
    def test_getGraph(self):
        Agraph = GraphAlgo()
        fileName = "../../data/A0"
        Agraph.load_from_json(fileName)
        self.assertTrue(isinstance(Agraph.get_graph(), DiGraph))

    def test_TSP(self):
        Agraph = GraphAlgo()
        fileName = "../../data/A0"
        Agraph.load_from_json(fileName)

        cities = [0, 3, 6, 9]
        nodes, dist = Agraph.TSP(cities)
        self.assertTrue(0 in nodes)
        self.assertTrue(3 in nodes)
        self.assertTrue(6 in nodes)
        self.assertTrue(9 in nodes)

        dist = '%0.3f' % dist

        self.assertEqual(float(dist), 11.291)
        self.assertEqual(nodes, [0, 10, 9, 8, 7, 6, 5, 4, 3])

    def test_load(self):
        Agraph = GraphAlgo()
        fileName = "../../data/A0"
        self.assertRaises(Exception, Agraph.load_from_json(fileName))
        fileName = "../../data/A1"
        self.assertTrue(Agraph.load_from_json(fileName))
        self.assertEqual(Agraph.get_graph().v_size(), 17)

    def test_save(self):
        Agraph = GraphAlgo()
        fileName = "../../data/A1"
        self.assertTrue(Agraph.load_from_json(fileName))
        self.assertTrue(Agraph.save_to_json('test.json'))
        self.assertTrue(Agraph.load_from_json('test.json'))

    def test_center(self):
        graph3 = GraphAlgo()
        fileName3 = "../../data/A0"
        graph3.load_from_json(fileName3)
        self.assertEqual(graph3.centerPoint()[0], 7)

    def test_shortest_path(self):
        Agraph = GraphAlgo()
        fileName = "../../data/A1"
        Agraph.load_from_json(fileName)
        list = [0, 1, 2, 6]
        self.assertEqual(list, Agraph.shortest_path(0, 6)[1])
