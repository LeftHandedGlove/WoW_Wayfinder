import cv2
import numpy as np
import math
import time


all_nodes = list()

# All of the node types and their colors
node_types = ["path", "start", "end"]
node_types_and_colors = {
    "path": np.array([0, 0, 0]),
    "start": np.array([0, 255, 0]),
    "end": np.array([0, 0, 255])
}
not_node_color = np.array([255, 255, 255])

# Load the image
# safe_area_img = cv2.imread(r"..\images\Zone_Path_Maps\Dun_Morogh_Path_Map.png")
safe_area_img = cv2.imread(r"..\images\test\simple_safe_map.png")


class Node:
    def __init__(self, coords: [tuple], node_type):
        # Dict of neighbors and their weights
        self.neighbors = dict()
        self.coords = coords
        self.node_type = node_type
        self.fastest_through_node = None
        self.cost = 0

    def add_neighbor(self, neighbor_node, distance):
        self.neighbors[neighbor_node] = distance


def does_node_already_exist(coords):
    for node in all_nodes:
        if node.coords == coords:
            return True
    return False


def is_pixel_color(pixel, color):
    b, g, r = pixel.ravel()
    if b == color[0] and g == color[1] and r == color[2]:
        return True
    return False


def create_all_nodes(img):
    for row_idx, row in enumerate(img):
        for col_idx, pixel in enumerate(row):
            for node_type, color in node_types_and_colors.items():
                if is_pixel_color(pixel, color):
                    new_node = Node(coords=(col_idx, row_idx), node_type=node_type)
                    all_nodes.append(new_node)


def connect_all_neighbors():
    for node in all_nodes:
        node_x, node_y = node.coords
        for potential_neighbor_node in all_nodes:
            if node == potential_neighbor_node:
                continue
            potential_neighbor_node_x, potential_neighbor_node_y = potential_neighbor_node.coords
            good_x = False
            good_y = False
            if node_x - 1 <= potential_neighbor_node_x <= node_x + 1:
                good_x = True
            if node_y - 1 <= potential_neighbor_node_y <= node_y + 1:
                good_y = True
            if good_x and good_y:
                dist = math.sqrt((node_x-potential_neighbor_node_x)**2 + (node_y-potential_neighbor_node_y)**2)
                node.add_neighbor(neighbor_node=potential_neighbor_node, distance=dist)


def find_center_of_start_area(img, start_area_node_type):
    start_area_color = node_types_and_colors[start_area_node_type]
    start_area_mask = cv2.inRange(img, start_area_color, start_area_color)
    start_area_pixel_cords = list()
    for row_idx, row in enumerate(start_area_mask):
        for col_idx, pixel in enumerate(row):
            if pixel == 255:
                start_area_pixel_cords.append([col_idx, row_idx])
    start_area_pixel_cords = np.array(start_area_pixel_cords)
    left, top, width, height = cv2.boundingRect(start_area_pixel_cords)
    mid_x = int(round(left + (width / 2)))
    mid_y = int(round(top + (height / 2)))
    starting_node = get_node_from_coords(coords=(mid_x, mid_y))
    return starting_node


def get_node_from_coords(coords):
    for node in all_nodes:
        if node.coords == coords:
            return node
    return -1, -1


def dykstras_alg(all_nodes, start_node, end_area_node_type):
    optimal_path = []
    finished_nodes = []
    priority_queue = [start_node]
    for node in all_nodes:
        node.cost = 999999999
    start_node.cost = 0
    current_node = start_node
    while True:
        if len(priority_queue) == 0:
            break
        current_node = priority_queue.pop(0)
        if current_node.node_type == end_area_node_type:
            break
        for neighbor_node, path_weight in current_node.neighbors.items():
            if neighbor_node.cost > current_node.cost + path_weight:
                neighbor_node.cost = current_node.cost + path_weight
                neighbor_node.fastest_through_node = current_node
            if (neighbor_node not in finished_nodes) and (neighbor_node not in priority_queue):
                priority_queue.append(neighbor_node)
        finished_nodes.append(current_node)
        priority_queue.sort(key=lambda x: x.cost, reverse=False)
    while True:
        if current_node is not start_node:
            optimal_path.append(current_node)
            current_node = current_node.fastest_through_node
        else:
            optimal_path.append(start_node)
            break
    optimal_path.reverse()
    return optimal_path


def add_optimal_path_to_img(img, optimal_path):
    marked_img = img.copy()
    for node in optimal_path:
        x, y = node.coords
        marked_img[y, x] = [126, 0, 255]
    return marked_img


def cleanup_optimal_path(img, optimal_path):
    cleaned_optimal_path = optimal_path
    print(optimal_path[0].node_type)
    for node_num, node in enumerate(optimal_path):
        for next_node_num, next_node in enumerate(optimal_path[node_num+1:]):
            # if next node in los then continue
            if node_in_los(img=img, start_node=node, end_node=next_node):
                # TODO
                pass
            # when it leaves, get the previous node
    return cleaned_optimal_path


def node_in_los(img, start_node, end_node):
    not_white_mask = cv2.inRange(img, not_node_color, not_node_color)
    not_white_mask = cv2.bitwise_not(not_white_mask)
    img_copy = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.line(img_copy, start_node.coords, end_node.coords, (255, 0, 0), 1)
    img_copy = cv2.bitwise_or(not_white_mask, img_copy)
    cv2.imshow("or img", img_copy)
    cv2.waitKey(100)
    diff_img = cv2.bitwise_xor(not_white_mask, img_copy)
    print(cv2.countNonZero(diff_img))
    if cv2.countNonZero(diff_img) > 0:
        return False
    cv2.imshow("img_copy", img_copy)
    cv2.imshow("not_white_mask", not_white_mask)



if __name__ == '__main__':
    start_time = time.time()
    create_all_nodes(img=safe_area_img)
    print("Create nodes time: {a}".format(a=time.time()-start_time))
    connect_all_neighbors()
    print("Connect nodes time: {a}".format(a=time.time() - start_time))
    start_node = find_center_of_start_area(img=safe_area_img, start_area_node_type="start")
    print("Finding start node: {a}".format(a=time.time() - start_time))
    optimal_path = dykstras_alg(all_nodes=all_nodes, start_node=start_node, end_area_node_type="end")
    print(len(optimal_path))
    optimal_path = cleanup_optimal_path(img=safe_area_img, optimal_path=optimal_path)
    print(len(optimal_path))
    print("Optimal path time: {a}".format(a=time.time() - start_time))
    marked_img = add_optimal_path_to_img(img=safe_area_img, optimal_path=optimal_path)
    print("Total time: {a}".format(a=time.time()-start_time))
    cv2.imshow("marked_img", marked_img)
    cv2.imwrite("marked_img.png", marked_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
