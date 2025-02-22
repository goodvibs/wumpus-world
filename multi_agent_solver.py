from agent import Agent
from search_knowledge import SearchKnowledge
from cave_room import CaveRoom


class MultiAgentSolver:
    def __init__(self, cave_info):
        self.cave_info = cave_info
        self.search_knowledge = SearchKnowledge(len(cave_info.pits))
        self.agents = [Agent(CaveRoom(0, 0), self.search_knowledge, cave_info)]
        self.update_agents()
        self.gold_found = False

    def update_agents(self):
        for i in range(len(self.agents)):
            self.agents[i].update_knowledge()

    def explore_multiply(self):
        unvisited_safe_rooms = set()

        for agent in self.agents:
            unvisited_safe_neighbors = agent.unvisited_safe_neighbors()
            unvisited_safe_rooms = unvisited_safe_rooms.union(unvisited_safe_neighbors)

        new_agents = []
        for room in unvisited_safe_rooms:
            if room == self.cave_info.gold_location:
                self.gold_found = True
                return False
            new_agent = Agent(room, self.search_knowledge, self.cave_info)
            new_agents.append(new_agent)

        self.agents.extend(new_agents)
        self.update_agents()

        return len(new_agents) > 0

    def run(self):
        while self.explore_multiply():
            pass

        return self.gold_found
