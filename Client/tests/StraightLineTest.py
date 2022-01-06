import unittest
from Client.StraightLineFormula import StraightLineFormula

class MyTestCase(unittest.TestCase):
    def test_constructor(self):
        line = StraightLineFormula()
        self.assertEqual(line.slope, 0)
        self.assertEqual(line.b_of_formula, 0)

    def test_StraightLineFormula(self):
        line = StraightLineFormula()
        p1 = (1, 1)
        p2 = (2, 2)
        line.StraightLineFormula(p1, p2)
        self.assertEqual(line.slope, 1)
        self.assertEqual(line.b_of_formula, 0)

    def test_onEdge(self):
        line = StraightLineFormula()
        p1 = (1, 1)
        p2 = (2, 2)
        line.StraightLineFormula(p1, p2)
        p3 = (2, 7)
        p4 = (3, 3)
        self.assertEqual(line.onEdge(p3), False)
        self.assertEqual(line.onEdge(p4), True)

if __name__ == '__main__':
    unittest.main()
