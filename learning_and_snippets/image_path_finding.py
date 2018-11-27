import cv2
import mss
from matplotlib import pyplot as plt
import numpy as np

def get_abs_point_from_percent(image, percent_x, percent_y):
    abs_height, abs_width = image.shape
    point_x = int((abs_width * percent_x) / 100)
    point_y = int((abs_height * percent_y) / 100)
    return [point_x, point_y]

# Get the raw image and make it smaller
raw_img = cv2.imread(r"..\images\test\dun_morogh_third_person_near.png")
raw_img = cv2.resize(raw_img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

# Convert it to greyscale
grey_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)

# Attempt to apply histogram equalization
hist, bins = np.histogram(grey_img.flatten(), 256, [0, 256])
cdf = hist.cumsum()
cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
cdf = np.ma.filled(cdf_m, 0).astype("uint8")
grey_img2 = cdf[grey_img]

# Try thresholding the image with the average of the road
left = get_abs_point_from_percent(grey_img2, 30, 40)[0]
top = get_abs_point_from_percent(grey_img2, 30, 40)[1]
right = get_abs_point_from_percent(grey_img2, 70, 100)[0]
bottom = get_abs_point_from_percent(grey_img2, 70, 100)[1]
smaller_img = grey_img2[top:bottom, left:right]
avg_color_per_row = np.average(smaller_img, axis=0)
avg_color = np.average(avg_color_per_row, axis=0)
avg_path_color = int(round(avg_color))

# Get the average color of outside the path
left = get_abs_point_from_percent(grey_img2, 0, 40)[0]
top = get_abs_point_from_percent(grey_img2, 0, 40)[1]
right = get_abs_point_from_percent(grey_img2, 20, 60)[0]
bottom = get_abs_point_from_percent(grey_img2, 20, 60)[1]
smaller_img_outside_left = grey_img2[top:bottom, left:right]
avg_color_per_row = np.average(smaller_img_outside_left, axis=0)
avg_color = np.average(avg_color_per_row, axis=0)
avg_outside_left_color = int(round(avg_color))

left = get_abs_point_from_percent(grey_img2, 80, 40)[0]
top = get_abs_point_from_percent(grey_img2, 80, 40)[1]
right = get_abs_point_from_percent(grey_img2, 100, 60)[0]
bottom = get_abs_point_from_percent(grey_img2, 100, 60)[1]
smaller_img_outside_right = grey_img2[top:bottom, left:right]
avg_color_per_row = np.average(smaller_img_outside_right, axis=0)
avg_color = np.average(avg_color_per_row, axis=0)
avg_outside_right_color = int(round(avg_color))
avg_outside_color = int((avg_outside_left_color + avg_outside_right_color) / 2)

if avg_path_color < avg_outside_color:
    half_diff = int((avg_outside_color - avg_path_color) / 2)
    avg_color_high = np.array([avg_path_color + half_diff])
    avg_color_low = np.array([0])
else:
    half_diff = int((avg_path_color - avg_outside_color) / 2)
    avg_color_high = np.array([255])
    avg_color_low = np.array([avg_path_color + half_diff])

path_avg_mask = cv2.inRange(grey_img2, avg_color_low, avg_color_high)

# Try closing the path mask
kernel = np.ones((5,5),np.uint8)
closed_path = cv2.morphologyEx(path_avg_mask, cv2.MORPH_CLOSE, kernel=kernel)

# Get the region of interest


# Now apply some bluring
kernel_size = 101
blur = cv2.GaussianBlur(closed_path, (kernel_size, kernel_size), 0)

# Redo the threshold
_, thresh_2_img = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

points = np.array([get_abs_point_from_percent(grey_img2, 0, 75),
                   get_abs_point_from_percent(grey_img2, 25, 25),
                   get_abs_point_from_percent(grey_img2, 75, 25),
                   get_abs_point_from_percent(grey_img2, 100, 75)],
                  np.int32)
mask = np.zeros_like(thresh_2_img)
cv2.fillPoly(mask, [points], 255)
roi_img = cv2.bitwise_and(thresh_2_img, mask)

# Apply edge detection
edges = cv2.Canny(roi_img, 100, 100)

# Show the images
cv2.imshow("raw_img", raw_img)
cv2.imshow("grey", grey_img)
cv2.imshow("grey_2", grey_img2)
cv2.imshow("roi_img", roi_img)
cv2.imshow("smaller_img", smaller_img)
cv2.imshow("smaller_img_outside_left", smaller_img_outside_left)
cv2.imshow("smaller_img_outside_right", smaller_img_outside_right)
cv2.imshow("edges", edges)
cv2.imshow("path_avg_mask", path_avg_mask)
cv2.imshow("closed_path", closed_path)
cv2.imshow("blur", blur)
cv2.imshow("thresh_2_img", thresh_2_img)

# Pause to see the windows
cv2.waitKey(0)
cv2.destroyAllWindows()


