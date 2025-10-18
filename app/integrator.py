# GPT‑4 Integration
import openai, os, re

class GPT4Integrator:
    def __init__(self):
        openai.api_key=os.getenv("OPENAI_API_KEY")
    def fallback_reasoning(self,query:str)->str:
        prompt=f"Explain the likely relationship: {query}"
        resp=openai.ChatCompletion.create(model="gpt-4-turbo",
                messages=[{"role":"system","content":"Cognitive reasoning assistant"},
                          {"role":"user","content":prompt}],
                max_tokens=300)
        return resp.choices[0].message['content']
    def semantic_expand(self,relation:str):
        prompt=f"Given '{relation}', suggest 3 related facts in 'subject predicate object' form."
        resp=openai.ChatCompletion.create(model="gpt-4-turbo",
                messages=[{"role":"system","content":"Symbolic reasoning model"},
                          {"role":"user","content":prompt}],
                max_tokens=150)
        text=resp.choices[0].message['content']
        triples=re.findall(r"([a-zA-Z_]+)\s+([a-zA-Z_]+)\s+([a-zA-Z_]+)",text)
        return triples
