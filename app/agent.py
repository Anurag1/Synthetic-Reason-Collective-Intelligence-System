# Synthetic Multi-Agent Layer
import os, time, json
from .core import SyntheticCore
from .hf_persistence import HFDatasetMemory

class SyntheticAgent:
    def __init__(self, name:str, repo_id:str=None):
        self.name = name
        self.core = SyntheticCore()
        self.memory = HFDatasetMemory(repo_id)
        self.last_sync = 0
        print(f"🤝 Agent {self.name} initialized.")

    def share_knowledge(self):
        data = {"agent": self.name, "timestamp": time.time(), "facts": self.core.kb.to_json()}
        self.memory.save(data)
        self.last_sync = time.time()
        print(f"📤 Agent {self.name} shared knowledge.")

    def pull_knowledge(self):
        data = self.memory.load()
        if not data: return
        try:
            all_facts = data.get("facts", [])
            for f in all_facts:
                self.core.kb.add(self.core.kb.__class__.Relation.from_dict(f))
            print(f"📥 Agent {self.name} merged {len(all_facts)} facts.")
        except Exception as e:
            print("⚠️ Merge failed:", e)

    def negotiate(self, other_agent_state:dict):
        mine = {f"{r.subject}-{r.predicate}-{r.object}" for r in self.core.kb.relations}
        theirs = {f"{f['subject']}-{f['predicate']}-{f['object']}" for f in other_agent_state.get('facts', [])}
        diff = theirs - mine
        for d in diff:
            s,p,o = d.split('-')
            self.core.kb.add(self.core.kb.__class__.Relation(s,p,o))
        return f"🤝 Agent {self.name} adopted {len(diff)} new facts."
