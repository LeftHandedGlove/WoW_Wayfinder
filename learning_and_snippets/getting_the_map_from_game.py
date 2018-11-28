import cv2

# With an image of the game where the map is open, get the map
game_frame = cv2.imread(r"..\images\test\open_map.png")

# Potentially find the corners of the map with know images (need to test)
top = 0
bottom = 0
left = 0
right = 0

map_img = game_frame[top:bottom, left:right]
cv2.imshow(map_img)
