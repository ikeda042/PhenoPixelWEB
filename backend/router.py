from fastapi import FastAPI, APIRouter
import uvicorn
import aiofiles.os as aos
import asyncio
import os
from schemas import DBname

app = FastAPI(docs_url="/docs")
router_cell = APIRouter(prefix="/cellapi")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@router_cell.get("/cells/databases", response_model=list[DBname])
async def get_database_names():
    loop = asyncio.get_event_loop()
    files = await loop.run_in_executor(None, lambda: [entry.name for entry in os.scandir("/") if entry.is_file() and entry.name.endswith(".db")])
    return [DBname(name=file) for file in files]

app.include_router(router_cell)

if __name__ == "__main__":
    uvicorn.run("router:app", host="0.0.0.0", port=8000, reload=True)
