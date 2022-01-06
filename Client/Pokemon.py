from implementation.Node import Edge

"""
This class will represent a pokemon object
"""


class Pokemon:
    def __init__(self, value: float, type: int, pos, id):
        self.id = id
        self.value = value
        self.type = type
        split = pos.split(",")
        self.pos = [float(split[0]), float(split[1])]
        self.on = None
        self.agentAssigned = -1

    # override to compare between pokemons
    def __eq__(self, other):
        if self.value == other.value and self.type == other.type and self.pos == other.pos:
            return True
        return False
