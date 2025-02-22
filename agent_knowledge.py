from cave_bit_map import CaveBitmap
from cave_room import CaveRoom


class AgentKnowledge:
    wumpus_tracker = None
    pits_tracker = None

    visited_map = CaveBitmap()

    @classmethod
    def is_room_visited(cls, room):
        return cls.visited_map.is_marked_at(room)

    @classmethod
    def process_visit(cls, visit_info):
        cls.visited_map.mark(visit_info.room)

        if visit_info.has_smell:
            cls.wumpus_tracker.mark_sensed_at(visit_info.room)
        else:
            cls.wumpus_tracker.mark_not_sensed_at(visit_info.room)

        if visit_info.has_wind:
            cls.pits_tracker.mark_sensed_at(visit_info.room)
        else:
            cls.pits_tracker.mark_not_sensed_at(visit_info.room)

    @classmethod
    def safe_map(cls):
        return cls.wumpus_tracker.safe_map() & cls.pits_tracker.safe_map()

    @classmethod
    def print(cls):
        char_array = [[None for _ in range(4)] for _ in range(4)]

        wumpus_unsafe_map = ~cls.wumpus_tracker.safe_map()
        pit_unsafe_map = ~cls.pits_tracker.safe_map()

        for room in CaveRoom.iter_all():
            char = ''

            if wumpus_unsafe_map.is_marked_at(room):
                char += 'W'
                if cls.wumpus_tracker.all_hazards_found:
                    char += '_'
                else:
                    char += '?'
            else:
                char += '__'

            if pit_unsafe_map.is_marked_at(room):
                char += 'P'
                if cls.pits_tracker.all_hazards_found:
                    char += '_'
                else:
                    char += '?'
            else:
                char += '__'

            if cls.wumpus_tracker.sense_map.is_marked_at(room):
                char += 's'
            else:
                char += '_'

            if cls.pits_tracker.sense_map.is_marked_at(room):
                char += 'w'
            else:
                char += '_'

            if cls.is_room_visited(room):
                char += 'v'
            else:
                char += '_'

            char_array[room.row_from_top][room.col_from_left] = char

        print('\n'.join([' '.join(row) for row in char_array]))
