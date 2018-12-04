import numpy as np

# All colors are in BGR due to OpenCV using BGR
PATH_COLOR = np.array([127, 127, 127])
IMPASSABLE_COLOR = np.array([0, 0, 0])

RED = np.array([0, 0, 255])
ORANGE = np.array([0, 127, 255])
YELLOW = np.array([0, 255, 255])
YELLOW_GREEN = np.array([0, 255, 127])
GREEN = np.array([0, 255, 0])
LIGHT_GREEN = np.array([127, 255, 0])
CYAN = np.array([255, 255, 0])
INDIGO = np.array([255, 127, 0])
BLUE = np.array([255, 0, 0])
PURPLE = np.array([255, 0, 127])
PINK = np.array([255, 0, 255])
HOT_PINK = np.array([127, 0, 255])
