import numpy as np
from scipy import ndimage
import pandas as pd
from bigtree import *
import SimpleITK as sitk

from config.path import out

tree = dataframe_to_tree(pd.read_csv(out + "\\tree.csv"))


def export(root):
    for patient in root.children:
        for date in patient.children:
            for session in date.children:
                for scan in session.children:
                    # define exit path
                    out_path = out + "\\" + "\\".join(scan.path_name[:-1].split("/")[2:])
                    print(scan.node_name[:-1])
                    img_path = out_path + "\\mask.mha"
                    reader = sitk.ImageFileReader()
                    reader.SetImageIO("MetaImageIO")
                    reader.SetFileName(img_path)
                    image = reader.Execute()
                    mask = sitk.GetArrayFromImage(image)
                    print("Initiating median filter")
                    refine = ndimage.median_filter(mask, size=10)
                    # put outer-layers as before because median filter expands holes
                    scope = np.where(mask == 0)
                    refine[scope] = 0
                    # morphological operation
                    sitk.WriteImage(sitk.GetImageFromArray(refine), out_path + "\\lobes.mha")


export(tree)