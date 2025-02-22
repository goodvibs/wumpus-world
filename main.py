from agent_knowledge import AgentKnowledge
from cave_bit_map import CaveBitmap
from cave_info import CaveInfo
from cave_room import CaveRoom
from hazard_tracker import WumpusTracker, PitsTracker
from multi_agent_solver import MultiAgentSolver


def create_sense_map(sources):
    sensing_rooms = []
    for source in sources:
        sensing_rooms.extend(source.neighbors())

    sensing_map = CaveBitmap()

    for sensing_room in sensing_rooms:
        sensing_map.mark(sensing_room)

    return sensing_map


def wumpus_world(cave_map):
    for room in CaveRoom.iter_all():
        room_char = cave_map[room.row_from_top][room.col_from_left]

        if room_char == 'W':
            CaveInfo.wumpus = room
        elif room_char == 'P':
            CaveInfo.pits.append(room)
        elif room_char == 'G':
            CaveInfo.gold = room

    AgentKnowledge.wumpus_tracker = WumpusTracker()
    AgentKnowledge.pits_tracker = PitsTracker(len(CaveInfo.pits))

    CaveInfo.wind_map = create_sense_map(CaveInfo.pits)
    CaveInfo.smell_map = create_sense_map([CaveInfo.wumpus])

    solver = MultiAgentSolver()
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
