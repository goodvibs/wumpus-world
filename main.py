from cave_info import CaveInfo
from cave_room import CaveRoom
from multi_agent_solver import MultiAgentSolver


def wumpus_world(cave_map):
    gold_location = None
    wumpus_location = None
    pits = []

    for room in CaveRoom.iter_all():
        room_char = cave_map[room.row_from_top][room.col_from_left]

        if room_char == 'W':
            wumpus_location = room
        elif room_char == 'P':
            pits.append(room)
        elif room_char == 'G':
            gold_location = room

    cave_info = CaveInfo(gold_location, wumpus_location, pits)
    solver = MultiAgentSolver(cave_info)

    return solver.run()


def main():
    cave = [
        [*"__GP"],
        [*"_P__"],
        [*"W___"],
        [*"____"]
    ]

    assert wumpus_world(cave) is True


if __name__ == '__main__':
    main()
