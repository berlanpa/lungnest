from bigtree import *
import pandas as pd
from scipy.io import loadmat, savemat

from src.scan.define import DataScan, Scan
from src.config.path import out

rows = ['type', 'date', 'size']

def export(root, print_array=False):
    for patient in root.children:
        for date in patient.children:
            for session in date.children:
                for scan in session.children:
                    out_path = out + "\\" + "\\".join(scan.path_name[:-1].split("/")[2:])
                    info = pd.DataFrame((s, vars(Scan(scan.location))[s]) for s in rows).transpose()
                    info.to_csv(out_path + "\\id.csv", index=False, header=False)
                    if print_array:
                        savemat(out_path + "\\raw.mat", mdict={'out': DataScan(scan.location).data}, oned_as='row')


tree = dataframe_to_tree(pd.read_csv(out + "\\read.csv"))
export(tree, True)
