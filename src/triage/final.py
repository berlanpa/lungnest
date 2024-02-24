import shutil
import pandas as pd
from bigtree import *
import os

from config.path import out

# check if directories exist
if not os.path.exists(out + "\\expi"): os.mkdir(out + "\\expi")
if not os.path.exists(out + "\\inspi"): os.mkdir(out + "\\inspi")
if not os.path.exists(out + "\\inspi\\lung"): os.mkdir(out + "\\inspi\\lung")
if not os.path.exists(out + "\\inspi\\lobes"): os.mkdir(out + "\\inspi\\lobes")
if not os.path.exists(out + "\\inspi\\visual"): os.mkdir(out + "\\inspi\\visual")
if not os.path.exists(out + "\\inspi\\lung"): os.mkdir(out + "\\inspi\\lung")
if not os.path.exists(out + "\\expi\\lobes"): os.mkdir(out + "\\expi\\lobes")
if not os.path.exists(out + "\\expi\\visual"): os.mkdir(out + "\\expi\\visual")
if not os.path.exists(out + "\\expi\\lung"): os.mkdir(out + "\\expi\\lung")
if not os.path.exists(out + "\\expi\\registered"): os.mkdir(out + "\\expi\\registered")
if not os.path.exists(out + "\\expi\\transform"): os.mkdir(out + "\\expi\\transform")

tree = dataframe_to_tree(pd.read_csv(out + "\\tree.csv"))
master = pd.read_csv(out + "\\master.csv")
for index, row in master.iterrows():
    base = "\\".join([out, row['Patient'], str(row['Date'])])
    path = "\\".join([base, row['Session'], row['Scan'] + "-" + row['Type']])
    scan_type = row['Type'].lower()
    id = "_".join([row['Patient'], str(row['Date'])])
    if row['Priority'] !=  1:
        id = "_".join([row['Patient'], str(row['Date']), str(row['Priority'])])

    try: shutil.move(path + "\\lung.mha", out + "\\" + scan_type + "\\lung\\" + id + ".mha")
    except:
        try:
            shutil.move(path + "\\lung.mhd", out + "\\" + scan_type + "\\lung\\" + id + ".mhd")
            shutil.move(path + "\\lung.raw", out + "\\" + scan_type + "\\lung\\" + id + ".raw")
        except: print("no lung moved")

    try: shutil.move(path + "\\lobes.mha", out + "\\" + scan_type + "\\lobes\\" + id + ".mha")
    except: print("no lobes moved")
    try: shutil.move(path + "\\visual.png", out + "\\" + scan_type + "\\visual\\" + id + ".png")
    except: print("no visual moved")
    if scan_type == "expi":
        try:
            shutil.move(path + "\\registered.mhd", out + "\\" + scan_type + "\\registered\\" + id + ".mhd")
            shutil.move(path + "\\registered.raw", out + "\\" + scan_type + "\\registered\\" + id + ".raw")
            shutil.move(path + "\\transform.tfm", out + "\\" + scan_type + "\\transform\\" + id + ".mha")
        except: print("no registered lung to move")

