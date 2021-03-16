from typing import List

class Route:

    def __init__(self):
        self.name = ''
        self.id = 0
        self.opposite_id = 0
        self.origin = ''
        self.terminal = ''
        self.no = 0
        self.stops: List[Stop] = []


class Stop:

    def __init__(self):
        self.name = ''
        self.id = 0
        self.lng = 0
        self.lat = 0
        self.buses: List[Bus] = []


class Bus:

    def __init__(self):
        self.id = 0
        self.plate = ''
        self.lng = 0
        self.lat = 0
        self.distance = 0
        self.seconds = 0
        self.is_arrive = False
