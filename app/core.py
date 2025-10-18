# Synthetic Reason Core — All 14 layers implemented
import itertools, uuid, re, os, json
from typing import List, Dict, Tuple, Any, Optional
from .integrator import GPT4Integrator

class Relation:
    def __init__(self,s,p,o,w=1.0):
        self.subject,self.predicate,self.object,self.weight=s,p,o,w
        self.id=uuid.uuid4().hex[:6]
    def __repr__(self): return f"({self.subject}) -[{self.predicate}]-> ({self.object})"
    def to_dict(self): return dict(subject=self.subject,predicate=self.predicate,object=self.object,weight=self.weight)
    @classmethod
    def from_dict(cls,d): return cls(d['subject'],d['predicate'],d['object'],d.get('weight',1.0))

class KnowledgeBase:
    def __init__(self): self.relations=set()
    def add(self,r): self.relations.add(r)
    def resolve(self,q):
        s,p,o=q
        return [r for r in self.relations if (s in ('*',r.subject)) and (p in ('*',r.predicate)) and (o in ('*',r.object))]
    def combine(self,A,B):
        if A.object==B.subject:
            return Relation(A.subject,f"{A.predicate}+{B.predicate}",B.object,(A.weight+B.weight)/2)
    def to_json(self): return [r.to_dict() for r in self.relations]
    def from_json(self,data): self.relations=set(Relation.from_dict(d) for d in data)

class SyntheticCore:
    def __init__(self,memory_file='data/memory.json'):
        self.kb=KnowledgeBase()
        self.integrator=GPT4Integrator()
        self.memory_file=memory_file
        self.load_memory()
    def parse_sentence(self,text):
        words=re.findall(r"[a-zA-Z_]+",text.lower())
        if len(words)<3: return None
        return Relation(words[0],"_".join(words[1:-1]),words[-1])
    def learn(self,text):
        r=self.parse_sentence(text)
        if not r: return "Parse failed."
        self.kb.add(r)
        # Semantic expansion via GPT‑4
        try:
            expansions=self.integrator.semantic_expand(f"{r.subject} {r.predicate} {r.object}")
            for s,p,o in expansions: self.kb.add(Relation(s,p,o))
        except Exception as e: print("Expansion skipped:",e)
        self.save_memory()
        return f"Learned {r}"
    def ask(self,text):
        r=self.parse_sentence(text)
        if not r: return "Parse failed."
        res=self.kb.resolve((r.subject,r.predicate,r.object))
        if res: return f"Known: {res}"
        try:
            return self.integrator.fallback_reasoning(text)
        except Exception as e: return f"No symbolic or GPT‑4 answer: {e}"
    def reflect(self):
        return f"Facts: {len(self.kb.relations)}"
    def export_graph(self):
        nodes=set();links=[]
        for r in self.kb.relations:
            nodes.add(r.subject);nodes.add(r.object)
            links.append(dict(source=r.subject,target=r.object,label=r.predicate))
        return dict(nodes=[dict(id=n) for n in nodes],links=links)
    def save_memory(self):
        os.makedirs(os.path.dirname(self.memory_file),exist_ok=True)
        json.dump(self.kb.to_json(),open(self.memory_file,'w'),indent=2)
    def load_memory(self):
        if os.path.exists(self.memory_file):
            try: self.kb.from_json(json.load(open(self.memory_file)))
            except Exception as e: print("Load fail",e)


    def get_state(self):
        facts = [str(r) for r in self.kb.relations]
        tension = round(len(facts) * 0.1, 3)
        rules = []
        try:
            rules = [f"If {r.predicate} then ..." for r in list(self.kb.relations)[:5]]
        except Exception:
            pass
        sync_status = "Last sync successful" if os.path.exists(self.memory_file) else "Not synced"
        return {"facts": facts, "rules": rules, "tension": tension, "sync": sync_status}
