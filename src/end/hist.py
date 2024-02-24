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
                    raw = loadmat(out_path + "\\raw.mat")["out"].flatten()
                    # initialize mask in 3d
                    indices = mask[0] * mask[1] * mask[2]
                    data = np.take(raw, indices); bounds = [min(data).astype(int), max(data).astype(int)]
                    hist, index = np.zeros(abs(bounds[0]) + abs(bounds[1]) + 1), np.arange(bounds[0],bounds[1] + 1,1)
                    for d in data:
                        hist[d.astype(int) + abs(bounds[0])] += 1
                    pd.DataFrame(np.array([index,hist])[:,2000:].transpose(), columns = ['Unit', 'Occurrences']).to_csv(out_path + "\\hist.csv", index = False)
                    print(scan.node_name,time() - initial_time, " seconds")
export(tree)