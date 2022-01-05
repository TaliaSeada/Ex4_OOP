from implementation.GraphAlgo import GraphAlgo
import numpy as np

class Game:
    def __init__(self, graph: GraphAlgo):
        self.graph = GraphAlgo(graph.get_graph())
        self.pokemons = []
        self.count = 0


    def takeSecondElement(self, list):
        return list[1]


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

    def allocate(self, new_pokemons, agentsPath, agents):
        if len(new_pokemons) == 0:
            return
        if len(agents) > 1:
            for p in new_pokemons:
                bestDist = float('inf')
                bestPath = []
                id = 0
                bestid = 0
                for a in agents:
                    if a["src"] == p.on.getSrcNode() and a["dest"] == p.on.getDestNode():
                        break
                    id = a["id"]
                    if len(agentsPath[id]) == 0:
                        if a["dest"] != -1:
                            dist, path = self.graph.shortest_path(a["dest"], p.on.getSrcNode())
                        else:
                            dist, path = self.graph.shortest_path(a["src"], p.on.getSrcNode())
                        bestid = id
                        bestPath = path
                        break
                    else:
                        if agentsPath[id][-1] == p.on.getSrcNode():
                            path = []
                            dist = 0
                        else:
                            dist, path = self.graph.shortest_path(agentsPath[id][-1], p.on.getSrcNode())
                        path2, dist2 = self.graph.TSP(agentsPath[id])
                        if dist + dist2 < bestDist:
                            bestDist = dist + dist2
                            bestid = id
                            path2.extend(path)
                            isIn = False
                            for i in range(len(path2) - 1):
                                if path2[i] == p.on.getSrcNode() and path2[i + 1] == p.on.getDestNode() and len(
                                        path) == 0:
                                    isIn = True
                                    break
                            if not isIn:
                                if len(path) != 0 and abs(path[0] - path2[-1]) != 1:
                                    dist, path3 = self.graph.shortest_path(path2[-1], path[0])
                                    path2.extend(path3)
                                    path2.append(p.on.getDestNode())
                            bestPath = path2

                agentsPath[bestid] = bestPath
        else:
            pokemonsResult = []
            for p in new_pokemons:
                agentSrc = agents[0]["src"]
                agentDest = agents[0]["dest"]
                pSrc = p.on.getSrcNode()
                pDest = p.on.getDestNode()
                if agentSrc == pSrc and agentDest == pDest:
                    continue
                if agentDest == -1:
                    dist, path = self.graph.shortest_path(agentSrc, pSrc)
                    path.append(pDest)
                    listToCheck = [p.id, dist / p.value, path]
                    isIn = False
                    for i in pokemonsResult:
                        if i[2] == listToCheck[2]:
                            isIn = True
                            break
                    if isIn is False:
                        pokemonsResult.append(listToCheck)

                else:
                    dist, path = self.graph.shortest_path(agentDest, pSrc)
                    path.append(pDest)
                    listToCheck = [p.id, dist / p.value, path]
                    isIn = False
                    for i in pokemonsResult:
                        if i[2] == listToCheck[2]:
                            isIn = True
                            break
                    if isIn is False:
                        pokemonsResult.append(listToCheck)

            pathToAdd = []
            isFirst = True
            pokemonsResultSorted = sorted(pokemonsResult, key=lambda x: x[1])
            length = len(pokemonsResultSorted) - 1
            rangeResult = np.arange(length)
            for i in rangeResult:
                for j in range(len(pokemonsResultSorted[i][2])):
                    if j < len(pokemonsResultSorted[i + 1][2]) and pokemonsResultSorted[i][2][j] == pokemonsResultSorted[i + 1][2][j]:
                        pokemonsResultSorted[i + 1][2][j] = -1
                    else:
                        break
                if isFirst is True:
                    pathToAdd.extend(pokemonsResultSorted[i][2])
                    isFirst = False
                else:

                    while pokemonsResultSorted[i][2][0] == -1:
                        pokemonsResultSorted[i][2].pop(0)
                        if len(pokemonsResultSorted[i][2]) == 0:
                            pokemonsResultSorted.pop(i)
                            continue
                    if abs(pathToAdd[-1] - pokemonsResultSorted[i][2][0]) != 1:
                        dist, Path = self.graph.shortest_path(pathToAdd[-1], pokemonsResultSorted[i][2][0])
                        pathToAdd.extend(Path)
                        pathToAdd.extend(pokemonsResultSorted[i][2])

            if len(pokemonsResultSorted) == 0:
                return

            if len(pathToAdd) == 0:
                print(pokemonsResultSorted[0][2])
                pathToAdd = pokemonsResultSorted[0][2]
            agentsPath[0] = pathToAdd