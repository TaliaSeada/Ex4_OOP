class StraightLineFormula:
    def __init__(self, slope, b_of_formula):
        self.slope = slope
        self.b_of_formula = b_of_formula

    def formula(self, first, second):
        firstX = first[0]
        firstY = first[1]
        secondX = second[0]
        secondY = second[1]

        self.slope = (secondY - firstY) / (secondX - firstX)
        self.b_of_formula = firstY - (firstX * self.slope)

    def onEdge(self, pos):
        y = pos[1]
        check = pos[0] * self.slope + self.b_of_formula
        if y == check:
            return True
        return False

    def __repr__(self):
        return "y = " + self.slope + " * x" + self.b_of_formula
