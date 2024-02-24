import numpy as np
from skimage import measure


def mask(raw, threshold):
    img = np.where(raw < threshold, 1, 0)
    labels = measure.label(img)
    regions = measure.regionprops(labels)
    lung = max(regions[1:], key=lambda x: x.area)
    print(lung.label, lung.area, lung.centroid)
    return np.where(labels == lung.label)