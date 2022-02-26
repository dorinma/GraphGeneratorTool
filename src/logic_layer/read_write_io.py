#   Read input from configuration file
#   Write output to .gr, .co, query files

import os
import json

resources_dir = os.path.dirname(os.getcwd()) + "\\GraphGeneratorTool\\resources\\"
FILE_NAME_CONFIG = "config.txt"
FILE_NAME_INPUT = "input.json"


def read_config():
    objectives = {}

    try:
        file = open(resources_dir + FILE_NAME_CONFIG, 'r')
        for line in file:
            line_str = line.split('\t')
            objectives[line_str[0]] = (int(line_str[1]), int(line_str[2].removesuffix("\n")))

        file.close()
    except:
        print("[ERROR] Could not read config file.")
    return objectives


def write_to_file_gr(full_path, edges):
    try:
        file = open(full_path + ".gr", 'w')
        file.writelines(edges)
        file.close()
        print("[INFO] Saved output to " + full_path)
    except:
        print("[ERROR] Could not write .gr file.")


def write_to_file_co(full_path, edges):
    try:
        file = open(full_path + '.co', 'w')
        file.writelines(edges)
        file.close()
        print("[INFO] Saved output to " + full_path)
    except:
        print("[ERROR] Could not write .co file.")


def write_to_file_query(full_path, edges):
    try:
        file = open(full_path, 'w')
        file.writelines(edges)
        file.close()
        print("[INFO] Saved output to " + full_path)
    except:
        print("[ERROR] Could not write query file.")


def read_json(path):
    try:
        if path:
            with open(path, 'r') as f:
                data = json.load(f)
            return data
        else:
            with open(resources_dir + FILE_NAME_INPUT, 'r') as f:
                data = json.load(f)
            return data
    except:
        print("[ERROR] Could not read input file.")
        return ""


def read_single_state(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    except:
        print("[ERROR] Could not read input file.")
        return ""
