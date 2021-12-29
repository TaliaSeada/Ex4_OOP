from GraphAlgo import GraphAlgo


class Game:
    def __init__(self, graph: GraphAlgo):
        self.graph = GraphAlgo(graph.get_graph())
        self.pokemons = []

    def setPokemonsEdges(self):
        for p in self.pokemons:
            for edge in self.graph.get_graph().get_edges():
                if edge.getDestNode() > edge.getSrcNode() and p.type > 0:
                    if edge.formula.onEdge(p.pos):
                        p.on = edge
                        break
                elif edge.getDestNode() < edge.getSrcNode() and p.type < 0:
                    if edge.formula.onEdge(p.pos):
                        p.on = edge
                        break