from cave_room import VisitInfo


class Agent:
    def __init__(self, room, search_knowledge, cave_info):
        self.location = room
        self.search_knowledge = search_knowledge
        self.cave_info = cave_info

    def senses_smell(self):
        return self.cave_info.smell_map.is_marked_at(self.location)

    def senses_wind(self):
        return self.cave_info.wind_map.is_marked_at(self.location)

    def update_knowledge(self):
        visit_info = VisitInfo(self.location, self.senses_smell(), self.senses_wind())
        self.search_knowledge.process_visit(visit_info)

    def safe_neighbors(self):
        safe_map = self.search_knowledge.safe_map()
        neighbors = self.location.neighbors()
        return [x for x in neighbors if safe_map.is_marked_at(x)]

    def unvisited_safe_neighbors(self):
        safe_neighbors = self.safe_neighbors()
        return [x for x in safe_neighbors if not self.search_knowledge.is_room_visited(x)]

    def __repr__(self):
        return f"Agent at {self.location}"
