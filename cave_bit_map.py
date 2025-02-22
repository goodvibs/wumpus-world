from functools import reduce


def calc_bitshift(room):
    return (3 - room.row_from_top) * 4 + (3 - room.col_from_left)


def validate(bitmap):
    bitmap.validate()
    return bitmap


class CaveBitmap:
    BITMASK = 0xFFFF

    def __init__(self, value=0):
        self.value = value

    @classmethod
    def from_room(cls, room):
        res = cls()
        res.mark(room)
        return validate(res)

    @classmethod
    def from_rooms(cls, rooms):
        return validate(reduce(
            lambda acc, room: acc | room.mask(),
            rooms,
            cls()
        ))

    def mark(self, room):
        self.value |= 1 << calc_bitshift(room)
        self.validate()

    def mark_neighbors(self, room):
        self.value |= room.neighbors_mask().value

    def is_marked_at(self, room):
        self.validate()
        return self.value & (1 << calc_bitshift(room)) != 0

    def validate(self):
        assert self.value & self.BITMASK == self.value

    def __invert__(self):
        return validate(CaveBitmap(value=~self.value & self.BITMASK))

    def __and__(self, other):
        return validate(CaveBitmap(value=self.value & other.value))

    def __or__(self, other):
        return validate(CaveBitmap(value=self.value | other.value))

    def __xor__(self, other):
        return validate(CaveBitmap(value=self.value ^ other.value))

    def __repr__(self):
        self.validate()
        binary_str = '\n\t'.join(format(self.value, '019_b').split('_'))
        return f"BinaryMap(\n\t{binary_str}\n)"

    def __eq__(self, other):
        if other is None:
            return False

        self.validate()
        other.validate()

        return self.value == other.value
