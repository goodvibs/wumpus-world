from agent_knowledge import AgentKnowledge
from cave_info import CaveInfo
from room import Room, VisitInfo


class Agent:
    def __init__(self, room=Room(0, 0)):
        self.location = room

    def senses_smell(self):
        return CaveInfo.smell_map.is_marked_at(self.location)

    def senses_wind(self):
        return CaveInfo.wind_map.is_marked_at(self.location)

    def update_knowledge(self):
        visit_info = VisitInfo(self.location, self.senses_smell(), self.senses_wind())
        AgentKnowledge.process_visit(visit_info)

    def safe_neighbors(self):
        safe_map = AgentKnowledge.safe_map()
        neighbors = self.location.neighbors()
        return [x for x in neighbors if safe_map.is_marked_at(x)]

    def unvisited_safe_neighbors(self):
        safe_neighbors = self.safe_neighbors()
        return [x for x in safe_neighbors if not AgentKnowledge.is_room_visited(x)]

    def __repr__(self):
        return f"Agent at {self.location}"
