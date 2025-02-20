from binary_map import BinaryMap


class Room:
    neighbors_memo = [[None for _ in range(4)] for _ in range(4)]

    def __init__(self, row_from_top, col_from_left):
        self.row_from_top = row_from_top
        self.col_from_left = col_from_left
        self.directions = [self.up, self.down, self.left, self.right]

    def up(self):
        if self.row_from_top == 0:
            return None
        else:
            return Room(self.row_from_top - 1, self.col_from_left)

    def down(self):
        if self.row_from_top == 3:
            return None
        else:
            return Room(self.row_from_top + 1, self.col_from_left)

    def left(self):
        if self.col_from_left == 0:
            return None
        else:
            return Room(self.row_from_top, self.col_from_left - 1)

    def right(self):
        if self.col_from_left == 3:
            return None
        else:
            return Room(self.row_from_top, self.col_from_left + 1)

    def neighbors(self):
        memo_lookup = self.neighbors_memo[self.row_from_top][self.col_from_left]

        if memo_lookup is not None:
            return memo_lookup
        else:
            res = []
            for direction in self.directions:
                next_room = direction()
                if next_room is not None:
                    res.append(next_room)
            self.neighbors_memo[self.row_from_top][self.col_from_left] = res
            return res

    def mask(self):
        return BinaryMap.from_room(self)

    def neighbors_mask(self):
        mask = BinaryMap()
        for neighbor in self.neighbors():
            mask |= neighbor.mask()
        return mask

    def __eq__(self, other):
        return self.row_from_top == other.row_from_top and self.col_from_left == other.col_from_left

    def __hash__(self):
        return hash((self.row_from_top, self.col_from_left))

    def __repr__(self):
        return f"Room({self.row_from_top}, {self.col_from_left})"

    @classmethod
    def iter_all(cls):
        return iter(
            cls(row_from_top, col_from_side) for row_from_top in range(4) for col_from_side in range(4)
        )


class VisitInfo:
    def __init__(self, room, has_smell, has_wind):
        self.room = room
        self.has_smell = has_smell
        self.has_wind = has_wind

    def __eq__(self, other):
        return self.room == other.room and self.has_smell == other.has_smell and self.has_wind == other.has_wind