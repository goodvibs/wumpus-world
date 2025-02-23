from functools import reduce
from itertools import combinations

from cave_bit_map import CaveBitmap
from hazard_tracker import HazardTracker


class PitConfigurationsCache:
    def __init__(self):
        self.cache = [None for _ in range(2 ** 16)]

    @staticmethod
    def calc_key(possible_pit_locations):
        return CaveBitmap.from_rooms(possible_pit_locations).value

    def lookup(self, possible_pit_locations):
        key = self.calc_key(possible_pit_locations)
        return self.cache[key]

    def store(self, possible_pit_locations, configurations):
        key = self.calc_key(possible_pit_locations)
        self.cache[key] = configurations

    def __getitem__(self, possible_pit_locations):
        return self.lookup(possible_pit_locations)

    def __setitem__(self, possible_pit_locations, configurations):
        self.store(possible_pit_locations, configurations)


class PitsTracker(HazardTracker):
    pit_configurations_caches = [PitConfigurationsCache() for _ in range(3)]
    k_rooms_combination_neighbors_mask_lookup = {}

    def __init__(self, num_pits, search_knowledge):
        self.num_pits = num_pits
        super().__init__(search_knowledge)

    @classmethod
    def initialize_k_rooms_combination_neighbors_mask_lookup(cls):
        for num_pits in range(1, 4):
            for rooms_combination in combinations(cls.ALL_POSSIBLE_SPAWN_LOCATIONS, num_pits):
                cls.k_rooms_combination_neighbors_mask_lookup[rooms_combination] = reduce(
                    lambda acc, room: acc | room.neighbors_mask(),
                    rooms_combination,
                    CaveBitmap()
                )

    @classmethod
    def k_rooms_combination_neighbors_mask(cls, rooms_combination):
        return cls.k_rooms_combination_neighbors_mask_lookup.get(rooms_combination)

    def filtered_possible_pit_configurations(self):
        possible_pit_locations = self.filtered_possible_hazard_locations()

        cache_index = self.num_pits - 1
        cache_lookup = self.pit_configurations_caches[cache_index][possible_pit_locations]

        if cache_lookup is None:
            self.pit_configurations_caches[cache_index][possible_pit_locations] = cache_lookup = list(
                combinations(possible_pit_locations, self.num_pits)
            )

        return cache_lookup

    def deduce_hazard_locations(self):
        # update wumpus location
        if self.search_knowledge.wumpus_tracker.all_hazards_found:
            self.impossibility_map |= self.search_knowledge.wumpus_tracker.naive_possible_hazard_map()

        # check if there is only one configuration of possible pit locations
        num_possible_configurations = 0
        possible_pit_map = CaveBitmap()

        for room_combination in self.filtered_possible_pit_configurations():
            neighbors_mask = self.k_rooms_combination_neighbors_mask(room_combination)

            if neighbors_mask & self.sense_map == self.sense_map:
                possible_pit_map |= CaveBitmap.from_rooms(room_combination)
                num_possible_configurations += 1

        assert num_possible_configurations != 0

        if num_possible_configurations == 1:
            self.all_hazards_found = True

        self.impossibility_map |= ~possible_pit_map


# Initialize
PitsTracker.initialize_k_rooms_combination_neighbors_mask_lookup()
