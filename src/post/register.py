import pandas as pd
import numpy as np
import torchio as tio
from bigtree import *
import SimpleITK as sitk
from time import time

from config.path import out
from define import register

tree = dataframe_to_tree(pd.read_csv(out + "\\tree.csv"))
mld = pd.read_csv(out + "\\mld.csv")
for index, row in mld.iterrows():
    initial_time = time(); print(index, time())
    base = "\\".join([out, row['Patient'], str(row['Date'])])
    inpath = "\\".join([base] + row['In.Loc.'].split("-")) + "-INSPI"
    expath = "\\".join([base] + row['Ex.Loc.'].split("-")) + "-EXPI"
    # get images
    reader = sitk.ImageFileReader()
    reader.SetImageIO("MetaImageIO")
    reader.SetFileName(inpath + "\\lung.mha"); fixed = reader.Execute()
    reader.SetFileName(expath + "\\lung.mha"); moving = reader.Execute()
    inspi = sitk.GetArrayFromImage(fixed)
    expi = sitk.GetArrayFromImage(moving)
    print("Data loaded", time() - initial_time)

    # upscale expi to be same box shape as inspi
    # testing dataset
    # find indexes in all axis
    xi, yi, zi = np.where(inspi != 0)
    # extract cube with extreme limits of where are the values != 0
    cropped_inspi = inspi[min(xi):max(xi) + 1, min(yi):max(yi) + 1, min(zi):max(zi) + 1]
    sitk.WriteImage(sitk.GetImageFromArray(cropped_inspi), inpath + '\\cropped-inspi.mha')

    # find indexes in all axis
    xs, ys, zs = np.where(expi != 0)
    cropped_expi = expi[min(xs):max(xs) + 1, min(ys):max(ys) + 1, min(zs):max(zs) + 1]
    sitk.WriteImage(sitk.GetImageFromArray(cropped_expi), expath + '\\cropped-expi.mha')
    print("Done with cropping, starting resampling")
    transform = tio.Resize((cropped_inspi.shape[2], cropped_inspi.shape[1], cropped_inspi.shape[0]),
                           image_interpolation='bspline', label_interpolation='bspline')
    resampled = transform(tio.ScalarImage(expath + '\\cropped-expi.mha'))
    array = resampled.data.numpy()[0]
    array_corrected = np.flip(np.rot90(array, 3, axes=(0, 2)), axis=2)
    sitk.WriteImage(sitk.GetImageFromArray(array_corrected), expath + '\\resampled.mha')
    print("Done with resampling, starting registration")
    # affine and register
    final, shift = register(sitk.GetImageFromArray(cropped_inspi), sitk.GetImageFromArray(array_corrected))
    sitk.WriteImage(final, expath + '\\final.mha')
    print("Done in: " + str(time() - initial_time) + " seconds.")
