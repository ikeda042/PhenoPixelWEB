import cv2
import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt
import pickle
from numpy.linalg import inv
from concurrent.futures import ThreadPoolExecutor
import asyncio
from schemas import BasicCellInfo, CellStats, CellDBAll
from database import get_cell_all

executor = ThreadPoolExecutor(max_workers=1)

async def save_fig_async(fig, filename):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, fig.savefig, filename)
    plt.close(fig)

async def draw_scale_bar_with_centered_text(image_ph):
    """
    Draws a 5 um white scale bar on the lower right corner of the image with "5 um" text centered under it.
    Assumes 1 pixel = 0.0625 um.
    
    Parameters:
    - image_ph: Input image on which the scale bar and text will be drawn.
    
    Returns:
    - Modified image with the scale bar and text.
    """
    # Conversion factor and scale bar desired length
    pixels_per_um = 1 / 0.0625  # pixels per micrometer
    scale_bar_um = 5  # scale bar length in micrometers

    # Calculate the scale bar length in pixels
    scale_bar_length_px = int(scale_bar_um * pixels_per_um)

    # Define the scale bar thickness and color
    scale_bar_thickness = 2  # in pixels
    scale_bar_color = (255, 255, 255)  # white for the scale bar

    # Determine the position for the scale bar (lower right corner)
    margin = 20  # margin from the edges in pixels, increased for text space
    x1 = image_ph.shape[1] - margin - scale_bar_length_px
    y1 = image_ph.shape[0] - margin
    x2 = x1 + scale_bar_length_px
    y2 = y1 + scale_bar_thickness

    # Draw the scale bar
    cv2.rectangle(image_ph, (x1, y1), (x2, y2), scale_bar_color, thickness=cv2.FILLED)

    # Add text "5 um" under the scale bar
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "5 um"
    text_scale = 0.4  # font scale
    text_thickness = 1  # font thickness
    text_color = (255, 255, 255)  # white for the text

    # Calculate text size to position it
    text_size = cv2.getTextSize(text, font, text_scale, text_thickness)[0]
    # Calculate the starting x-coordinate of the text to center it under the scale bar
    text_x = x1 + (scale_bar_length_px - text_size[0]) // 2
    text_y = y2 + text_size[1] + 5  # a little space below the scale bar

    # Draw the text
    cv2.putText(image_ph, text, (text_x, text_y), font, text_scale, text_color, text_thickness)

    return image_ph

def basis_conversion(contour:list[list[int]],X:np.ndarray,center_x:float,center_y:float,coordinates_incide_cell:list[list[int]]) -> list[list[float]]:
    Sigma = np.cov(X)
    eigenvalues, eigenvectors = eig(Sigma)
    if eigenvalues[1] < eigenvalues[0]:
        m = eigenvectors[1][1]/eigenvectors[1][0]
        Q = np.array([eigenvectors[1],eigenvectors[0]])
        U = [Q.transpose()@np.array([i,j]) for i,j in coordinates_incide_cell]
        U = [[j,i] for i,j in U]
        contour_U = [Q.transpose()@np.array([j,i]) for i,j in contour]
        contour_U = [[j,i] for i,j in contour_U]
        color = "red"
        center = [center_x, center_y]
        u1_c, u2_c = center@Q
    else:
        m = eigenvectors[0][1]/eigenvectors[0][0]
        Q = np.array([eigenvectors[0],eigenvectors[1]])
        U = [Q.transpose()@np.array([j,i]).transpose() for i,j in coordinates_incide_cell]
        contour_U = [Q.transpose()@np.array([i,j]) for i,j in contour]
        color = "blue"
        center = [center_x,
                  center_y]
        u2_c, u1_c = center@Q
    
    u1 = [i[1] for i in U]
    u2 = [i[0] for i in U]
    u1_contour = [i[1] for i in contour_U]
    u2_contour = [i[0] for i in contour_U]
    min_u1, max_u1 = min(u1), max(u1)
    return u1,u2,u1_contour,u2_contour,min_u1,max_u1,u1_c,u2_c, U, contour_U




async def get_cell_stats(dbname:str, cell_id: str, include_ph: bool = False) -> CellStats:
    cell : CellDBAll = await get_cell_all(dbname, cell_id)
    image_ph = cv2.imdecode(np.frombuffer(cell.img_ph, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_fluo =  cv2.imdecode(np.frombuffer(cell.img_fluo1, dtype=np.uint8), cv2.IMREAD_COLOR)
    contour_raw = cell.contour
    gray = cv2.cvtColor(image_fluo, cv2.COLOR_BGR2GRAY)

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
    max_brightness = max(points_inside_cell_1)
    min_brightness = min(points_inside_cell_1)
    W = np.array([[i**4, i**3, i**2, i, 1] for i in [i[1] for i in U]])
    f = np.array([i[0] for i in U])
    theta = inv(W.transpose() @ W) @ W.transpose() @ f
    x = np.linspace(min_u1, max_u1, 1000)
    y = [
        theta[0] * i**4
        + theta[1] * i**3
        + theta[2] * i**2
        + theta[3] * i
        + theta[4]
        for i in x
    ]
    mean_brightness_raw = round(np.mean(points_inside_cell_1),2)
    mean_brightness_normalized = round(np.mean([i / max_brightness for i in points_inside_cell_1]),2)
    median_brightness_raw = round(np.median(points_inside_cell_1),2)
    median_brightness_normalized = round( np.median([i / max_brightness for i in points_inside_cell_1]),2)
    if include_ph:
        image_ph = cv2.cvtColor(image_ph, cv2.COLOR_BGR2GRAY)
        coords_inside_cell_1_ph, points_inside_cell_1_ph = [], []
        for i in range(image_ph.shape[1]):
            for j in range(image_ph.shape[0]):
                if (
                    cv2.pointPolygonTest(
                        pickle.loads(contour_raw), (i, j), False
                    )
                    >= 0
                ):
                    coords_inside_cell_1_ph.append([i, j])
                    points_inside_cell_1_ph.append(image_ph[j][i])
        ph_max_brightness = max(points_inside_cell_1_ph)
        ph_min_brightness = min(points_inside_cell_1_ph)
        ph_mean_brightness_raw = round(np.mean(points_inside_cell_1_ph),2)
        ph_mean_brightness_normalized = round(np.mean([i / ph_max_brightness for i in points_inside_cell_1_ph]),2)
        ph_median_brightness_raw = round(np.median(points_inside_cell_1_ph),2)
        ph_median_brightness_normalized = round( np.median([i / ph_max_brightness for i in points_inside_cell_1_ph]),2)
        return CellStats(basic_cell_info=BasicCellInfo(
            cell_id=cell.cell_id,
            label_experiment=cell.label_experiment,
            manual_label=cell.manual_label,
            perimeter=round(cell.perimeter,2),
            area=cell.area
        ),ph_max_brightness=ph_max_brightness,ph_min_brightness=ph_min_brightness,ph_mean_brightness_raw=ph_mean_brightness_raw,ph_mean_brightness_normalized=ph_mean_brightness_normalized,ph_median_brightness_raw=ph_median_brightness_raw,ph_median_brightness_normalized=ph_median_brightness_normalized,max_brightness=max_brightness,min_brightness=min_brightness,mean_brightness_raw=mean_brightness_raw,mean_brightness_normalized=mean_brightness_normalized,median_brightness_raw=median_brightness_raw,median_brightness_normalized=median_brightness_normalized)
    return CellStats(basic_cell_info=BasicCellInfo(
        cell_id=cell.cell_id,
        label_experiment=cell.label_experiment,
        manual_label=cell.manual_label,
        perimeter=round(cell.perimeter,2),
        area=cell.area
    ),max_brightness=max_brightness,min_brightness=min_brightness,mean_brightness_raw=mean_brightness_raw,mean_brightness_normalized=mean_brightness_normalized,median_brightness_raw=median_brightness_raw,median_brightness_normalized=median_brightness_normalized)

async def replot_blocking_operations(image_fluo, contour_raw, gray):
    class Point:
        def __init__(self, u1: float, G: float):
            self.u1 = u1
            self.G = G

        def __gt__(self, other):
            return self.u1 > other.u1
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
    W = np.array([[i**4, i**3, i**2, i, 1] for i in [i[1] for i in U]])
    f = np.array([i[0] for i in U])
    theta = inv(W.transpose() @ W) @ W.transpose() @ f
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
    await save_fig_async(fig, "temp_replot.png")
    plt.close()
