import Node
from StraightLineFormula import StraightLineFormula


class Edge:
    def __init__(self, srcNode: int, weight: float, destNode: int, formula: StraightLineFormula):
        self._srcNode = srcNode
        self._w = weight
        self._destNode = destNode
        self.formula = formula.StraightLineFormula()

    # getters
    def getSrcNode(self):
        return self._srcNode

    def getDestNode(self):
        return self._destNode

    def getWeight(self):
        return self._w

    # setters
    def setSrcNode(self, node: Node):
        self._srcNode = node

    def setDestNode(self, node: Node):
        self._destNode = node

    def setWeight(self, w):
        self._w = w
