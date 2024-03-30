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
from fastapi.responses import StreamingResponse
import aiofiles
import pickle
import matplotlib.pyplot as plt
from functions import draw_scale_bar_with_centered_text, basis_conversion
from fastapi.params import Query
from numpy.linalg import inv


app = FastAPI(docs_url="/docs")
router_cell = APIRouter(prefix="/cellapi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Point:
    def __init__(self, u1: float, G: float):
        self.u1 = u1
        self.G = G

    def __gt__(self, other):
        return self.u1 > other.u1
    
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
    cell: bytes = await get_cell_fluo(f"./databases/{db_name}.db", cell_id)
    image_fluo = cv2.imdecode(np.frombuffer(cell, dtype=np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image_fluo, cv2.COLOR_BGR2GRAY)
    contour_raw = await get_cell_contour(f"./databases/{db_name}.db", cell_id)
    contour = [
                        [j, i] for i, j in [i[0] for i in pickle.loads(contour_raw)]
                    ]
    coords_inside_cell_1, points_inside_cell_1, projected_points = [], [],[]
    for i in range(image_fluo.shape[1]):
        for j in range(image_fluo.shape[0]):
            if (
                cv2.pointPolygonTest(
                    pickle.loads(contour_raw), (i, j), False
                )
                >= 0
            ):
                coords_inside_cell_1.append([i, j])
                points_inside_cell_1.append(gray[j][i])
    X = np.array(
                        [
                            [i[1] for i in coords_inside_cell_1],
                            [i[0] for i in coords_inside_cell_1],
                        ]
                    )
    (
                        u1,
                        u2,
                        u1_contour,
                        u2_contour,
                        min_u1,
                        max_u1,
                        u1_c,
                        u2_c,
                        U,
                        contour_U,
                    ) = basis_conversion(
                        contour, X, image_fluo.shape[0]//2, image_fluo.shape[1]//2, coords_inside_cell_1
                    )   
    min_u1, max_u1 = min(u1), max(u1)
    fig = plt.figure(figsize=[6, 6])
    cmap = plt.get_cmap("inferno")
    x = np.linspace(0, 100, 1000)
    max_points = max(points_inside_cell_1)
    plt.scatter(
        u1,
        u2,
        c=[i / max_points for i in points_inside_cell_1],
        s=10,
        cmap=cmap,
    )
    # plt.scatter(u1_contour, u2_contour, s=10, color="lime")
    plt.grid()
    W = np.array([[i**4, i**3, i**2, i, 1] for i in [i[1] for i in U]])
    print(W)
    f = np.array([i[0] for i in U])
    theta = inv(W.transpose() @ W) @ W.transpose() @ f
    print(theta)
    x = np.linspace(min_u1, max_u1, 1000)
    y = [
        theta[0] * i**4
        + theta[1] * i**3
        + theta[2] * i**2
        + theta[3] * i
        + theta[4]
        for i in x
    ]
    plt.plot(x, y, color="blue", linewidth=1)
    plt.scatter(
        min_u1,
        theta[0] * min_u1**4
        + theta[1] * min_u1**3
        + theta[2] * min_u1**2
        + theta[3] * min_u1
        + theta[4],
        s=100,
        color="red",
        zorder=100,
        marker="x",
    )
    plt.scatter(
        max_u1,
        theta[0] * max_u1**4
        + theta[1] * max_u1**3
        + theta[2] * max_u1**2
        + theta[3] * max_u1
        + theta[4],
        s=100,
        color="red",
        zorder=100,
        marker="x",
    )

    plt.xlabel("u1")
    plt.ylabel("u2")
    plt.axis("equal")
    plt.xlim(min_u1 - 80, max_u1 + 80)
    plt.ylim(u2_c - 80, u2_c + 80)

    # Y軸の範囲を取得
    ymin, ymax = plt.ylim()
    y_pos = ymin + 0.2 * (ymax - ymin)
    y_pos_text = ymax - 0.15 * (ymax - ymin)
    plt.text(
        u1_c,
        y_pos_text,
        s=f"",
        color="red",
        ha="center",
        va="top",
    )
    for u, g in zip(u1, points_inside_cell_1):
        point = Point(u, g)
        projected_points.append(point)
    sorted_projected_points = sorted(projected_points)
    # add second axis
    ax2 = plt.twinx()
    ax2.grid(False)
    ax2.set_xlabel("u1")
    ax2.set_ylabel("Brightness")
    ax2.set_ylim(0, 900)
    ax2.set_xlim(min_u1 - 40, max_u1 + 40)
    ax2.scatter(
        [i.u1 for i in sorted_projected_points],
        [i.G for i in sorted_projected_points],
        color="lime",
        s=1,
    )
    fig.savefig(f"temp_replot.png")
    plt.close()
    return StreamingResponse(open("temp_replot.png", "rb"), media_type="image/png")











app.include_router(router_cell)

if __name__ == "__main__":
    uvicorn.run("router:app", host="0.0.0.0", port=8000, reload=True)
