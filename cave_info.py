from cave_bit_map import CaveBitmap


def create_sense_map(hazard_locations):
    sense_map = CaveBitmap()
    for room in hazard_locations:
        sense_map |= room.neighbors_mask()

    return sense_map


class CaveInfo:
    def __init__(self, gold_location, wumpus_location, pits):
        self.gold_location = gold_location
        self.wumpus_location = wumpus_location
        self.pits = pits
        self.smell_map = create_sense_map([wumpus_location])
        self.wind_map = create_sense_map(pits)
