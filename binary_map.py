from functools import reduce


def calc_bitshift(room):
    return (3 - room.row_from_top) * 4 + (3 - room.col_from_left)


class BinaryMap:
    BITMASK = 0b1111_1111_1111_1111

    def __init__(self, value=0):
        self.value = value
        self.validate()

    @classmethod
    def from_room(cls, room):
        res = cls()
        res.mark(room)
        res.validate()
        return res

    @classmethod
    def from_rooms(cls, rooms):
        return reduce(
            lambda acc, room: acc | room.mask(),
            rooms,
            cls()
        )

    def mark(self, room):
        shift = calc_bitshift(room)
        self.value |= 1 << shift
        self.validate()

    def is_marked_at(self, room):
        self.validate()
        shift = calc_bitshift(room)
        return self.value & (1 << shift) != 0

    # def count_marked_rooms(self):
    #     self.validate()
    #     return self.value.bit_count()
    #
    # def get_marked_rooms(self):
    #     from room import Room
    #
    #     self.validate()
    #     markings = []
    #     for room in Room.iter_all():
    #         if self.is_marked_at(room):
    #             markings.append(room)
    #     return markings

    def validate(self):
        assert self.value & self.BITMASK == self.value

    def __invert__(self):
        self.validate()
        res = BinaryMap(value=~self.value & self.BITMASK)
        res.validate()
        return res

    def __and__(self, other):
        self.validate()
        res = BinaryMap(value=self.value & other.value)
        res.validate()
        return res

    def __or__(self, other):
        self.validate()
        res = BinaryMap(value=self.value | other.value)
        res.validate()
        return res

    def __xor__(self, other):
        self.validate()
        res = BinaryMap(value=self.value ^ other.value)
        res.validate()
        return res

    def __repr__(self):
        self.validate()
        binary_str = '\n\t'.join(format(self.value, '019_b').split('_'))
        return f"BinaryMap(\n\t{binary_str}\n)"

    def __eq__(self, other):
        return self.value == other.value
