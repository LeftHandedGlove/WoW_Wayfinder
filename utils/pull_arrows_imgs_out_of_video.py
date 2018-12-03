import cv2
import numpy as np
import math
import os
import shutil


direction_frames_dict = {
    "N": 14,
    "NNE": 63,
    "NE": 137,
    "ENE": None,
    "E": 244,
    "ESE": None,
    "SE": None,
    "SSE": None,
    "S": None,
    "SSW": None,
    "SW": None,
    "WSW": None,
    "W": None,
    "WNW": None,
    "NW": None,
    "NNW": None,
}

shutil.rmtree(r"arrow_test_images")
os.mkdir(r"arrow_test_images")
os.mkdir(r"arrow_test_images\useful_frames")
os.mkdir(r"arrow_test_images\all_frames")
os.mkdir(r"arrow_test_images\boundary_frames")

frame_cnt = 0
cap = cv2.VideoCapture(r"..\images\raw_arrows_dun_morogh.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # crop the image for the arrow
        arrow_crop_frame = frame[100:130, 1795:1830]

        if frame_cnt == 0:
            prev_frame = cv2.bitwise_not(arrow_crop_frame)

        # if the image is the same then remove it
        diff = cv2.subtract(arrow_crop_frame, prev_frame)
        b, g, r = cv2.split(diff)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            continue
        else:
            prev_frame = arrow_crop_frame

        # save the image
        file_name = r"arrow_test_images\all_frames\arrow_num_" + str(frame_cnt) + ".png"
        cv2.imwrite(file_name, arrow_crop_frame)

        frame_cnt += 1
    else:
        break

cap.release()

start_frame_boundary = 0
end_frame_boundary = 1000
one_none_flag = False
for direction, frame_num in direction_frames_dict.items():
    if frame_num is not None:
        if start_frame_boundary != 0:
            end_frame_boundary = frame_num
            if one_none_flag:
                break
        else:
            start_frame_boundary = frame_num
            end_frame_boundary = frame_num + 1000
    else:
        one_none_flag = True

for frame_num in range(start_frame_boundary, end_frame_boundary):
    src = r"arrow_test_images\all_frames\arrow_num_" + str(frame_num) + ".png"
    dest = r"arrow_test_images\boundary_frames"
    shutil.copy(src=src, dst=dest)

for frame_num in range(0, frame_cnt):
    for direction, specific_frame_num in direction_frames_dict.items():
        if frame_num == specific_frame_num:
            src = r"arrow_test_images\all_frames\arrow_num_" + str(frame_num) + ".png"
            dest = r"arrow_test_images\useful_frames"
            shutil.copy(src=src, dst=dest)
            src = r"arrow_test_images\useful_frames\arrow_num_" + str(frame_num) + ".png"
            dest = r"arrow_test_images\useful_frames\{a}_arrow.png".format(a=direction)
            os.rename(src=src, dst=dest)

exit(0)

cap = cv2.VideoCapture(r"..\images\raw_arrows_dun_morogh.mp4")

if cap.isOpened() == False:
    print("Error opening video")

wait_15_fps = int(1000 / 20)
cnt = 0
prev_frame = cv2.imread(r"..\images\test\dun_morogh_first_person.png")
while cap.isOpened():
    break
    # Read the frame
    ret, frame = cap.read()
    if ret:
        # crop the image for the arrow
        arrow_crop_frame = frame[100:130, 1795:1830]
        if cnt == 0:
            prev_frame = cv2.bitwise_not(arrow_crop_frame)

        # if the image is the same then remove it
        diff = cv2.subtract(arrow_crop_frame, prev_frame)
        b, g, r = cv2.split(diff)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            continue
        else:
            prev_frame = arrow_crop_frame

        # save the image
        file_name = r"..\images\training_images\minimap_arrows\dun_morogh\in_processing\arrow_num_" + str(cnt) + ".png"
        cv2.imshow("frame", arrow_crop_frame)
        cv2.imwrite(file_name, arrow_crop_frame)
        print(cnt)
        cnt += 1
    else:
        break

cap.release()


# ==================================================================================================
cap = cv2.VideoCapture(r"..\images\raw_arrows_dun_morogh.mp4")
if cap.isOpened() == False:
    print("Error opening video")
cnt = 0
prev_frame = cv2.imread(r"..\images\test\dun_morogh_first_person.png")

while cap.isOpened():
    # Read the frame
    ret, frame = cap.read()
    if ret:
        pass
    else:
        break

north_arrow = cv2.imread(r"..\images\training_images\minimap_arrows\dun_morogh\_n_arrow.png")
northeast_arrow = cv2.imread(r"..\images\training_images\minimap_arrows\dun_morogh\_ne_arrow.png")
east_arrow = cv2.imread(r"..\images\training_images\minimap_arrows\dun_morogh\_e_arrow.png")
southeast_arrow = cv2.imread(r"..\images\training_images\minimap_arrows\dun_morogh\_se_arrow.png")
south_arrow = cv2.imread(r"..\images\training_images\minimap_arrows\dun_morogh\_s_arrow.png")
southwest_arrow = cv2.imread(r"..\images\training_images\minimap_arrows\dun_morogh\_sw_arrow.png")
west_arrow = cv2.imread(r"..\images\training_images\minimap_arrows\dun_morogh\_w_arrow.png")
northwest_arrow = cv2.imread(r"..\images\training_images\minimap_arrows\dun_morogh\_nw_arrow.png")

cv2.imshow("north_arrow", north_arrow)
cv2.imshow("northeast_arrow", northeast_arrow)
cv2.imshow("east_arrow", east_arrow)
cv2.imshow("southeast_arrow", southeast_arrow)
cv2.imshow("south_arrow", south_arrow)
cv2.imshow("southwest_arrow", southwest_arrow)
cv2.imshow("west_arrow", west_arrow)
cv2.imshow("northwest_arrow", northwest_arrow)

cv2.waitKey(0)

exit(0)
