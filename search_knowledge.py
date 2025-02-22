from cave_bit_map import CaveBitmap
from cave_room import CaveRoom
from hazard_tracker import WumpusTracker, PitsTracker


class SearchKnowledge:
    def __init__(self, num_pits):
        self.visited_map = CaveBitmap()
        self.wumpus_tracker = WumpusTracker(self)
        self.pits_tracker = PitsTracker(num_pits, self)

    def is_room_visited(self, room):
        return self.visited_map.is_marked_at(room)

    def process_visit(self, visit_info):
        self.visited_map.mark(visit_info.room)

        if visit_info.has_smell:
            self.wumpus_tracker.mark_sensed_at(visit_info.room)
        else:
            self.wumpus_tracker.mark_not_sensed_at(visit_info.room)

        if visit_info.has_wind:
            self.pits_tracker.mark_sensed_at(visit_info.room)
        else:
            self.pits_tracker.mark_not_sensed_at(visit_info.room)

    def safe_map(self):
        return self.wumpus_tracker.safe_map() & self.pits_tracker.safe_map()

    def print(self):
        char_array = [[None for _ in range(4)] for _ in range(4)]

        wumpus_unsafe_map = ~self.wumpus_tracker.safe_map()
        pit_unsafe_map = ~self.pits_tracker.safe_map()

        for room in CaveRoom.iter_all():
            char = ''

            if wumpus_unsafe_map.is_marked_at(room):
                char += 'W'
                if self.wumpus_tracker.all_hazards_found:
                    char += '_'
                else:
                    char += '?'
            else:
                char += '__'

            if pit_unsafe_map.is_marked_at(room):
                char += 'P'
                if self.pits_tracker.all_hazards_found:
                    char += '_'
                else:
                    char += '?'
            else:
                char += '__'

            if self.wumpus_tracker.sense_map.is_marked_at(room):
                char += 's'
            else:
                char += '_'

            if self.pits_tracker.sense_map.is_marked_at(room):
                char += 'w'
            else:
                char += '_'

            if self.is_room_visited(room):
                char += 'v'
            else:
                char += '_'

            char_array[room.row_from_top][room.col_from_left] = char

        print('\n'.join([' '.join(row) for row in char_array]))
