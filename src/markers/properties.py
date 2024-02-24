import pandas as pd
import numpy as np
from bigtree import *
import SimpleITK as sitk
import hashlib
from scipy.stats import kurtosis, skew, skewnorm

from config.path import out
from config.dict import threshold

tree = dataframe_to_tree(pd.read_csv(out + "\\tree.csv"))


def export(root):
    count = 0
    columns = ['Hash', 'Patient', 'Date', 'Session', 'Scan', 'Type', 'Priority', 'Volume', 'Mean', 'Variance', 'Median', 'Skew',
               'Kurtosis', 'Shape', 'Location', 'Scale']
    df = pd.DataFrame([], columns = columns)
    for patient in root.children:
        # momentary stop
        if count == 2:
            break
        count += 1
        for date in patient.children:
            block = []
            for session in date.children:
                for scan in session.children:
                    # define exit path
                    out_path = out + "\\" + "\\".join(scan.path_name[:-1].split("/")[2:])
                    reader = sitk.ImageFileReader()
                    reader.SetImageIO("MetaImageIO")
                    reader.SetFileName(out_path + "\\lung.mha")
                    image = reader.Execute()
                    arr = sitk.GetArrayFromImage(image).flatten()
                    # remove -1024 outlier
                    indices = np.where(np.logical_and(arr <= threshold[1], arr > threshold[0]))[0]
                    volume, lung = len(indices),  arr[indices]
                    sample = np.random.choice(arr[indices], size=int(np.power(volume, 3/4)))
                    mean, var, median, skewed, kurt = np.mean(lung), np.var(lung), np.median(lung), skew(lung), kurtosis(lung)
                    print(scan.node_name, volume, mean, var, median, skewed, kurt)
                    # estimate fit
                    shape, location, scale = skewnorm.fit(sample)
                    print(shape, location, scale)
                    key = hashlib.sha1('-'.join(scan.path_name.split('/')[2:])[:-1].encode("UTF-8")).hexdigest()[:10]
                    block += [key, patient.node_name, date.node_name, session.node_name,
                                             scan.node_name.split('-')[0], scan.node_name.split('-')[1][:-1], 0,
                                             volume, mean, var, median, skewed, kurt, shape, location, scale]
            block = np.array(block).reshape(-1,len(columns))
            block = block[block[:, 8].argsort()]
            block = block[block[:, 6].argsort(kind='mergesort')]
            for i in range(len(block)):
                if block[i][5] == 'INSPI': block[i][6] = len(block) - i
                elif block[i][5] == 'EXPI': block[i][6] = i + 1
            df = pd.concat([df,pd.DataFrame(block, columns = columns)], ignore_index = True)
            print(df)
    df.to_csv(out + "\\master.csv", index=False)


export(tree)
