import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

MIN_MATCH_COUNT = 3

# Given a map image with a player cursor facing north extracted from a game frame,
# find the cursor with correct coords.
no_arrow_img = cv2.imread(r"..\images\test\no_arrow.png", 0)
map_north_img = cv2.imread(r"..\images\test\east_arrow.png", 0)

only_arrow = cv2.subtract(no_arrow_img, map_north_img)
only_arrow_bgr = cv2.cvtColor(only_arrow, cv2.COLOR_GRAY2BGR)

_, arrow_thresh = cv2.threshold(only_arrow, 50, 255, cv2.THRESH_BINARY)

kernel = np.ones((5, 5), np.uint8)
closed_img = cv2.morphologyEx(arrow_thresh, cv2.MORPH_CLOSE, kernel=kernel)

_, contours, hierarchy = cv2.findContours(closed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
x, y, w, h = cv2.boundingRect(contours[0])
closed_cropped_img = closed_img[y-5:y+h+5, x-5:x+w+5]

zoomed_img = cv2.resize(closed_cropped_img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
zoomed_img_bgr = cv2.cvtColor(zoomed_img, cv2.COLOR_GRAY2BGR)
blur = cv2.GaussianBlur(zoomed_img, (5, 5), 0)

corners = cv2.goodFeaturesToTrack(zoomed_img, 4, 0.01, 10)
corners = np.int0(corners)

for i in corners:
    x, y = i.ravel()
    cv2.circle(zoomed_img_bgr, (x, y), 2, (0, 0, 255), -1)

print(corners)
x1, y1 = corners[0].ravel()
x2, y2 = corners[1].ravel()
x3, y3 = corners[2].ravel()
x4, y4 = corners[3].ravel()
len1_2 = math.sqrt(math.pow(abs(x1 - x2), 2) + math.pow(abs(y1 - y2), 2))
len1_3 = math.sqrt(math.pow(abs(x1 - x3), 2) + math.pow(abs(y1 - y3), 2))
len1_4 = math.sqrt(math.pow(abs(x1 - x4), 2) + math.pow(abs(y1 - y4), 2))
len2_3 = math.sqrt(math.pow(abs(x2 - x3), 2) + math.pow(abs(y2 - y3), 2))
len2_4 = math.sqrt(math.pow(abs(x2 - x4), 2) + math.pow(abs(y2 - y4), 2))
len3_4 = math.sqrt(math.pow(abs(x3 - x4), 2) + math.pow(abs(y3 - y4), 2))

dict_of_lens = {
    "1_2": len1_2,
    "1_3": len1_3,
    "1_4": len1_4,
    "2_3": len2_3,
    "2_4": len2_4,
    "3_4": len3_4
}
print(dict_of_lens)

long, short = 0, 1000
long_name, short_name = "", ""
for name, length in dict_of_lens.items():
    if length > long:
        long = length
        long_name = name
    elif length < short:
        short = length
        short_name = name

for i in range(1, 5):
    if str(i) in long_name and str(i)in short_name:
        rear_point = i - 1
        front_point = long_name.replace(str(i), "")
        front_point = front_point.replace("_", "")
        front_point = int(front_point) - 1

side_points = list()
for i in range(0, 4):
    if i != front_point and i != rear_point:
        side_points.append(i)


front_x, front_y = corners[front_point].ravel()
side0_x, side0_y = corners[side_points[0]].ravel()
side1_x, side1_y = corners[side_points[1]].ravel()
side_x_avg = int(round((side0_x + side1_x) / 2))
side_y_avg = int(round((side0_y + side1_y) / 2))

cv2.line(zoomed_img_bgr, (front_x,front_y), (side0_x, side0_y), (255, 0, 0), 1)
cv2.line(zoomed_img_bgr, (front_x,front_y), (side1_x, side1_y), (255, 0, 0), 1)
cv2.line(zoomed_img_bgr, (front_x,front_y), (side_x_avg, side_y_avg), (0, 255, 0), 1)

print(side_x_avg - front_x, front_y - side_y_avg)

angle = math.atan((front_y - side_y_avg) / (side_x_avg - front_x))
print(math.degrees(angle) - 90 + 180)

zoomed_img_bgr = cv2.resize(zoomed_img_bgr, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)

cv2.imshow("zoomed_img_bgr",zoomed_img_bgr)

cv2.waitKey(0)
cv2.destroyAllWindows()
exit(0)




zooms = 3
zoomed_img = closed_cropped_img.copy()
blured_zoom = closed_cropped_img.copy()
for i in range(0, zooms+1):

    blured_zoom = cv2.GaussianBlur(zoomed_img, (3, 3), 0)
_, large_blur_thresh = cv2.threshold(zoomed_img, 240, 255, cv2.THRESH_BINARY)
cv2.imshow("large_blur_thresh", large_blur_thresh)

large_blur_thresh_bgr = cv2.cvtColor(large_blur_thresh, cv2.COLOR_GRAY2BGR)

#large_blur_thresh = np.float32(large_blur_thresh)
#dst = cv2.cornerHarris(large_blur_thresh, 5, 25, 0.03)
#kernel = np.ones((3, 3), np.uint8)
#dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel=kernel)
#cv2.imshow("dst", dst)

corners = cv2.goodFeaturesToTrack(large_blur_thresh, 3, 0.01, 10)
corners = np.int0(corners)

for i in corners:
    x, y = i.ravel()
    cv2.circle(large_blur_thresh_bgr, (x, y), 3, 255, -1)

cv2.imshow("large_blur_thresh_bgr", large_blur_thresh_bgr)



cv2.waitKey(0)
cv2.destroyAllWindows()
exit(0)

edges = cv2.Canny(closed_img, 50, 150)

cv2.imwrite("edges.png", edges)

minLineLength = 10
maxLineGap = 5
lines = cv2.HoughLinesP(closed_img, 1, np.pi/180, 10, minLineLength, maxLineGap)

print(lines)

# find the two longest lines
good_lines = [0, 0]
first_longest_line_len, second_longest_line_len = 0, 0
for line in lines:
    for x1, y1, x2, y2 in line:
        line_len = math.sqrt(math.pow(abs(x2 - x1), 2) + math.pow(abs(y2 - y1), 2))
        if line_len > first_longest_line_len:
            second_longest_line_len = first_longest_line_len
            first_longest_line_len = line_len
            good_lines[1] = good_lines[0]
            good_lines[0] = line
        elif line_len > second_longest_line_len:
            second_longest_line_len = line_len
            good_lines[1] = line

print(good_lines)

for line in good_lines:
    for x1, y1, x2, y2 in line:
        cv2.line(only_arrow_bgr, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow('only_arrow', only_arrow)
cv2.imshow("arrow_thresh", arrow_thresh)
cv2.imshow("closed_img", closed_img)
cv2.imshow("edges", edges)
cv2.imshow('houghlines5', only_arrow_bgr)

cv2.waitKey(0)
cv2.destroyAllWindows()
exit(0)

'''

closed_img = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel=kernel)
closed_img_bgr = cv2.cvtColor(closed_img, cv2.COLOR_GRAY2BGR)

edges = cv2.Canny(closed_img, 50, 200, apertureSize=3)

blur = cv2.GaussianBlur(edges, (3, 3), 0)

_, blur_thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

blur_bgr = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)

edges = cv2.Canny(blur_thresh, 50, 200, apertureSize=3)
'''



cv2.imshow("edges", edges)
edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

kernel = np.ones((5, 5), np.uint8)
closed_img = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel=kernel)

edges = cv2.Canny(closed_img, 50, 200)

cv2.imshow("edges", edges)

cv2.imshow("closed_img", closed_img)

minLineLength = 2
maxLineGap = 5
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 8, minLineLength, maxLineGap)

print(lines)

# find the two longest lines
good_lines = [0, 0]
first_longest_line_len, second_longest_line_len = 0, 0
for line in lines:
    for x1, y1, x2, y2 in line:
        line_len = math.sqrt(math.pow(abs(x2 - x1), 2) + math.pow(abs(y2 - y1), 2))
        if line_len > first_longest_line_len:
            second_longest_line_len = first_longest_line_len
            first_longest_line_len = line_len
            good_lines[1] = good_lines[0]
            good_lines[0] = line
        elif line_len > second_longest_line_len:
            second_longest_line_len = line_len
            good_lines[1] = line

print(good_lines)
'''
# fix the lines so the point of the arrow is the starting point of both lines
x1_1, y1_1, x2_1, y2_1 = 0, 0, 0, 0
x1_2, y1_2, x2_2, y2_2 = 0, 0, 0, 0
for x1, y1, x2, y2 in good_lines[0]:
    x1_1, y1_1, x2_1, y2_1 = x1, y1, x2, y2
for x1, y1, x2, y2 in good_lines[1]:
    x1_2, y1_2, x2_2, y2_2 = x1, y1, x2, y2

x1_to_x1_diff = abs(x1_1 - x1_2)
x1_to_x2_diff = abs(x1_1 - x2_2)
x2_to_x1_diff = abs(x2_1 - x1_2)
x2_to_x2_diff = abs(x2_1 - x2_2)
y1_to_y1_diff = abs(y1_1 - y1_2)
y1_to_y2_diff = abs(y1_1 - y2_2)
y2_to_y1_diff = abs(y2_1 - y1_2)
y2_to_y2_diff = abs(y2_1 - y2_2)

xy1_to_xy1 = x1_to_x1_diff + y1_to_y1_diff
xy1_to_xy2 = x1_to_x2_diff + y1_to_y2_diff
xy2_to_xy1 = x2_to_x1_diff + y2_to_y1_diff
xy2_to_xy2 = x1_to_x2_diff + y2_to_y2_diff

list_of_points_diffs = [xy1_to_xy1, xy1_to_xy2, xy2_to_xy1, xy2_to_xy2]
list_of_points_diffs.sort()

if xy1_to_xy1 == list_of_points_diffs[0]:
    pass
elif xy1_to_xy2 == list_of_points_diffs[0]:
    good_lines[1] = np.array([[x2_2, y2_2, x1_2, y1_2]])
elif xy2_to_xy1 == list_of_points_diffs[0]:
    good_lines[0] = np.array([[x2_1, y2_1, x1_1, y1_1]])
elif xy2_to_xy2 == list_of_points_diffs[0]:
    pass

print(good_lines)

'''

for line in lines:
    for x1, y1, x2, y2 in line:
        '''
        line_len = math.sqrt(math.pow(abs(x2 - x1), 2) + math.pow(abs(y2 - y1), 2))
        if line_len < minLineLength:
            continue
        '''
        cv2.line(edges_bgr, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow('houghlines5', edges_bgr)



'''

# get the slope of the lines
slopes = [0, 0]
for idx, line in enumerate(good_lines):
    for x1, y1, x2, y2 in line:
        slopes[idx] = (y2 - y1) / (x2 - x1)
avg_slope = (slopes[0] + slopes[1]) / 2
print(good_lines)
print(slopes[0], slopes[1], avg_slope)

top = slopes[1] - slopes[0]
bot = 1 - (slopes[0] * slopes[1])
angle_between_lines = math.atan(top/bot)
print(math.degrees(angle_between_lines) - 90)

# average those slopes, that is the angle the player is facing
# convert the slope to degrees from north, that is the angle the player is facing

'''





# Then Given a map image with a player cursor facing in all of the cardinal directions,
# find the cursor with correct coords.


# Then a map image with the player facing north east, find the cursor, give coords, and give angle.

