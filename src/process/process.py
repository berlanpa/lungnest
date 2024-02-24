import pandas as pd
from bigtree import *
import SimpleITK as sitk

from config.path import out
from segment import segment

tree = dataframe_to_tree(pd.read_csv(out + "\\tree.csv"))


def export(root):
    for patient in root.children:
        for date in patient.children:
            for session in date.children:
                for scan in session.children:
                    # define exit path
                    out_path = out + "\\" + "\\".join(scan.path_name[:-1].split("/")[2:])
                    print(scan.node_name[:-1])
                    lung, mask = segment(scan.location)
                    sitk.WriteImage(sitk.GetImageFromArray(lung), out_path + "\\lung.mha")
                    sitk.WriteImage(sitk.GetImageFromArray(mask), out_path + "\\mask.mha")


export(tree)
