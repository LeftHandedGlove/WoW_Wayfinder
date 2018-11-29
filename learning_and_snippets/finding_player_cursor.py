import cv2
import numpy as np
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 3

# Given a map image with a player cursor facing north extracted from a game frame,
# find the cursor with correct coords.
no_arrow_img = cv2.imread(r"..\images\test\no_arrow.png", 0)
map_north_img = cv2.imread(r"..\images\test\north_arrow.png", 0)
print(no_arrow_img.shape, map_north_img.shape)
only_arrow = cv2.subtract(no_arrow_img, map_north_img)
edges = cv2.Canny(only_arrow, 100, 200, apertureSize=3)


cv2.imshow("edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()





minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('houghlines5.jpg',img)




map_north_img_copy = map_north_img.copy()
res = cv2.matchTemplate(map_north_img_copy, cursor_img, cv2.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(map_north_img_copy, top_left, bottom_right, 255, 2)

cv2.imshow("north arrow highlighted", map_north_img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Then Given a map image with a player cursor facing in all of the cardinal directions,
# find the cursor with correct coords.


# Then a map image with the player facing north east, find the cursor, give coords, and give angle.

