import Edge


class Pokemon:
    def __init__(self, value: float, type: int, pos, on: Edge):
        self.value = value
        self.type = type
        self.pos = pos
        self.on = on
