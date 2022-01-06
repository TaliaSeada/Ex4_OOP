import unittest

from Client.StraightLineFormula import StraightLineFormula
from implementation.Node import Edge


class MyTestCase(unittest.TestCase):
    def test_Edge(self):
        formula = StraightLineFormula()
        edge = Edge(0, 1.0, 1, formula)
        src = edge.getSrcNode()
        dest = edge.getDestNode()
        w = edge.getWeight()

        self.assertNotEqual(edge, None)
        # getters
        self.assertEqual(src, 0)
        self.assertEqual(dest, 1)
        self.assertEqual(w, 1.0)
        # setters
        edge.setSrcNode(2)
        edge.setDestNode(4)
        edge.setWeight(1.22)

        src = edge.getSrcNode()
        dest = edge.getDestNode()
        w = edge.getWeight()

        self.assertEqual(src, 2)
        self.assertEqual(dest, 4)
        self.assertEqual(w, 1.22)


if __name__ == '__main__':
    unittest.main()
