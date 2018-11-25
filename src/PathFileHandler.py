import os
import json

class PathFileHandler:
    top_dir = os.getcwd()
    top_dir = top_dir[:top_dir.find("WoW_Wayfinder")+len("WoW_Wayfinder")+1]
    path_files_dir = top_dir + "path_files" + os.sep

    def __init__(self):
        self.all_nodes = list()
        self.node_paths = dict()

    def load_all_nodes(self):

        all_path_files = os.listdir(PathFileHandler.top_dir + "path_files" + os.sep)
        print(all_path_files)
        with open(PathFileHandler.path_files_dir + "Dun_Morogh.json") as json_file:
            dun_morogh_dict = json.load(json_file)
        print(dun_morogh_dict["subzones"])

test = PathFileHandler()
test.load_all_nodes()