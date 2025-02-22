from agent import Agent
from agent_knowledge import AgentKnowledge
from cave_info import CaveInfo


class MultiAgentSolver:
    def __init__(self):
        self.agents = [Agent()]
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
            if room == CaveInfo.gold:
                self.gold_found = True
                return False
            new_agent = Agent(room=room)
            new_agents.append(new_agent)

        self.agents.extend(new_agents)
        self.update_agents()

        return len(new_agents) > 0

    def run(self):
        while self.explore_multiply():
            pass

        return self.gold_found
