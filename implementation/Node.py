from implementation import StraightLineFormula


class Edge:
    def __init__(self, srcNode: int, weight: float, destNode: int, formula: StraightLineFormula):
        self._srcNode = srcNode
        self._w = weight
        self._destNode = destNode
        self.formula = formula
    # getters
    def getSrcNode(self):
        return self._srcNode

    def getDestNode(self):
        return self._destNode

    def getWeight(self):
        return self._w

    # setters
    def setSrcNode(self, node):
        self._srcNode = node

    def setDestNode(self, node):
        self._destNode = node

    def setWeight(self, w):
        self._w = w


class Node:
    def __init__(self, key: int):
        self._key = key
        self._location = ()
        self._edgesToNode = {}
        self._edgesFromNode = {}
        self._tag = 0

    def __repr__(self):
        s = "{}: |edges out| {} |edges in| {}".format(self._key, len(self._edgesFromNode), len(self._edgesToNode))
        return s

    # this function adds an edge to the relevant list of the node (depend on the type of the edge - in or out)
    def addEdge(self, edge: Edge):
        if edge.getSrcNode() == self._key:
            self._edgesFromNode[edge.getDestNode()] = edge.getWeight()
        elif edge.getDestNode() == self._key:
            self._edgesToNode[edge.getSrcNode()] = edge.getWeight()

    # this function removes an edge of the relevant list of the node (depend on the type of the edge - in or out)
    def removeEdge(self, edge: Edge):
        if edge.getSrcNode() == self._key:
            del self._edgesFromNode[edge.getDestNode()]
        elif edge.getDestNode() == self._key:
            del self._edgesToNode[edge.getSrcNode()]

    # getters
    def getKey(self):
        return self._key

    def getLocation(self):
        return self._location

    def getTag(self):
        return self._tag

    def getEdgesToNode(self):
        return self._edgesToNode

    def getEdgesFromNode(self):
        return self._edgesFromNode

    # setters
    def setKey(self, k):
        self._key = k

    def setLocation(self, loc):
        self._location = loc

    def setTag(self, t):
        self._tag = t
