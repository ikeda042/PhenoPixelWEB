from fastapi import FastAPI, APIRouter,Depends
import uvicorn
import aiofiles.os as aos
import asyncio
import os
from schemas import DBInfo, CellDB
from database import count_valid_cells, get_cells, get_cell_ph, get_cell_fluo, get_cell_contour
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from fastapi.responses import StreamingResponse, FileResponse
import aiofiles
import pickle
import matplotlib.pyplot as plt
from functions import draw_scale_bar_with_centered_text, basis_conversion, replot_blocking_operations
from fastapi.params import Query
from numpy.linalg import inv
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import aiofiles
import base64
from io import BytesIO



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

@router_cell.get("/cells/databases/{db_name}/sqliteexport")
async def read_cell_db(db_name: str):
    return FileResponse(
        path=f"./databases/{db_name}.db",
        headers={"Content-Disposition": f"attachment; filename={db_name}.db"},
    )
@router_cell.get("/cells/databases", response_model=list[DBInfo])
async def read_cell_dbs():
    loop = asyncio.get_event_loop()
    dbinfo_list = []
    for file in await loop.run_in_executor(None, lambda: [entry.name for entry in os.scandir("./databases/") if entry.is_file() and entry.name.endswith(".db")]):
        dbinfo_list.append(DBInfo(file_name=file, cell_count=await count_valid_cells(f"./databases/{file}")))
    return dbinfo_list

@router_cell.get("/cells/{db_name}/cell/{cell_id}/ph")
async def read_cell_ph(db_name: str, cell_id: str,draw_scale_bar: bool = Query(default=True)):
    cell: bytes = await get_cell_ph(f"./databases/{db_name}.db", cell_id)
    image_ph = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    if draw_scale_bar:
        image_ph = await draw_scale_bar_with_centered_text(image_ph)
    _, buffer = cv2.imencode(".png", image_ph)
    async with aiofiles.open("temp.png", "wb") as afp:
        await afp.write(buffer)
    return StreamingResponse(open("temp.png", "rb"), media_type="image/png")

@router_cell.get("/cells/{db_name}/cell/{cell_id}/phcontour")
async def read_cell_ph_contour(db_name: str, cell_id: str,draw_scale_bar: bool = Query(default=True)):
    cell: bytes = await get_cell_ph(f"./databases/{db_name}.db", cell_id)
    image_ph = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    if draw_scale_bar:
        image_ph = await draw_scale_bar_with_centered_text(image_ph)
    contour = await get_cell_contour(f"./databases/{db_name}.db", cell_id)
    cv2.drawContours(image_ph,pickle.loads(contour),-1,(0,255,0),1)
    _, buffer = cv2.imencode(".png", image_ph)
    async with aiofiles.open("temp_phcontour.png", "wb") as afp:
        await afp.write(buffer)
    return StreamingResponse(open("temp_phcontour.png", "rb"), media_type="image/png")


@router_cell.get("/cells/{db_name}/cell/{cell_id}/fluo")
async def read_cell_fluo(db_name: str, cell_id: str,draw_scale_bar: bool = Query(default=True)):
    cell: bytes = await get_cell_fluo(f"./databases/{db_name}.db", cell_id)
    image_fluo = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    if draw_scale_bar:
        image_fluo = await draw_scale_bar_with_centered_text(image_fluo)
    _, buffer = cv2.imencode(".png", image_fluo)
    async with aiofiles.open("temp_fluo.png", "wb") as afp:
        await afp.write(buffer)
    return StreamingResponse(open("temp_fluo.png", "rb"), media_type="image/png")


@router_cell.get("/cells/{db_name}/cell/{cell_id}/fluox5")
async def read_cell_fluo5(db_name: str, cell_id: str,draw_scale_bar: bool = Query(default=True)):
    cell: bytes = await get_cell_fluo(f"./databases/{db_name}.db", cell_id)
    image_fluo = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_fluo = cv2.convertScaleAbs(image_fluo, alpha=5, beta=0)
    if draw_scale_bar:
        image_fluo = await draw_scale_bar_with_centered_text(image_fluo)
    _, buffer = cv2.imencode(".png", image_fluo)
    async with aiofiles.open("temp_fluo5.png", "wb") as afp:
        await afp.write(buffer)
    return StreamingResponse(open("temp_fluo5.png", "rb"), media_type="image/png")


@app.get("/cells/{db_name}/overview/cell/{cell_id}")
async def read_cell_for_overview(db_name: str, cell_id: str, draw_scale_bar: bool = Query(default=True)):
    cell: bytes = await get_cell_fluo(f"./databases/{db_name}.db", cell_id)
    image_fluo = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_fluo = cv2.convertScaleAbs(image_fluo, alpha=2, beta=0)
    contour = await get_cell_contour(f"./databases/{db_name}.db", cell_id)
    cv2.drawContours(image_fluo,pickle.loads(contour),-1,(0,255,0),1)
    if draw_scale_bar:
        image_fluo = await draw_scale_bar_with_centered_text(image_fluo)
    _, buffer = cv2.imencode(".png", image_fluo)
    base64_image = base64.b64encode(buffer).decode("utf-8")
    return {"image": base64_image}


@router_cell.get("/cells/{db_name}/cell/{cell_id}/fluocontour")
async def read_cell_fluo_contour(db_name: str, cell_id: str,draw_scale_bar: bool = Query(default=True)):
    cell: bytes = await get_cell_fluo(f"./databases/{db_name}.db", cell_id)
    image_fluo = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    if draw_scale_bar:
        image_fluo = await draw_scale_bar_with_centered_text(image_fluo)
    contour = await get_cell_contour(f"./databases/{db_name}.db", cell_id)
    cv2.drawContours(image_fluo,pickle.loads(contour),-1,(0,255,0),1)
    _, buffer = cv2.imencode(".png", image_fluo)
    async with aiofiles.open("temp_fluocontour.png", "wb") as afp:
        await afp.write(buffer)
    return StreamingResponse(open("temp_fluocontour.png", "rb"), media_type="image/png")

@router_cell.get("/cells/{db_name}/cell/{cell_id}/fluohadamard")
async def read_cell_fluo_hadamard(db_name: str, cell_id: str,draw_scale_bar: bool = Query(default=True)):
    cell: bytes = await get_cell_fluo(f"./databases/{db_name}.db", cell_id)
    contour = await get_cell_contour(f"./databases/{db_name}.db", cell_id)
    image_fluo = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    mask = np.zeros((image_fluo.shape[0], image_fluo.shape[0]), dtype=np.uint8)
    cv2.fillPoly(mask, [pickle.loads(contour)], 1)
    output_image = cv2.bitwise_and(image_fluo, image_fluo, mask=mask)
    output_image[:, :, 0] = 0
    output_image[:, :, 2] = 0
    if draw_scale_bar:
        output_image = await draw_scale_bar_with_centered_text(output_image)
    _, buffer = cv2.imencode(".png", output_image)
    async with aiofiles.open("temp_fluohadamard.png", "wb") as afp:
        await afp.write(buffer)
    return StreamingResponse(open("temp_fluohadamard.png", "rb"), media_type="image/png")


@router_cell.get("/cells/{db_name}/cell/{cell_id}/replot")
async def replot(db_name: str, cell_id: str):
    plt.style.use("dark_background")
    cell: bytes = await get_cell_fluo(f"./databases/{db_name}.db", cell_id)
    image_fluo = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_fluo = cv2.cvtColor(image_fluo, cv2.COLOR_BGR2GRAY)
    contour_raw = await get_cell_contour(f"./databases/{db_name}.db", cell_id)
    await replot_blocking_operations(image_fluo, contour_raw, image_fluo)
    return StreamingResponse(open("temp_replot.png", "rb"), media_type="image/png")












app.include_router(router_cell)

if __name__ == "__main__":
    uvicorn.run("router:app", host="0.0.0.0", port=8000, reload=True)
