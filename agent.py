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

    # def safe_neighbors(self):
    #     safe_map = self.search_knowledge.safe_map()
    #     neighbors = self.location.neighbors()
    #     return [x for x in neighbors if safe_map.is_marked_at(x)]

    def is_useless(self):
        # return True if agent has no unvisited neighbors or all unvisited neighbors are pits
        unvisited_neighbors = self.unvisited_neighbors()
        if len(unvisited_neighbors) == 0:
            print(self.location)
            return True
        elif not self.search_knowledge.pits_tracker.all_hazards_found:
            return False
        else:
            return False
            # for neighbor in unvisited_neighbors:
            #     if self.search_knowledge.pits_tracker.naive_possible_hazard_map().is_marked_at(neighbor):
            #         return False
            # return True

    def unvisited_neighbors(self):
        neighbors = self.location.neighbors()
        return [x for x in neighbors if not self.search_knowledge.is_room_visited(x)]

    # def unvisited_safe_neighbors(self):
    #     safe_neighbors = self.safe_neighbors()
    #     return [x for x in safe_neighbors if not self.search_knowledge.is_room_visited(x)]

    def __repr__(self):
        return f"Agent at {self.location}"
