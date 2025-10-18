# Collective Intelligence Consensus Engine
import time
from .agent_network import AgentNetwork

class ConsensusEngine:
    def __init__(self, network: AgentNetwork):
        self.network = network
        self.history = []

    def propose(self, proposition: str):
        votes = []
        for name, agent in self.network.agents.items():
            answer = agent.core.ask(proposition)
            confidence = 1.0 if "Known" in str(answer) else 0.5
            votes.append({"agent": name, "vote": confidence, "answer": str(answer)})
        return votes

    def aggregate(self, votes):
        total = sum(v["vote"] for v in votes)
        normalized = total / len(votes)
        decision = "accepted" if normalized >= 0.6 else "rejected"
        tension = round(1 - normalized, 3)
        return {"decision": decision, "tension": tension, "support": round(normalized,3)}

    def consensus_round(self, proposition: str):
        votes = self.propose(proposition)
        result = self.aggregate(votes)
        record = {"timestamp": time.time(), "proposition": proposition, "result": result, "votes": votes}
        self.history.append(record)
        return record

    def get_history(self):
        return self.history[-10:]
