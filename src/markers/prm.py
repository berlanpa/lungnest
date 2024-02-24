import os
import numpy as np
import pandas as pd
from bigtree import *
import SimpleITK as sitk

from config.path import out
if not os.path.exists(out + "\\inspi\\prm"): os.makedirs(out + "\\inspi\\prm")
tree = dataframe_to_tree(pd.read_csv(out + "\\tree.csv"))
mld = pd.read_csv(out + "\\mld.csv")
for index, row in mld.iterrows():
    if index != 11: continue
    base = "\\".join([out, row['Patient'], str(row['Date'])])
    inpath = "\\".join([base] + row['In.Loc.'].split("-")) + "-INSPI\\lung.mha"
    expath = "\\".join([base] + row['Ex.Loc.'].split("-")) + "-EXPI\\registered.mha"
    # get images
    reader = sitk.ImageFileReader()
    reader.SetImageIO("MetaImageIO")
    reader.SetFileName(inpath); inspi = sitk.GetArrayFromImage(reader.Execute())
    reader.SetFileName(expath); expi = sitk.GetArrayFromImage(reader.Execute())
    # calculate intervals
    emph = np.where(np.logical_and(inspi < -950, expi < -856))
    sad = np.where(np.logical_and(np.logical_and(inspi < -850, inspi > -950), expi < -857))
    pad = np.where(np.logical_and(np.logical_and(inspi < -500, inspi > -810), expi < -500))
    nrml = np.where(np.logical_and(np.logical_and(inspi < -810, inspi > -950), np.logical_and(expi < -500, expi > -856)))
    # apply to lobe mask
    prm = np.empty_like(inspi)
    prm[emph] = 4; prm[sad] = 3; prm[pad] = 2; prm[nrml] = 1
    sitk.WriteImage(sitk.GetImageFromArray(prm), out + "\\inspi\\prm\\" + "_".join([row['Patient'], str(row['Date'])]) + ".mha")
