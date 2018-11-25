
def get_node_from_node_id(node_id):
    for node in all_nodes:
        if node_id == node.name:
            return node


def setup():
    # Make all of the nodes
    for node_id in connections:
        all_nodes.append(Node(name=node_id))

    # Connect all of the nodes
    for node in all_nodes:
        neighbors_dict = connections[node.name]
        for neighbor_node_id, path_weight in neighbors_dict.items():
            neighbor_node = get_node_from_node_id(neighbor_node_id)
            node.add_neighbor(neighbor_node=neighbor_node, distance=path_weight)


class Node:
    def __init__(self, name):
        self.name = name
        # Dict of neighbors and their weights
        self.neighbors = dict()
        self.fastest_through_node = None
        self.cost = 0

    def add_neighbor(self, neighbor_node, distance):
        self.neighbors[neighbor_node] = distance


all_nodes = list()

connections = {
    "A": {"B": 4, "C": 3, "E": 7},
    "B": {"A": 5, "C": 6, "D": 5},
    "C": {"A": 2, "B": 6, "D": 11, "E": 8},
    "D": {"B": 6, "C": 9, "E": 2, "F": 2, "G": 10},
    "E": {"A": 8, "C": 7, "D": 5, "G": 5},
    "F": {"D": 4, "G": 3},
    "G": {"D": 6, "E": 6, "F": 2}
}


def dykstras_alg(all_nodes, start_node, end_node):
    optimal_path = [start_node]
    finished_nodes = []
    unfinished_nodes = all_nodes
    priority_queue = [start_node]
    for node in all_nodes:
        node.cost = 999999999
    start_node.cost = 0
    while True:
        if len(priority_queue) == 0:
            break
        current_node = priority_queue.pop(0)
        for neighbor_node, path_weight in current_node.neighbors.items():
            if neighbor_node.cost > current_node.cost + path_weight:
                neighbor_node.cost = current_node.cost + path_weight
            if (neighbor_node not in finished_nodes) and (neighbor_node not in priority_queue):
                priority_queue.append(neighbor_node)
        finished_nodes.append(current_node)
        priority_queue.sort(key=lambda x: x.cost, reverse=False)
        print("------------- {} -------------".format(current_node.name))
        for node in priority_queue:
            print(node.name, node.cost)
    print("==============================")
    for node in all_nodes:
        print(node.name, node.cost)
    exit(0)

'''
    for node in all_nodes:
        for neighbor_node, path_weight in node.neighbors.items():
            print(neighbor_node, neighbor_node.name, path_weight)
            if neighbor_node.cost > node.cost + path_weight:
                neighbor_node.cost = node.cost + path_weight:
    return optimal_path
    '''


setup()
dykstras_alg(all_nodes=all_nodes, start_node=all_nodes[0], end_node=all_nodes[5])

