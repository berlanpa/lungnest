import numpy as np
from scipy.io import loadmat, savemat
from skimage import measure
# continuity is useless for noise reduction from lung, keeps trachea
# no efficient way to remove trachea info


size = 512
path = "C:\\Users\\Pablo\\Documents\\professional\\idesp-2023\\maria-felicia\\projects\\segmentation\\out\\C1-P16" \
       "\\20200109\\ST0\\SE2-EXPI"

# data loading and quick analysis
test = loadmat(path + "\\mask.mat")['out']
raw = np.array(test)
change = np.where(raw[0, 1:] - raw[0, :-1] > 0)[0] + 1

# !!! need to add empty arrays to chunk in case empty layers in data
# reformat data to 3d
data = np.split(raw[1:].transpose(), change)

# step 1: rough removal of trachea by top-to-bottom traversal
# settings
cut = 10
thresh = len(data) // 2
top = thresh
# outer scope variable
trachea, lung_top, lung_reached = [], [], False

for floor in range(0, thresh, cut):
    # initialization
    block, display = data[floor:floor + cut], np.zeros((cut + 1, size, size))

    # display initialization
    if floor != 0:
        for voxel in trachea[-1]: display[tuple([0, voxel[0], voxel[1]])] = 1
    for c, layer in enumerate(block):
        for voxel in layer: display[tuple([c + 1, voxel[0], voxel[1]])] = 1

    # label connected areas
    labels = measure.label(display)
    regions = measure.regionprops(labels)
    regions.sort(key=lambda x: (x.bbox[0], x.area))

    # !!! need to update condition in case of small regions that might appear before lung
    # target length (a bit after top of lung)
    if len(regions) > 2  and regions[1].area_bbox > 200 and not lung_reached: top = floor; lung_reached = True
    if floor > top + cut * 3: break

    # define trachea chunk from block of layers
    chunk = np.asarray(np.where(labels == regions[0].label))
    # manipulation to fit data format
    chunk_change = np.where(chunk[0, 1:] - chunk[0, :-1] > 0)[0] + 1
    chunk = np.split(chunk[1:].transpose(), chunk_change)

    # add lung to be anything else (this is to facilitate step 2)
    if lung_reached:
        if len(regions) > 1:
            lung_chunk = np.asarray(np.where(labels == regions[1].label))
            if len(regions) > 2:
                for r in regions[2:]:  lung_chunk = np.concatenate((lung_chunk,np.asarray(np.where(labels == r.label))), axis = 1)
            lung_chunk = lung_chunk[:, lung_chunk[0].argsort()]
            lung_chunk_change = np.where(lung_chunk[0, 1:] - lung_chunk[0, :-1] > 0)[0] + 1
            lung_chunk = np.split(lung_chunk[1:].transpose(), lung_chunk_change)
            lung_top += lung_chunk

    # !!! need to add empty arrays to chunk in case length is not 10
    # add chunk to trachea
    if floor == 0:
        trachea = chunk
    else:
        trachea += chunk[1:]

# step 2: remove main bit of trachea from lung
# !!! again is fucked if empty rows appear
top += (cut - len(lung_top) % cut)
lung_data = lung_top + data[top:]

# step 3: noise reduction, keep only lung
# settings
cut = 2
thresh = len(lung_data) // 3 * 2 // cut * cut
# outer scope variable
lung = []
for ceil in range(thresh, 0, - cut):
    # initialization
    block, display = lung_data[ceil - cut: ceil], np.zeros((cut + 1, size, size))

    # display initialization
    # if ceil != thresh:
    #    for voxel in lung[1 - cut]: display[tuple([cut, voxel[0], voxel[1]])] = 1
    for c, layer in enumerate(block):
        for voxel in layer: display[tuple([c, voxel[0], voxel[1]])] = 1

    # label connected areas
    labels = measure.label(display)
    regions = measure.regionprops(labels)
    regions.sort(key=lambda x: (x.bbox[3], x.area), reverse = True)

    # define trachea chunk from block of layers
    chunk = np.asarray(np.where(labels == regions[0].label))
    # if both lungs present
    if len(regions) > 1:
        chunk = np.concatenate((chunk,np.asarray(np.where(labels == regions[1].label))), axis = 1)
        chunk = chunk[:, chunk[0].argsort()]
    # manipulation to fit data format
    chunk_change = np.where(chunk[0, 1:] - chunk[0, :-1] > 0)[0] + 1
    chunk = np.split(chunk[1:].transpose(), chunk_change)
    # !!! need to add empty arrays to chunk in case length is not 10
    # add chunk to trachea
    if ceil == thresh:
        lung = chunk
    else:
        lung = chunk + lung

lung += lung_data[thresh:]

# reformatting data to fit output
out = np.array([0])
for c in range(0,len(lung)):
    out = np.concatenate((out,np.column_stack(([c + top]*lung[c].shape[0],lung[c])).flatten()))
out = out[1:].reshape(-1,3)

# save
savemat(path + "\\test.mat", mdict={'out': out}, oned_as='row')
