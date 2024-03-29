from fastapi import FastAPI, APIRouter,Depends
import uvicorn
import aiofiles.os as aos
import asyncio
import os
from schemas import DBInfo, CellDB
from database import count_valid_cells, get_cells, get_cell
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from fastapi.responses import StreamingResponse
import aiofiles


app = FastAPI(docs_url="/docs")
router_cell = APIRouter(prefix="/cellapi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    print("Hello World")
    return {"message": "Hello World"}

@router_cell.get("/cells/databases/{db_name}", response_model=list[CellDB])
async def read_cell_db(db_name: str):
    print(db_name)
    print(f"./databases/{db_name}++++++++++++++++++++++++++++++++++++++")
    return await get_cells(f"./databases/{db_name}.db")

@router_cell.get("/cells/databases", response_model=list[DBInfo])
async def read_cell_dbs():
    loop = asyncio.get_event_loop()
    dbinfo_list = []
    for file in await loop.run_in_executor(None, lambda: [entry.name for entry in os.scandir("./databases/") if entry.is_file() and entry.name.endswith(".db")]):
        dbinfo_list.append(DBInfo(file_name=file, cell_count=await count_valid_cells(f"./databases/{file}")))
    return dbinfo_list

@router_cell.get("/cells/{db_name}/cell/{cell_id}/ph")
async def read_cell_ph(db_name: str, cell_id: str):
    cell: bytes = await get_cell(f"./databases/{db_name}.db", cell_id)
    image_ph = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    _, buffer = cv2.imencode(".png", image_ph)
    async with aiofiles.open("temp.png", "wb") as afp:
        await afp.write(buffer)
    return StreamingResponse(open("temp.png", "rb"), media_type="image/png")




    

app.include_router(router_cell)

if __name__ == "__main__":
    uvicorn.run("router:app", host="0.0.0.0", port=8000, reload=True)
