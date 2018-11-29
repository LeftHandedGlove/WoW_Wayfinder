import cv2

# With an image of the game where the map is open, get the map
game_frame = cv2.imread(r"..\images\test\no_arrow.png")

top = 97
bottom = 1035
left = 254
right = 1662

map_img = game_frame[top:bottom, left:right]
cv2.imwrite(r"..\images\test\no_arrow.png", map_img)
cv2.imshow("map", map_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

