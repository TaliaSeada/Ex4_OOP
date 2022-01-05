"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the Client!"
"""
import random
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

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into Object
first_split = client.get_info().split(',')
second_split = first_split[7].split(":")
path = second_split[1].split('\"')[1]
algo = GraphAlgo()
algo.load_from_json("../" + path)
center, dist = algo.centerPoint()

graph = json.loads(graph_json)
for n in graph["Nodes"]:
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

# TODO
client.add_agent("{\"id\":" + str(center) + "}")
client.add_agent("{\"id\":" + str(center) + "}")
client.add_agent("{\"id\":" + str(center) + "}")
client.add_agent("{\"id\":" + str(center) + "}")

# this commnad starts the server - the Client is running now
client.start()

game = Game(algo)
pokemonsFirst = json.loads(client.get_pokemons())
IDcounter = 0
for p in pokemonsFirst["Pokemons"]:
    p = p["Pokemon"]
    pikachu = Pokemon(p["value"], p["type"], p["pos"], IDcounter)
    game.pokemons.append(pikachu)
    IDcounter += 1
agentsPath = []
game.setPokemonsEdges()

agentsFirst = json.loads(client.get_agents())
agentsFirst = [agent["Agent"] for agent in agentsFirst["Agents"]]

for a in agentsFirst:
    agentsPath.append([])

# load Pokemons pictures
p1 = pygame.image.load("p1.png")
p2 = pygame.image.load("p2.png")
p3 = pygame.image.load("p3.png")
p4 = pygame.image.load("p4.png")
p5 = pygame.image.load("p5.png")
p6 = pygame.image.load("p6.png")
pictures = [p1, p2, p3, p4, p5, p6]
# rand = random.randint(0, 5)

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

    # stop button
    stop = Button(
        screen, 0, 0, 100, 40, text='Stop',
        fontSize=25, margin=5,
        inactiveColour=(255, 255, 255),
        pressedColour=(70, 70, 70), radius=0,
        onClick=lambda: client.stop()
    )

    # refresh surface
    screen.fill(Color(200, 200, 200))

    # background:
    bg = pygame.image.load("pokemon_background.jpeg")
    bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    screen.blit(bg, (0, 0))

    # Title
    title = pygame.image.load("title.png")
    title = pygame.transform.scale(title, (600, 350))
    screen.blit(title, (screen.get_width()/2-300, -140))

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

    # draw Pokemons:
    for p in pokemons:
        val = p['value']
        if val < 6:
            pic = pictures[0]
        elif val < 11:
            pic = pictures[1]
        elif val < 16:
            pic = pictures[2]
        elif val < 21:
            pic = pictures[3]
        elif val < 26:
            pic = pictures[4]
        else:
            pic = pictures[5]

        pic = pygame.transform.scale(pic, (200, 200))
        screen.blit(pic, (int(p["pos"].x)-90, int(p["pos"].y)-100))


    first_split = client.get_info().split(',')
    second_split = first_split[3].split(":")
    third_split = first_split[2].split(":")

    # display time:
    ttl = client.time_to_end()
    time = "time: " + str(ttl)

    # display score:
    scores = second_split[1]
    score = "scores: " + scores

    # display moves:
    moves = third_split[1]
    move = "moves: " + moves

    # text print:
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 20)

    textsurface = myfont.render(time, True, (255, 255, 255))
    screen.blit(textsurface, (0, 40))

    textsurface = myfont.render(score, True, (255, 255, 255))
    screen.blit(textsurface, (0, 70))

    textsurface = myfont.render(move, True, (255, 255, 255))
    screen.blit(textsurface, (0, 100))

    # update screen changes
    pygame_widgets.update(events)
    display.update()

    # refresh rate
    prevDest = [agent["dest"] for agent in agents]

    clock.tick(10)
    # choose next edge
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

    # move:
    client.move()
    # time.sleep(0.1)

# Client over:
client.stop()
pygame.quit()
