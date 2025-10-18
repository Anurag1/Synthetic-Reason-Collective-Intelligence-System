# Synthetic Reason — Cognitive Chatbot (14 Layers + GPT-4 Integration)

Implements a complete symbolic cognitive architecture based on 14 layers, integrated with OpenAI GPT‑4 for hybrid reasoning and semantic expansion.

## Features
- Symbolic knowledge engine (14 layers)
- Persistent JSON memory
- Web chat interface (FastAPI + D3.js)
- Live knowledge graph visualization
- GPT‑4 fallback + expansion reasoning
- Self‑reflection, induction, and tension metrics

## Setup
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
uvicorn app.main:app --reload
```
Then open http://localhost:8000 in your browser.



## 💾 Hugging Face Dataset Persistence
This version supports saving and restoring chatbot memory to a Hugging Face dataset.

### Required Environment Variables
| Variable | Description |
|-----------|--------------|
| `HF_TOKEN` | Your Hugging Face access token |
| `HF_DATASET_REPO` | Dataset repo ID, e.g. `username/synthetic-reason-memory` |
| `OPENAI_API_KEY` | OpenAI GPT‑4 key |

Memory will automatically upload to the dataset after learning and download during startup.


## 🤝 Multi-Agent Collaboration Layer (Phase 15)
This version introduces distributed reasoning via multiple Synthetic Reason agents.

### Key Features
- Agents share and merge knowledge through a shared Hugging Face dataset.
- Automatic synchronization and contradiction negotiation.
- Each Hugging Face Space can act as one autonomous agent in the network.

### Environment Variables
| Variable | Description |
|-----------|--------------|
| `HF_TOKEN` | Hugging Face API token |
| `HF_DATASET_REPO` | Shared dataset ID (e.g., `username/synthetic-reason-collective`) |
| `OPENAI_API_KEY` | GPT‑4 key for reasoning |

Agents (e.g., Ares, Athena) will exchange facts and rules every 45–60 seconds, maintaining harmony across the collective.


## 🧠 Phase 16 — Collective Intelligence Consensus Engine
Adds distributed consensus across agents. Each agent votes on propositions and the collective decides via semantic harmony.

### Features
- Weighted voting on facts or hypotheses.
- Consensus aggregation with harmony/tension metrics.
- Results shown in live dashboard.

### API
- POST `/collective/consensus` → Run consensus on a proposition.
- GET `/collective/history` → Retrieve recent decisions.
