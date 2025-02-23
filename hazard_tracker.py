from cave_bit_map import CaveBitmap
from cave_room import CaveRoom


class HazardTracker:
    ALL_POSSIBLE_SPAWN_LOCATIONS = frozenset(
        location for i, location in enumerate(CaveRoom.iter_all()) if i > 0
    )

    def __init__(self, search_knowledge):
        self.search_knowledge = search_knowledge
        self.sense_map = CaveBitmap()
        self.sense_adjacency_map = CaveBitmap()
        self.impossibility_map = CaveBitmap()
        self.all_hazards_found = False
        self.hazards_dangerous = True

    def mark_sensed_at(self, room):
        self.sense_map.mark(room)
        self.sense_adjacency_map.mark_neighbors(room)

    def mark_not_sensed_at(self, room):
        # No need to mark the room itself, as we must already know it's safe
        self.impossibility_map.mark_neighbors(room)

    def naive_possible_hazard_map(self):
        return self.sense_adjacency_map & ~self.impossibility_map & ~self.search_knowledge.visited_map

    def sensed_area_map(self):
        return self.sense_adjacency_map | self.impossibility_map | self.search_knowledge.visited_map

    def deduce_hazard_locations(self):
        raise NotImplementedError

    def unsafe_map(self):
        if not self.hazards_dangerous:
            return CaveBitmap()

        elif not self.all_hazards_found:
            self.deduce_hazard_locations()

            if not self.hazards_dangerous:
                return CaveBitmap()

        return self.naive_possible_hazard_map()

    def safe_map(self):
        return ~self.unsafe_map()

    def filtered_possible_hazard_locations(self, other_occupied_map=CaveBitmap()):
        possible_hazard_map = self.naive_possible_hazard_map() | ~self.sensed_area_map() & ~other_occupied_map

        return list(
            room for room in self.ALL_POSSIBLE_SPAWN_LOCATIONS
            if possible_hazard_map.is_marked_at(room)
        )
