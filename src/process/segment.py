import SimpleITK as sitk
import numpy as np
from lungmask import LMInferer
def segment(inp_dir):
    print("Reading Dicom directory:", inp_dir)
    reader = sitk.ImageSeriesReader()

    dicom_names = reader.GetGDCMSeriesFileNames(inp_dir)
    reader.SetFileNames(dicom_names)

    image = reader.Execute()

    size = image.GetSize()
    print("Image size:", size[0], size[1], size[2])

    print("Segmenting image")
    inferer = LMInferer(modelname='LTRCLobes', fillmodel='R231')
    mask = inferer.apply(image)

    print("Applying Mask")
    scan = sitk.GetArrayFromImage(image)
    return np.multiply(scan,np.where(mask > 0, 1, 0)), mask

