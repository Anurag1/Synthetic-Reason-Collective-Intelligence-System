from fastapi import FastAPI
from .interfaces.web_ui import router as web_router
app=FastAPI()
app.include_router(web_router)

if __name__=='__main__':
    import uvicorn
    uvicorn.run('app.main:app',host='0.0.0.0',port=8000,reload=True)

from .interfaces.agent_api import router as agent_router
app.include_router(agent_router)

from .interfaces.collective_api import router as collective_router
app.include_router(collective_router)
