import numpy as np


def percent_to_pixel(image, coords_perc):
    if len(image.shape) == 3:
        height_pix, width_pix, _ = image.shape
    elif len(image.shape) == 2:
        height_pix, width_pix = image.shape
    else:
        raise Exception("Unsupported image type.")
    x_pix = (width_pix * coords_perc) / 100
    y_pix = (height_pix * coords_perc) / 100
    return x_pix, y_pix


# TODO: make this work with multiple channels
def average_color_of_image_bgr(image):
    average_color_per_row = np.average(image, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    average_color = int(round(average_color))
    return average_color


def average_color_of_image_grey(image):
    average_color_per_row = np.average(image, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    average_color = int(round(average_color))
    return average_color
