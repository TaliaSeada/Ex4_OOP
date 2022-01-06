from Client import Game
import math
import numpy as np



def getGraphFromClient(longString):
    first_split = longString.split(',')
    second_split = first_split[7].split(":")
    path = second_split[1].split('\"')[1]
    return path

def getNumOfAgents(longString):
    first_split = longString.split(',')
    second_split = first_split[-1].split(":")
    third_split = second_split[1].split("}")
    agentsNum = int(third_split[0])
    return agentsNum


def oneAgent(game, pokemonsResult):
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
                dist, Path = game.graph.shortest_path(pathToAdd[-1], pokemonsResultSorted[i][2][0])
                pathToAdd.extend(Path)
                pathToAdd.extend(pokemonsResultSorted[i][2])

    if len(pokemonsResultSorted) == 0:
        return

    if len(pathToAdd) == 0:
        pathToAdd = pokemonsResultSorted[0][2]
    return pathToAdd


def allocate(game: Game, pokemons, agentsPath, agents):
    if len(pokemons) == 0:
        return
    if len(agents) > 1:
        agentsPath = []
        resultList = []
        limit = math.floor(len(pokemons) / len(agents))
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
                dist, path = game.graph.shortest_path(a["src"], p.on.getSrcNode())
                dist += p.on.getWeight()
                pokDists.append([p, dist])
            pokDists = sorted(pokDists, key=lambda i: i[1])

            for i in range(limit):
                poksToAdd.append(pokDists.pop(0))
            isFirst = True
            for p in poksToAdd:
                if isFirst is True:
                    dist, path = game.graph.shortest_path(a["src"], p[0].on.getSrcNode())
                    p[0].agentAssigned = id
                    path.append(p[0].on.getDestNode())
                    isFirst = False
                    agentsPath[id].extend(path)
                else:
                    p[0].agentAssigned = id
                    dist, path = game.graph.shortest_path(agentsPath[id][-1], p[0].on.getSrcNode())
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
                dist, path = game.graph.shortest_path(agentSrc, pSrc)
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
                dist, path = game.graph.shortest_path(agentDest, pSrc)
                path.append(pDest)
                listToCheck = [p.id, dist / p.value, path]
                isIn = False
                for i in pokemonsResult:
                    if i[2] == listToCheck[2]:
                        isIn = True
                        break
                if isIn is False:
                    pokemonsResult.append(listToCheck)

        agentsPath[0] = game.oneAgent(pokemonsResult)

    return agentsPath

def chooseNextEdge(client, agents, agentsPath):
    for agent in agents:
        if agent["dest"] == -1:
            if len(agentsPath[agent["id"]]) == 0:
                continue
            next_node = agentsPath[agent["id"]].pop(0)
            if agent["src"] == next_node:
                next_node = agentsPath[agent["id"]].pop(0)
            client.choose_next_edge(
                '{"agent_id":' + str(agent["id"]) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

def addNewPokemons(game, currPokemons):
    for p in game.pokemons:
        if p not in currPokemons:
            game.pokemons.remove(p)

    for p in currPokemons:
        if p not in game.pokemons:
            game.pokemons.append(p)

    game.setPokemonsEdges()