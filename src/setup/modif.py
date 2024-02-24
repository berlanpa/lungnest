from bigtree import *
import pydicom
import pandas as pd
import os

from src.config import path

# fix issues with exporting .dot file to .png using graphviz
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'


def find_date(session_node):
    dcm_path = (session_node.children[0]).location + "\\" + os.listdir((session_node.children[0]).location)[0]
    dcm = pydicom.dcmread(dcm_path)
    return str(dcm[0x0008, 0x0023].value)


def split_by_date(tree):
    for patient in tree.children:
        dates = {}
        for session in patient.children:
            # delete session if empty, i.e. no relevant scans were selected
            if len(session.children) == 0:
                shift_nodes(
                    data,
                    from_paths=[session.path_name],
                    to_paths=[""]
                )
            else:
                date = find_date(session)
                if date not in dates:
                    dates[date] = Node(date, parent=patient)
                shift_nodes(
                    data,
                    from_paths=[session.path_name],
                    to_paths=[dates[date].path_name + "/" + session.name]
                )
    return tree


og_tree_data = pd.read_csv(path.out + "\\read.csv")
data = dataframe_to_tree(og_tree_data)

new_data = split_by_date(data)
print_tree(new_data)

tree_data = tree_to_dataframe(new_data, name_col="name", parent_col="parent", path_col="path",
                              attr_dict={"type": "type", "location": "location"})
tree_data.to_csv(path.out + "\\read.csv", index=False)

tree_visual = tree_to_dot(new_data)
tree_visual.write_png(path.out + "\\visual.png")