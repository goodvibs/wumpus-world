from agent import Agent
from search_knowledge import SearchKnowledge
from cave_room import CaveRoom


class MultiAgentSolver:
    def __init__(self, cave_info):
        self.cave_info = cave_info
        self.search_knowledge = SearchKnowledge(len(cave_info.pits))
        self.agents = [Agent(CaveRoom(0, 0), self.search_knowledge, cave_info)]
        self.gold_found = False
        self.safe_map = None
        self.update()

    def update_agents(self):
        for i in range(len(self.agents)):
            self.agents[i].update_knowledge()

    def update_safe_map(self):
        self.safe_map = self.search_knowledge.safe_map()

    def update(self):
        self.update_agents()
        self.update_safe_map()

    def explore_multiply(self):
        unvisited_safe_rooms = set()

        for agent in self.agents:
            unvisited_neighbors = agent.unvisited_neighbors()
            safe_unvisited_neighbors = [x for x in unvisited_neighbors if self.safe_map.is_marked_at(x)]
            unvisited_safe_rooms = unvisited_safe_rooms.union(safe_unvisited_neighbors)

        new_agents = []
        for room in unvisited_safe_rooms:
            if room == self.cave_info.gold_location:
                self.gold_found = True
                return False
            new_agent = Agent(room, self.search_knowledge, self.cave_info)
            new_agents.append(new_agent)

        self.agents.extend(new_agents)
        self.update()

        return len(new_agents) > 0

    def prune_agents(self):
        self.agents = [agent for agent in self.agents if not agent.is_useless()]

    def run(self):
        while self.explore_multiply():
            # self.search_knowledge.print()
            # print()
            self.prune_agents()

        return self.gold_found
