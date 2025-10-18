from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..agent_network import AgentNetwork
from ..consensus_engine import ConsensusEngine

router = APIRouter()
network = AgentNetwork()
consensus = ConsensusEngine(network)

@router.post("/collective/consensus")
async def run_consensus(req: Request):
    body = await req.json()
    proposition = body.get("proposition", "")
    if not proposition:
        return JSONResponse({"error": "No proposition provided."})
    record = consensus.consensus_round(proposition)
    return JSONResponse(record)

@router.get("/collective/history")
def history():
    return JSONResponse({"history": consensus.get_history()})
