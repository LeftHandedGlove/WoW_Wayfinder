import cv2
import numpy as np
from matplotlib import pyplot as plt


# Given a map image with a player cursor facing north extracted from a game frame,
# find the cursor with correct coords.
cursor_img = cv2.imread(r"..\images\test\cursor.png", 0)
map_north_img = cv2.imread(r"..\images\test\map_cursor_north.png", 0)
w, h = cursor_img.shape[::-1]

map_north_img_copy = map_north_img.copy()
res = cv2.matchTemplate(map_north_img_copy, cursor_img, cv2.TM_SQDIFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = min_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(map_north_img_copy, top_left, bottom_right, 255, 2)

cv2.imshow(map_north_img_copy)

# Then Given a map image with a player cursor facing in all of the cardinal directions,
# find the cursor with correct coords.


# Then a map image with the player facing north east, find the cursor, give coords, and give angle.

