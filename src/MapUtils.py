import CommonUtils
import os
import cv2
import colors
import ImageUtils


# TODO
def get_zone_map_from_game_image():
    zone_image = cv2.imread(CommonUtils.top_dir + os.sep + "images" + os.sep + "Raw_Zones" +
                            os.sep + "Dun_Morogh_Raw.png")
    return zone_image


def get_zone_path_map(zone):
    file_path = CommonUtils.top_dir + os.sep + "images" + os.sep + "Zone_Path_Maps" + os.sep + \
                zone.replace(" ", "_") + "_Path_Map.png"
    path_map = cv2.imread(file_path)
    return path_map


# TODO: currently does nothing
def get_current_zone():
    current_zone = "Dun Morogh"
    return current_zone


# x665,y423 is good for dun_morogh
def is_player_on_path():
    player_on_path = False
    current_zone = get_current_zone()
    current_zone_path_map = get_zone_path_map(zone=current_zone)
    player_x_perc, player_y_perc = get_player_coords()
    player_x_pix, player_y_pix = ImageUtils.percent_to_pixel(
        image=current_zone_path_map,
        coords_perc=(player_x_perc, player_y_perc))
    color_at_player_location = current_zone_path_map[player_y_pix, player_x_pix]
    if np.array_equal(color_at_player_location, colors.PATH_COLOR_BGR):
        player_on_path = True
    return player_on_path


# TODO
def get_player_coords():
    player_x = 50.0
    player_y = 50.0
    return player_x, player_y