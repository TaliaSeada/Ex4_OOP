from implementation.GraphAlgo import GraphAlgo
from Client import Algorithm

"""
The Model file.
This class will hold the graph of each level and the list of Pokemons
"""


class Game:
    def __init__(self, graph: GraphAlgo):
        self.graph = GraphAlgo(graph.get_graph())
        self.pokemons = []
        self.count = 0

    def setPokemonsEdges(self):
        for p in self.pokemons:
            if p.on is not None:
                continue
            for edge in self.graph.get_graph().get_edges():
                if edge.getDestNode() > edge.getSrcNode() and p.type > 0:
                    if edge.formula.onEdge(p.pos):
                        p.on = edge
                        self.count += 1
                        break
                elif edge.getDestNode() < edge.getSrcNode() and p.type < 0:
                    if edge.formula.onEdge(p.pos):
                        p.on = edge
                        self.count += 1
                        break

    def oneAgent(self, pokemonsResult):
        pathToAdd = Algorithm.oneAgent(self, pokemonsResult)
        return pathToAdd

    def allocate(self, pokemons, agentsPath, agents):
        agentsPath = Algorithm.allocate(self, pokemons, agentsPath, agents)
        return agentsPath
