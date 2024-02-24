import csv
import numpy as np
import pandas as pd
import SimpleITK as sitk
from bigtree import *
from scipy.io import loadmat
from time import time

from src.config.path import out
from src.scan.define import Scan
tree = dataframe_to_tree(pd.read_csv(out + "\\read.csv"))


def export(root):
    writer = sitk.ImageFileWriter()
    for patient in root.children:
        for date in patient.children:
            for session in date.children:
                for scan in session.children:
                    initial_time = time()
                    # define exit path
                    out_path = out + "\\" + "\\".join(scan.path_name[:-1].split("/")[2:])
                    # load data
                    mask = loadmat(out_path + "\\mask.mat")["out"]
                    raw = loadmat(out_path + "\\raw.mat")["out"]
                    # initialize mask in 3d
                    arr = np.zeros((len(raw),512,512))
                    for m in mask: arr[tuple(m)] = 1
                    # get lung data
                    lung = arr * raw
                    # get metadata
                    info, keys = Scan(scan.location).__dict__, {'patient', 'date', 'type', 'size'}
                    relevant_info = {k: info[k] for k in keys} ; relevant_info['volume'] = len(mask)
                    with open(out_path + '\\id.csv', 'w') as csv_file:
                        writer_csv = csv.writer(csv_file)
                        for key, value in relevant_info.items(): writer_csv.writerow([key, value])
                    # export as .mha and metadata as .csv
                    writer.SetFileName(out_path + "\\segmented.mha")
                    writer.Execute(sitk.GetImageFromArray(lung))
                    print("Done in: ", time() - initial_time, " seconds")

export(tree)