from bigtree import *
import os
import pydicom

from config import path
from config import dict

tree = {"root": Node("data", path=path.data)}


def is_node_relevant(end_node_path, dictionary):
    dcm_path = end_node_path + "\\" + os.listdir(end_node_path)[0]
    try:
        dcm = pydicom.dcmread(dcm_path)
    except:
        dcm = pydicom.dcmread(dcm_path + ".dicom")
    if dcm.__contains__((0x0008, 0x103e)):
        for word in dictionary:
            if word in dcm[0x0008, 0x103e].value.upper():
                return word
    return ""


def make_tree(data_path, level=1):
    for element in next(os.walk(data_path))[1]:
        parent = data_path.split("\\")[-1]
        # remove unnecessary nodes, i.e. PA extra folder
        if "PA" in parent:
            parent = data_path.split("\\")[-2]
        if "PA" in element:
            make_tree(os.path.join(data_path, element), level)
        else:
            node_path = os.path.join(data_path, element)
            # if leaf node
            if level == 3:
                # check if scan is relevant, i.e. that we want
                type_scan = is_node_relevant(node_path, dict.series)
                if len(type_scan) > 0:
                    tree[element] = Node(element + "-" + type_scan, parent=tree[parent], path=node_path,
                                         type=type_scan)
            else:
                if parent == path.data.split("\\")[-1]: parent = "root"
                tree[element] = Node(element, parent=tree[parent], path=node_path)
            make_tree(node_path, level + 1)


make_tree(path.data)
tree_data = tree_to_dataframe(tree["root"], name_col="name", parent_col="parent", path_col="path", attr_dict={"type": "type", "path": "location"})

if not os.path.exists(path.out): os.mkdir(path.out)
tree_data.to_csv(path.out + "\\tree.csv", index=False)