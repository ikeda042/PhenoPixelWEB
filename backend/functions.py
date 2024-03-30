import cv2
import numpy as np
from numpy.linalg import eig

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
