"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the Client!"
"""
from types import SimpleNamespace

import numpy as np

from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from implementation.GraphAlgo import GraphAlgo
from implementation.Game import Game
from implementation.Pokemon import Pokemon
from itertools import groupby
import pygame_widgets
from pygame_widgets.button import Button
import time

# init pygame
WIDTH, HEIGHT = 1080, 720
EPS = 0.000001

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons)

print(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object
print(client.get_info())
first_split = client.get_info().split(',')
print(first_split)
second_split = first_split[7].split(":")
print(second_split)
path = second_split[1].split('\"')[1]
algo = GraphAlgo()
algo.load_from_json("../" + path)
center, dist = algo.centerPoint()

graph = json.loads(graph_json)
print(graph)
for n in graph["Nodes"]:
    print(n["pos"])
    x, y, _ = n["pos"].split(',')
    n["pos"] = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph["Nodes"]), key=lambda n: n["pos"].x)["pos"].x
min_y = min(list(graph["Nodes"]), key=lambda n: n["pos"].y)["pos"].y
max_x = max(list(graph["Nodes"]), key=lambda n: n["pos"].x)["pos"].x
max_y = max(list(graph["Nodes"]), key=lambda n: n["pos"].y)["pos"].y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


def distance(pos1, pos2):
    x = pos1.x - pos2.x
    y = pos1.y - pos2.y
    X = x * x
    Y = y * y
    res = (X + Y) ** 0.5
    return res


radius = 15

print(client.get_pokemons())
# print("{\"id\":" + str(center) + "}")
# print("{\"id\":12}")
client.add_agent("{\"id\":" + str(center) + "}")
client.add_agent("{\"id\":" + str(center) + "}")
client.add_agent("{\"id\":" + str(center) + "}")
client.add_agent("{\"id\":" + str(center) + "}")

# this commnad starts the server - the Client is running now
client.start()

game = Game(algo)
pokemonsFirst = json.loads(client.get_pokemons())
print(pokemonsFirst)
IDcounter = 0
for p in pokemonsFirst["Pokemons"]:
    p = p["Pokemon"]
    print(p)
    pikachu = Pokemon(p["value"], p["type"], p["pos"], IDcounter)
    game.pokemons.append(pikachu)
    IDcounter += 1
agentsPath = []
game.setPokemonsEdges()

agentsFirst = json.loads(client.get_agents())
print(agentsFirst)
agentsFirst = [agent["Agent"] for agent in agentsFirst["Agents"]]

for a in agentsFirst:
    agentsPath.append([])


def allocate(new_pokemons, agentsPath, agents):
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
                        dist, path = game.graph.shortest_path(a["dest"], p.on.getSrcNode())
                    else:
                        dist, path = game.graph.shortest_path(a["src"], p.on.getSrcNode())
                    bestid = id
                    bestPath = path
                    break
                else:
                    if agentsPath[id][-1] == p.on.getSrcNode():
                        path = []
                        dist = 0
                    else:
                        dist, path = game.graph.shortest_path(agentsPath[id][-1], p.on.getSrcNode())
                    path2, dist2 = game.graph.TSP(agentsPath[id])
                    if dist + dist2 < bestDist:
                        bestDist = dist + dist2
                        bestid = id
                        path2.extend(path)
                        isIn = False
                        for i in range(len(path2) - 1):
                            if path2[i] == p.on.getSrcNode() and path2[i + 1] == p.on.getDestNode() and len(path) == 0:
                                isIn = True
                                break
                        if not isIn:
                            if len(path) != 0 and abs(path[0] - path2[-1]) != 1:
                                dist, path3 = game.graph.shortest_path(path2[-1], path[0])
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
                    dist, Path = game.graph.shortest_path(pathToAdd[-1], pokemonsResultSorted[i][2][0])
                    pathToAdd.extend(Path)
                    pathToAdd.extend(pokemonsResultSorted[i][2])

        if len(pokemonsResultSorted) == 0:
            return

        if len(pathToAdd) == 0:
            print(pokemonsResultSorted[0][2])
            pathToAdd = pokemonsResultSorted[0][2]
        agentsPath[0] = pathToAdd


game.allocate(game.pokemons, agentsPath, agentsFirst)

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons())
    pokemons = [p["Pokemon"] for p in pokemons["Pokemons"]]
    currPokemons = []

    for p in pokemons:
        pikachu = Pokemon(p["value"], p["type"], p["pos"], IDcounter)
        IDcounter += 1
        currPokemons.append(pikachu)
        x, y, _ = p["pos"].split(',')
        p["pos"] = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    #
    new_pokemons = []
    for p in game.pokemons:
        if p not in currPokemons:
            game.pokemons.remove(p)

    for p in currPokemons:
        if p not in game.pokemons:
            game.pokemons.append(p)
            new_pokemons.append(p)

    game.setPokemonsEdges()

    agents = json.loads(client.get_agents())
    agents = [agent["Agent"] for agent in agents["Agents"]]

    # set the new Pokemon's path
    game.allocate(game.pokemons, agentsPath, agents)
    print(agentsPath[0])

    for a in agents:
        agentsPath[a["id"]] = [x[0] for x in groupby(agentsPath[a["id"]])]

    for a in agents:
        x, y, _ = a["pos"].split(',')
        a["pos"] = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            client.stop()
            pygame.quit()

            exit(0)

    stop = Button(
        screen, 0, 0, 100, 40, text='Stop',
        fontSize=25, margin=5,
        inactiveColour=(255, 255, 255),
        pressedColour=(70, 70, 70), radius=0,
        onClick=lambda: client.stop()
    )

    # refresh surface
    screen.fill(Color(200, 200, 200))
    # draw nodes
    for n in graph["Nodes"]:
        x = my_scale(n["pos"].x, x=True)
        y = my_scale(n["pos"].y, y=True)

        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n["id"]), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph["Edges"]:
        # find the edge nodes
        src = next(n for n in graph["Nodes"] if n["id"] == e["src"])
        dest = next(n for n in graph["Nodes"] if n["id"] == e["dest"])

        # scaled positions
        src_x = my_scale(src["pos"].x, x=True)
        src_y = my_scale(src["pos"].y, y=True)
        dest_x = my_scale(dest["pos"].x, x=True)
        dest_y = my_scale(dest["pos"].y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(150, 150, 200),
                           (int(agent["pos"].x), int(agent["pos"].y)), 10)
        id_srf = FONT.render(str(agent["id"]), True, Color(0, 0, 0))
        rect = id_srf.get_rect(center=(int(agent["pos"].x), int(agent["pos"].y)))
        screen.blit(id_srf, rect)

    # draw pokemons
    for p in pokemons:
        if p["type"] == 1:
            pygame.draw.circle(screen, Color(203, 108, 200), (int(p["pos"].x), int(p["pos"].y)), 10)
        else:
            pygame.draw.circle(screen, Color(203, 108, 0), (int(p["pos"].x), int(p["pos"].y)), 10)

    # update screen changes
    pygame_widgets.update(events)
    display.update()

    # refresh rate
    prevDest = [agent["dest"] for agent in agents]

    clock.tick(10)
    # choose next edge
    for agent in agents:
        if agent["dest"] == -1:
            # print(agentsPath[agent["id"]])
            if len(agentsPath[agent["id"]]) == 0:
                continue
            next_node = agentsPath[agent["id"]].pop(0)
            if agent["src"] == next_node:
                next_node = agentsPath[agent["id"]].pop(0)
            print('{"agent_id":' + str(agent["id"]) + ', "next_node_id":' + str(next_node) + '}')
            client.choose_next_edge(
                '{"agent_id":' + str(agent["id"]) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
            # print(agent)

    # move:
    client.move()
    # time.sleep(0.1)

# Client over:
client.stop()
pygame.quit()
