# Simple Agent Network for Multi-Agent Collaboration
import threading, time, os
from .agent import SyntheticAgent

class AgentNetwork:
    def __init__(self, repo_id:str=None):
        self.agents = {}
        self.repo_id = repo_id or os.getenv("HF_DATASET_REPO")

    def register(self, name:str):
        agent = SyntheticAgent(name, self.repo_id)
        self.agents[name] = agent
        return agent

    def broadcast(self):
        while True:
            for a in self.agents.values():
                a.share_knowledge()
            time.sleep(60)

    def listen(self):
        while True:
            for a in self.agents.values():
                a.pull_knowledge()
            time.sleep(45)

    def start(self):
        threading.Thread(target=self.broadcast, daemon=True).start()
        threading.Thread(target=self.listen, daemon=True).start()
