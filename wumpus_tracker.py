from cave_bit_map import CaveBitmap
from hazard_tracker import HazardTracker


class WumpusTracker(HazardTracker):
    def deduce_hazard_locations(self):
        # check if there is only one configuration of possible wumpus location
        possible_rooms = []
        for room in self.filtered_possible_hazard_locations():
            neighbors_mask = room.neighbors_mask()
            if neighbors_mask & self.sense_map == self.sense_map:
                possible_rooms.append(room)

        possible_wumpus_map = CaveBitmap.from_rooms(possible_rooms)
        self.impossibility_map |= ~possible_wumpus_map

        if len(possible_rooms) == 1:
            self.all_hazards_found = True
            self.hazards_dangerous = False
