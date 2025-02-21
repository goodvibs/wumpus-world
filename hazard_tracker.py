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

    def all_found(self):
        raise NotImplementedError

    def safe_map(self):
        raise NotImplementedError

    def filtered_possible_hazard_locations(self, other_occupied_map=BinaryMap()):
        possible_hazard_map = self.naive_possible_hazard_map() | ~self.sensed_area_map() & ~other_occupied_map
        return filter(
            lambda room: possible_hazard_map.is_marked_at(room),
            self.ALL_POSSIBLE_SPAWN_LOCATIONS
        )


class WumpusTracker(HazardTracker):

    def __init__(self):
        self.known_wumpus_location = None
        super().__init__()

    def get_wumpus_location(self):
        if self.known_wumpus_location is not None:
            return self.known_wumpus_location

        naive_possible_wumpus_map = self.naive_possible_hazard_map()
        num_possible_rooms = naive_possible_wumpus_map.count_marked_rooms()

        if num_possible_rooms == 1:
            self.known_wumpus_location = naive_possible_wumpus_map.get_marked_rooms()[0]
            return self.known_wumpus_location

        elif num_possible_rooms > 1:
            # check if there is only one configuration of possible wumpus location
            possible_rooms = []
            for room in self.filtered_possible_hazard_locations():
                neighbors_mask = room.neighbors_mask()
                if neighbors_mask & self.sense_map == self.sense_map:
                    possible_rooms.append(room)
            
            if len(possible_rooms) == 1:
                self.known_wumpus_location = possible_rooms[0]
                return self.known_wumpus_location
            else:
                return None
        else:
            return None

    def safe_map(self):
        if self.get_wumpus_location() is not None:
            # wumpus is found and therefore dead
            return ~BinaryMap()
        else:
            return ~self.naive_possible_hazard_map()


class PitsTracker(HazardTracker):
    
    def __init__(self, num_pits):
        self.num_pits = num_pits
        self.known_pit_map = None
        super().__init__()

    def filtered_possible_pit_configurations(self):
        possible_pit_locations = self.filtered_possible_hazard_locations()

        return itertools.combinations(possible_pit_locations, self.num_pits)

    def get_pit_map(self):
        if self.known_pit_map is not None:
            return self.known_pit_map

        # update wumpus location
        if AgentKnowledge.wumpus_tracker.known_wumpus_location is not None:
            self.impossibility_map.mark(AgentKnowledge.wumpus_tracker.known_wumpus_location)

        # check if there is only one configuration of possible pit locations
        possible_configurations = []

        for k_rooms in self.filtered_possible_pit_configurations():
            neighbors_mask = reduce(
                lambda acc, room: acc | room.neighbors_mask(),
                k_rooms,
                BinaryMap()
            )

            if neighbors_mask & self.sense_map == self.sense_map:
                possible_configurations.append(k_rooms)

        assert len(possible_configurations) != 0

        possible_pit_map = reduce(
            lambda acc, rooms_in_configuration: acc | reduce(
                lambda acc, room: acc | room.mask(),
                rooms_in_configuration,
                BinaryMap()
            ),
            possible_configurations,
            BinaryMap()
        )
        self.impossibility_map |= ~possible_pit_map

        if len(possible_configurations) == 1:
            self.known_pit_map = possible_pit_map

        return self.known_pit_map

    def safe_map(self):
        pit_map = self.get_pit_map()

        if pit_map is not None:
            return ~pit_map
        else:
            return ~self.naive_possible_hazard_map()
