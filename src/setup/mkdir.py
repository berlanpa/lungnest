from bigtree import *
import pandas as pd
import os

from config import path

tree_data = pd.read_csv(path.out + "\\tree.csv")
data = dataframe_to_tree(tree_data)
offset = len(data.path_name)


def mkdir_node(node):
    os.mkdir(path.out + node.path_name[offset:])
    return True


def mkdir():
    for patient in data.children:
        mkdir_node(patient)
        for date in patient.children:
            mkdir_node(date)
            for session in date.children:
                mkdir_node(session)
                for scan in session.children:
                    mkdir_node(scan)

mkdir()