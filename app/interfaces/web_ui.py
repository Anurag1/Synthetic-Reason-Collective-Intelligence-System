from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from ..core import SyntheticCore
core=SyntheticCore()
router=APIRouter()

@router.get('/',response_class=HTMLResponse)
def home():
    return open('templates/chat.html').read()

@router.post('/chat')
async def chat(req:Request):
    data=await req.json()
    text=data.get('text','')
    if text.lower().startswith('reflect'): reply=core.reflect()
    elif any(w in text.lower() for w in ['is','does','can','why','what','how','?']): reply=core.ask(text)
    else: reply=core.learn(text)
    return JSONResponse({'reply':reply})

@router.get('/graph')
def graph(): return JSONResponse(core.export_graph())


@router.get('/dashboard')
def dashboard():
    state = core.get_state()
    return JSONResponse(state)
