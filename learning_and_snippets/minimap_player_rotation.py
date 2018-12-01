import cv2
import numpy as np
import math


cap = cv2.VideoCapture(r"..\images\test\moving_minimap_arrow_dun_morogh.mp4")

if cap.isOpened() == False:
    print("Error opening video")

wait_15_fps = int(1000/20)

fourcc = cv2.VideoWriter_fourcc("D", "I", "V", "X")
video_out = cv2.VideoWriter("output.avi", fourcc, 15.0, (210, 180))

while cap.isOpened():
    # Read the frame
    ret, frame = cap.read()

    if ret:

        # crop the image for the arrow
        arrow_crop_frame = frame[100:130, 1795:1830]


        # Increase the size a ton
        sizer = 6
        enlarged_arrow_frame = cv2.resize(arrow_crop_frame, None, fx=sizer, fy=sizer)
        marked_frame = enlarged_arrow_frame.copy()
        print(marked_frame.shape)

        # Convert the frame to grey
        grey_frame = cv2.cvtColor(enlarged_arrow_frame, cv2.COLOR_BGR2GRAY)

        # Blur the image
        kernel_size = 21
        blured_frame = cv2.GaussianBlur(grey_frame, (kernel_size, kernel_size), 0)

        # Apply a histogram
        hist, bins = np.histogram(blured_frame.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype("uint8")
        hist_frame = cdf[blured_frame]

        # bitwise not to bring out the circle
        not_hist_frame = cv2.bitwise_not(hist_frame)

        # Now apply some thresholding, the arrow will always be bright so we can assume it will be white after histogram
        _, hist_thresh_frame = cv2.threshold(not_hist_frame, 251, 255, cv2.THRESH_BINARY)

        # now open it
        kernel = np.ones((9, 9), np.uint8)
        opened_frame = cv2.morphologyEx(hist_thresh_frame, cv2.MORPH_OPEN, kernel=kernel)

        # Mark the pivot of the arrow
        h, w, _ = marked_frame.shape
        arrow_pivot_x = int(round(w / 2)) - 5
        arrow_pivot_y = int(round(h / 2)) - 5
        cv2.circle(marked_frame, (arrow_pivot_x, arrow_pivot_y), 10, (255, 0, 0), -1)

        try:
            # Mark the circle and find its center point
            circles = cv2.HoughCircles(opened_frame, cv2.HOUGH_GRADIENT, 1, 20,
                                       param1=50, param2=10, minRadius=10, maxRadius=0)
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(marked_frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(marked_frame, (i[0], i[1]), 2, (0, 0, 255), 3)
        except:
            pass

        # draw a line through the pivot point starting at the center of the circle
        cen_x, cen_y, rad = circles.ravel()
        new_x = cen_x + (5 * (arrow_pivot_x - cen_x))
        new_y = cen_y + (5 * (arrow_pivot_y - cen_y))
        cv2.line(marked_frame, (cen_x, cen_y), (new_x, new_y), (0, 0, 255), 2)

        north_vector = (0, arrow_pivot_y)
        arrow_vector = (arrow_pivot_x - cen_x, cen_y - arrow_pivot_y)
        # magnitudes
        north_vector_magnitude = math.sqrt(math.pow(north_vector[0], 2) + math.pow(north_vector[1], 2))
        arrow_vector_magnitude = math.sqrt(math.pow(arrow_vector[0], 2) + math.pow(arrow_vector[1], 2))
        # dot product
        dot_prod = (north_vector[0] * arrow_vector[0]) + (north_vector[1] * arrow_vector[1])
        # cos(theta) = dot_prod / (mag_a * mag_b)
        angle = math.acos(dot_prod / (north_vector_magnitude * arrow_vector_magnitude))
        angle = math.degrees(angle)
        # Handle the extra angle so that we use all 360 degrees
        if cen_x < arrow_pivot_x:
            angle = 360 - angle
        print(angle)

        # Show some stuff
        cv2.imshow("enlarged_arrow_frame", enlarged_arrow_frame)
        cv2.imshow("grey_frame", grey_frame)
        cv2.imshow("blured_frame", blured_frame)
        cv2.imshow("hist_frame", hist_frame)
        cv2.imshow("not_hist_frame", not_hist_frame)
        cv2.imshow("hist_thresh_frame", hist_thresh_frame)
        cv2.imshow("opened_frame", opened_frame)
        cv2.imshow("marked_frame", marked_frame)

        # Save things to video for later
        video_out.write(marked_frame)

        if cv2.waitKey(wait_15_fps) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
video_out.release()
cv2.destroyAllWindows()
exit(0)












# Read in the full screen image as greyscale
raw_img = cv2.imread(r"..\images\test\minimap_fullscreen_north.png", 0)

# Crop it so we get the arrow
grey_arrow_crop_img = raw_img[100:125, 1800:1825]

# try enlarging and bluring it
enlarged_crop = cv2.resize(grey_arrow_crop_img, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
blured_enlarge = cv2.GaussianBlur(enlarged_crop, (11, 11), 0)

# Attempt to apply histogram equalization
hist, bins = np.histogram(blured_enlarge.flatten(), 256, [0, 256])
cdf = hist.cumsum()
cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
cdf = np.ma.filled(cdf_m, 0).astype("uint8")
hist_img = cdf[blured_enlarge]

# Now apply some thresholding, the arrow will always be bright so we can assume it will be white after histogram
_, hist_thresh_img = cv2.threshold(hist_img, 230, 255, cv2.THRESH_BINARY)

# try bluring it again
blured_hist = cv2.GaussianBlur(hist_thresh_img, (21, 21), 0)

# try thresholding it again
_, blur_thresh_img = cv2.threshold(blured_hist, 100, 255, cv2.THRESH_BINARY)

# Now find the important parts
marked_img = cv2.cvtColor(blur_thresh_img, cv2.COLOR_GRAY2BGR)
corners = cv2.goodFeaturesToTrack(blur_thresh_img, 3, 0.01, 10)
corners = np.int0(corners)
for i in corners:
    x, y = i.ravel()
    cv2.circle(marked_img, (x, y), 2, (0, 0, 255), -1)

# draw some lines
x0, y0 = corners[0].ravel()
x1, y1 = corners[1].ravel()
x2, y2 = corners[2].ravel()
cv2.line(marked_img, (x0, y0), (x1, y1), (255, 0, 0), 3)
cv2.line(marked_img, (x1, y1), (x2, y2), (255, 0, 0), 3)
cv2.line(marked_img, (x2, y2), (x0, y0), (255, 0, 0), 3)

# Find the 2 longest lines
len_0_1 = math.sqrt(math.pow(abs(x0 - x1), 2) + math.pow(abs(y0 - y1), 2))
len_0_2 = math.sqrt(math.pow(abs(x0 - x2), 2) + math.pow(abs(y0 - y2), 2))
len_1_2 = math.sqrt(math.pow(abs(x1 - x2), 2) + math.pow(abs(y1 - y2), 2))

print(corners)
print(len_0_1, len_0_2, len_1_2)


# Display everything
cv2.imshow("grey_arrow_crop_img", grey_arrow_crop_img)
cv2.imshow("hist_img", hist_img)
cv2.imshow("hist_thresh_img", hist_thresh_img)
cv2.imshow("enlarged_crop", enlarged_crop)
cv2.imshow("blured_hist", blured_hist)
cv2.imshow("blur_thresh_img", blur_thresh_img)
cv2.imshow("marked_img", marked_img)


cv2.waitKey(0)
cv2.destroyAllWindows()
exit(0)

