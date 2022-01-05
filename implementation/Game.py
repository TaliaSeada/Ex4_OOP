import math

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

    def oneAgent(self, pokemonsResult):
        pathToAdd = []
        isFirst = True
        pokemonsResultSorted = sorted(pokemonsResult, key=lambda x: x[1])
        length = len(pokemonsResultSorted) - 1
        rangeResult = np.arange(length)
        for i in rangeResult:
            for j in range(len(pokemonsResultSorted[i][2])):
                if j < len(pokemonsResultSorted[i + 1][2]):
                    if pokemonsResultSorted[i][2][j] == pokemonsResultSorted[i + 1][2][j]:
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
                        break
                if len(pokemonsResultSorted[i][2]) != 0 and abs(pathToAdd[-1] - pokemonsResultSorted[i][2][0]) != 1:
                    dist, Path = self.graph.shortest_path(pathToAdd[-1], pokemonsResultSorted[i][2][0])
                    pathToAdd.extend(Path)
                    pathToAdd.extend(pokemonsResultSorted[i][2])

        if len(pokemonsResultSorted) == 0:
            return

        if len(pathToAdd) == 0:
            pathToAdd = pokemonsResultSorted[0][2]
        return pathToAdd

    def allocate(self, pokemons, agentsPath, agents):
        if len(pokemons) == 0:
            return
        if len(agents) > 1:
            agentsPath = []
            resultList = []
            limit = math.floor(len(pokemons)/len(agents))
            for a in agents:
                agentsPath.append([])
                resultList.append([])
            for p in pokemons:
                p.agentAssigned = -1
            for a in agents:
                id = a["id"]
                poksToAdd = []
                pokDists = []
                for p in pokemons:
                    if p.agentAssigned != -1:
                        continue
                    dist, path = self.graph.shortest_path(a["src"],p.on.getSrcNode())
                    dist += p.on.getWeight()
                    pokDists.append([p, dist])
                pokDists = sorted(pokDists, key=lambda i: i[1])

                for i in range(limit):
                    poksToAdd.append(pokDists.pop(0))
                isFirst = True
                for p in poksToAdd:
                    if isFirst is True:
                        dist, path = self.graph.shortest_path(a["src"], p[0].on.getSrcNode())
                        p[0].agentAssigned = id
                        path.append(p[0].on.getDestNode())
                        isFirst = False
                        agentsPath[id].extend(path)
                    else:
                        p[0].agentAssigned = id
                        dist, path = self.graph.shortest_path(agentsPath[id][-1], p[0].on.getSrcNode())
                        path.append(p[0].on.getDestNode())
                        agentsPath[id].extend(path)
        else:
            pokemonsResult = []
            for p in pokemons:
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

            agentsPath[0] = self.oneAgent(pokemonsResult)

        return agentsPath
