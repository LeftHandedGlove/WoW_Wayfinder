import cv2
import colors
import numpy as np

current_zone_path_map = cv2.imread(r"..\images\Zone_Path_Maps\Dun_Morogh_Path_Map.png")
color_at_player_location = current_zone_path_map[423, 665]
print(color_at_player_location)
print(colors.PATH_COLOR_BGR)
if np.array_equal(color_at_player_location, colors.PATH_COLOR_BGR):
    print("On Path")
    player_on_path = True
else:
    print("Off Path")
    player_on_path = False

for row_idx, row in enumerate(current_zone_path_map):
    for col_idx, pixel in enumerate(row):
        if np.array_equal(pixel, colors.PATH_COLOR_BGR):
            current_zone_path_map[row_idx, col_idx] = [0, 0, 0]
            print(row_idx, col_idx)

cv2.imshow("converted", current_zone_path_map)
cv2.waitKey(0)
