"""
 This class will represent the straight line of each edge in our graph,
 we will use it to determine on which edge each Pokemon sits
"""


class StraightLineFormula:
    def __init__(self):
        self.slope = 0
        self.b_of_formula = 0

    def StraightLineFormula(self, first, second):
        firstX = first[0]
        firstY = first[1]
        secondX = second[0]
        secondY = second[1]

        self.slope = (secondY - firstY) / (secondX - firstX)
        self.b_of_formula = firstY - (firstX * self.slope)

    def onEdge(self, pos):
        y = pos[1]
        y = float("{:.10f}".format(y))
        check = pos[0] * self.slope + self.b_of_formula
        check = float("{:.10f}".format(check))
        if y == check:
            return True
        return False

    def __repr__(self):
        return "y = " + str(self.slope) + " * x" + str(self.b_of_formula)
