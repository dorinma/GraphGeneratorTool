#   Read input from configuration file
#   Write output to .gr, .co, query files

import os

dir = os.getcwd() + "\\config\\"
FILE_NAME_CONFIG = "config.txt"


def read_config():
    objectives = {}

    try:
        file = open(dir + FILE_NAME_CONFIG, 'r')

        for line in file:
            line_str = line.split('\t')
            objectives[line_str[0]] = (int(line_str[1]), int(line_str[2].removesuffix("\n")))

        file.close()
    except:
        print("[ERROR] Could not read config file.")
    return objectives
