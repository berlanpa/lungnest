import pandas as pd
from time import time
from bigtree import *
from scipy.io import loadmat, savemat

from src.config.path import out
from src.mask.threshold import threshold
from src.mask.mask import mask
from src.denoise.test import denoise

size = 512
tree = dataframe_to_tree(pd.read_csv(out + "\\read.csv"))


def export(root):
    for patient in root.children:
        for date in patient.children:
            for session in date.children:
                for scan in session.children:
                    initial_time = time()
                    # define exit path
                    out_path = out + "\\" + "\\".join(scan.path_name[:-1].split("/")[2:])
                    # load data
                    data = loadmat(out_path + "\\raw.mat")["out"]
                    # output data
                    print(session.node_name, scan.node_name)
                    # find lungs + trachea
                    lung_mask = denoise(mask(data,threshold(data,size)))
                    savemat(out_path + "\\mask.mat", mdict={'out': lung_mask}, oned_as='row')
                    print(time() - initial_time, "seconds")

export(tree)
