from cave_bit_map import CaveBitmap


class CaveRoom:
    neighbors_lookup = [[None for _ in range(4)] for _ in range(4)]
    neighbors_mask_lookup = [[None for _ in range(4)] for _ in range(4)]

    def __init__(self, row_from_top, col_from_left):
        self.row_from_top = row_from_top
        self.col_from_left = col_from_left
        self.directions = [self.up, self.down, self.left, self.right]

    def up(self):
        if self.row_from_top == 0:
            return None
        else:
            return CaveRoom(self.row_from_top - 1, self.col_from_left)

    def down(self):
        if self.row_from_top == 3:
            return None
        else:
            return CaveRoom(self.row_from_top + 1, self.col_from_left)

    def left(self):
        if self.col_from_left == 0:
            return None
        else:
            return CaveRoom(self.row_from_top, self.col_from_left - 1)

    def right(self):
        if self.col_from_left == 3:
            return None
        else:
            return CaveRoom(self.row_from_top, self.col_from_left + 1)

    def calc_neighbors(self):
        return [direction() for direction in self.directions if direction() is not None]

    def neighbors(self):
        return CaveRoom.neighbors_lookup[self.row_from_top][self.col_from_left]

    def mask(self):
        return CaveBitmap.from_room(self)

    def neighbors_mask(self):
        return CaveRoom.neighbors_mask_lookup[self.row_from_top][self.col_from_left]

    def calc_neighbors_mask(self):
        self_mask_value = self.mask().value

        left_mask_value = (self_mask_value << 1) & ~0x1111
        right_mask_value = (self_mask_value >> 1) & ~0x8888
        up_mask_value = self_mask_value << 4
        down_mask_value = self_mask_value >> 4

        mask_value = (left_mask_value | right_mask_value | up_mask_value | down_mask_value) & CaveBitmap.BITMASK
        return CaveBitmap(mask_value)

    def __eq__(self, other):
        return other is not None and self.row_from_top == other.row_from_top and self.col_from_left == other.col_from_left

    def __hash__(self):
        return hash((self.row_from_top, self.col_from_left))

    def __repr__(self):
        return f"Room({self.row_from_top}, {self.col_from_left})"

    @classmethod
    def iter_all(cls):
        return iter(
            cls(row_from_top, col_from_side) for row_from_top in range(4) for col_from_side in range(4)
        )

    @classmethod
    def initialize_neighbors_lookup(cls):
        for room in cls.iter_all():
            cls.neighbors_lookup[room.row_from_top][room.col_from_left] = room.calc_neighbors()

    @classmethod
    def initialize_neighbors_mask_lookup(cls):
        for room in cls.iter_all():
            cls.neighbors_mask_lookup[room.row_from_top][room.col_from_left] = room.calc_neighbors_mask()


class VisitInfo:
    def __init__(self, room, has_smell, has_wind):
        self.room = room
        self.has_smell = has_smell
        self.has_wind = has_wind

    def __eq__(self, other):
        return self.room == other.room and self.has_smell == other.has_smell and self.has_wind == other.has_wind


# Initialize after the class definition
CaveRoom.initialize_neighbors_lookup()
CaveRoom.initialize_neighbors_mask_lookup()
