import cv2
import os
import numpy as np
import colors

top_dir = os.getcwd()
top_dir = top_dir[:top_dir.find("WoW_Wayfinder")+len("WoW_Wayfinder")+1]


# TODO
def get_player_coords():
    player_x = 50.0
    player_y = 50.0
    return player_x, player_y


def is_player_on_path():
    player_on_path = False
    current_zone = get_current_zone()
    current_zone_path_map = get_zone_path_map(zone=current_zone)
    player_x_perc, player_y_perc = get_player_coords()
    player_x_pix, player_y_pix = percent_to_pixel(
        image=current_zone_path_map,
        coords_perc=(player_x_perc, player_y_perc))
    color_at_player_location = current_zone_path_map[player_x_pix, player_y_pix]
    if color_at_player_location == colors.PATH_COLOR_BGR:
        player_on_path = True
    return player_on_path


# TODO: currently does nothing
def get_current_zone():
    current_zone = "Dun Morogh"
    return current_zone


def get_zone_path_map(zone):
    file_path = top_dir + os.sep + "images" + os.sep + "Zone_Path_Maps" + os.sep + \
                zone.replace(" ", "_") + "_Path_Map.png"
    path_map = cv2.imread(file_path)
    return path_map


# TODO: current does nothing
def percent_to_pixel(image, coords_perc):
    x_pix, y_pix = coords_perc
    return x_pix, y_pix


# TODO: make this work with multiple channels
def average_color_of_image_BGR(image):
    average_color_per_row = np.average(image, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    average_color = int(round(average_color))
    return average_color
