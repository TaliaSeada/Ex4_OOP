"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the Client!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from implementation.GraphAlgo import GraphAlgo
from implementation.Game import Game
from implementation.Pokemon import Pokemon

# init pygame
WIDTH, HEIGHT = 1080, 720

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
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

print(client.get_info())
first_split = client.get_info().split(',')
print(first_split)
second_split = first_split[7].split(":")
print(second_split)
path = second_split[1].split('\"')[1]
algo = GraphAlgo()
algo.load_from_json("../" + path)
center, dist = algo.centerPoint()

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


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


radius = 15

print(client.get_pokemons())
print("{\"id\":" + str(center) + "}")
print("{\"id\":12}")
client.add_agent("{\"id\":" + str(center) + "}")
client.add_agent("{\"id\":" + str(center + 1) + "}")
client.add_agent("{\"id\":" + str(center - 1) + "}")
client.add_agent("{\"id\":" + str(center + 2) + "}")

# this commnad starts the server - the Client is running now
client.start()

"""
The implementation below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
game = Game(algo)
pokemonsFirst = json.loads(client.get_pokemons(),
                           object_hook=lambda d: SimpleNamespace(**d)).Pokemons
pokemonsFirst = [p.Pokemon for p in pokemonsFirst]
for p in pokemonsFirst:
    pikachu = Pokemon(p.value, p.type, p.pos)
    game.pokemons.append(pikachu)
agentsPath = []
game.setPokemonsEdges()

agentsFirst = json.loads(client.get_agents(),
                         object_hook=lambda d: SimpleNamespace(**d)).Agents
agentsFirst = [agent.Agent for agent in agentsFirst]

for a in agentsFirst:
    agentsPath.append([])

for p in game.pokemons:
    bestDist = float('inf')
    bestPath = []
    id = 0
    for a in agentsFirst:
        id = a.id
        if len(agentsPath[a.id]) == 0:
            dist, path = game.graph.shortest_path(a.src, p.on.getSrcNode())
            bestPath = path
            break
        else:
            dist, path = game.graph.shortest_path(agentsPath[a.id][-1], p.on.getSrcNode())
            if dist < bestDist:
                bestDist = dist
                bestPath = path
    agentsPath[id].extend(bestPath)

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    currPokemons = []

    for p in pokemons:
        pikachu = Pokemon(p.value, p.type, p.pos)
        currPokemons.append(pikachu)
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    for p in game.pokemons:
        if p not in currPokemons:
            game.pokemons.remove(p)

    for p in currPokemons:
        if p not in game.pokemons:
            game.pokemons.append(p)

    game.setPokemonsEdges()

    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(200, 200, 200))
    print(agents)
    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle

        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(150, 150, 200),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons
    for p in pokemons:
        if p.type == 1:
            pygame.draw.circle(screen, Color(203, 108, 200), (int(p.pos.x), int(p.pos.y)), 10)
        else:
            pygame.draw.circle(screen, Color(203, 108, 0), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    for agent in agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.Nodes)
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
# Client over:
