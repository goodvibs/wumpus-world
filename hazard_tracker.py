import itertools
from functools import reduce

from agent_knowledge import AgentKnowledge
from binary_map import BinaryMap
from room import Room


def mark_neighbors(map_, room):
    for neighbor in room.neighbors():
        map_.mark(neighbor)


def generate_all_possible_spawn_locations():
    gen = Room.iter_all()
    next(gen)  # skip the first room
    return gen


class HazardTracker:
    ALL_POSSIBLE_SPAWN_LOCATIONS = list(generate_all_possible_spawn_locations())

    def __init__(self):
        self.sense_map = BinaryMap()
        self.possibility_map = BinaryMap()
        self.impossibility_map = BinaryMap()
        self.all_hazards_found = False
        self.hazards_dangerous = True

    def mark_sensed_at(self, room):
        self.sense_map.mark(room)
        mark_neighbors(self.possibility_map, room)

    def mark_not_sensed_at(self, room):
        # No need to mark the room itself, as we must already know it's safe
        mark_neighbors(self.impossibility_map, room)

    def naive_possible_hazard_map(self):
        return self.possibility_map & ~self.impossibility_map & ~AgentKnowledge.visited_map

    def sensed_area_map(self):
        return self.possibility_map | self.impossibility_map | AgentKnowledge.visited_map

    def deduce_hazard_locations(self):
        raise NotImplementedError

    def unsafe_map(self):
        if not self.hazards_dangerous:
            return BinaryMap()

        elif not self.all_hazards_found:
            self.deduce_hazard_locations()

        return self.naive_possible_hazard_map()

    def safe_map(self):
        return ~self.unsafe_map()

    def filtered_possible_hazard_locations(self, other_occupied_map=BinaryMap()):
        possible_hazard_map = self.naive_possible_hazard_map() | ~self.sensed_area_map() & ~other_occupied_map
        return filter(
            lambda room: possible_hazard_map.is_marked_at(room),
            self.ALL_POSSIBLE_SPAWN_LOCATIONS
        )


class WumpusTracker(HazardTracker):

    def deduce_hazard_locations(self):
        # check if there is only one configuration of possible wumpus location
        possible_rooms = []
        for room in self.filtered_possible_hazard_locations():
            neighbors_mask = room.neighbors_mask()
            if neighbors_mask & self.sense_map == self.sense_map:
                possible_rooms.append(room)

        possible_wumpus_map = BinaryMap.from_rooms(possible_rooms)
        self.impossibility_map |= ~possible_wumpus_map

        if len(possible_rooms) == 1:
            self.all_hazards_found = True
            self.hazards_dangerous = False


class PitsTracker(HazardTracker):
    
    def __init__(self, num_pits):
        self.num_pits = num_pits
        super().__init__()

    def filtered_possible_pit_configurations(self):
        possible_pit_locations = self.filtered_possible_hazard_locations()

        return itertools.combinations(possible_pit_locations, self.num_pits)

    def deduce_hazard_locations(self):
        # update wumpus location
        if AgentKnowledge.wumpus_tracker.all_hazards_found:
            self.impossibility_map |= AgentKnowledge.wumpus_tracker.naive_possible_hazard_map()

        # check if there is only one configuration of possible pit locations
        possible_configurations = []

        for room_combination in self.filtered_possible_pit_configurations():
            neighbors_mask = reduce(
                lambda acc, room: acc | room.neighbors_mask(),
                room_combination,
                BinaryMap()
            )

            if neighbors_mask & self.sense_map == self.sense_map:
                possible_configurations.append(room_combination)

        assert len(possible_configurations) != 0

        possible_pit_map = reduce(
            lambda acc, rooms_in_configuration: acc | BinaryMap.from_rooms(rooms_in_configuration),
            possible_configurations,
            BinaryMap()
        )
        self.impossibility_map |= ~possible_pit_map

        if len(possible_configurations) == 1:
            self.all_hazards_found = True
