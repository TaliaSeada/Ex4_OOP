from implementation.Node import Edge


class Pokemon:
    def __init__(self, value: float, type: int, pos):
        self.value = value
        self.type = type
        split = pos.split(",")
        self.pos = [float(split[0]), float(split[1])]
        self.on = None

    def __eq__(self, other):
        if self.value == other.value and self.type == other.type and self.pos == other.pos and self.on == other.on:
            return True
        return False