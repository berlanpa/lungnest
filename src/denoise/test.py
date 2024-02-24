import numpy as np
from scipy.io import loadmat, savemat
from skimage import measure
# continuity is useless for noise reduction from lung, keeps trachea
# no efficient way to remove trachea info

def denoise(inp):
    raw = np.array(inp)
    change = np.where(raw[0, 1:] - raw[0, :-1] > 0)[0] + 1

    # !!! need to add empty arrays to chunk in case empty layers in data
    # reformat data to 3d
    data = np.split(raw[1:].transpose(), change)

    # step 1: rough removal of trachea by top-to-bottom traversal
    # settings
    cut = 1
    thresh = len(data) // 2
    top = 0
    # outer scope variable
    trachea, lung_top, lung_hit, lung_reached = [], 0, False, 0

    for floor in range(0, thresh, cut):
        # initialization
        block, display = data[floor:floor + cut], np.zeros((cut + 1, 512, 512))

        # display initialization
        if floor != 0:
            for voxel in trachea[-1]: display[tuple([0, voxel[0], voxel[1]])] = 1
        for c, layer in enumerate(block):
            for voxel in layer: display[tuple([c + 1, voxel[0], voxel[1]])] = 1

        # label connected areas
        labels = measure.label(display)
        regions = measure.regionprops(labels)
        regions.sort(key=lambda x: (- x.bbox[3], - x.area))

        # !!! need to update condition in case of small regions that might appear before lung
        # target length (a bit after top of lung)
        if len(regions) > 2 and regions[1].bbox[0] != 0 and not lung_reached:
            top = floor + regions[1].bbox[0]
            lung_reached = True

        # count number of trachea parts + find if lung hit in process
        parts = 0
        for count, r in enumerate(regions):
            if r.bbox[0] == 0:
                if r.area > 5000: lung_hit = True
            else:
                parts = count
                break
        if lung_hit:
            lung_reached = floor
            break
        if parts == 0: parts = 1
        # define trachea chunk from block of layers
        chunk = np.array([[0], [0], [0]])
        for r in regions[0:parts]: chunk = np.append(chunk, np.asarray(np.where(labels == r.label)), axis=1)
        chunk = chunk[:, chunk[0].argsort()]
        # manipulation to fit data format
        chunk_change = np.where(chunk[0, 1:] - chunk[0, :-1] > 0)[0] + 1
        chunk = np.split(chunk[1:].transpose(), chunk_change)
        # !!! need to add empty arrays to chunk in case length is not 10
        # add chunk to trachea
        if floor == 0:
            trachea = chunk
        else:
            trachea += chunk[1:]


    raw = np.array(inp)
    change = np.where(raw[0, 1:] - raw[0, :-1] > 0)[0] + 1

    # !!! need to add empty arrays to chunk in case empty layers in data
    # reformat data to 3d
    data = np.split(raw[1:].transpose(), change)

    # step 2: rough removal of trachea by bottom-to-top traversal
    # settings
    cut = 1
    thresh = len(data) // 3 * 2
    top -= 5
    lung = []
    # outer scope variable
    for ceil in range(thresh, top, - cut):
        # initialization
        block, display = data[ceil - cut: ceil], np.zeros((cut + 1, 512, 512))

        # display initialization
        if ceil != thresh and ceil < lung_reached - 1:
           for voxel in lung[0]: display[tuple([cut, voxel[0], voxel[1]])] = 1
        for c, layer in enumerate(block):
            for voxel in layer: display[tuple([c, voxel[0], voxel[1]])] = 1

        # label connected areas
        labels = measure.label(display)
        regions = measure.regionprops(labels)
        regions.sort(key=lambda x: (x.bbox[3], x.area), reverse=True)


        # define trachea chunk from block of layers
        chunk = np.asarray(np.where(labels == regions[0].label))
        # if both lungs present
        if len(regions) > 1:
            if regions[1].bbox[3] == regions[0].bbox[3]:
                chunk = np.concatenate((chunk,np.asarray(np.where(labels == regions[1].label))), axis = 1)
                chunk = chunk[:, chunk[0].argsort()]
        # manipulation to fit data format
        chunk_change = np.where(chunk[0, 1:] - chunk[0, :-1] > 0)[0] + 1
        chunk = np.split(chunk[1:].transpose(), chunk_change)
        # !!! need to add empty arrays to chunk in case length is not 10
        # add chunk to trachea
        if ceil == thresh:
            lung = chunk
        elif ceil < lung_reached - 1:
            lung = chunk[:-1] + lung
        else:
            lung = chunk + lung

    lung += data[thresh:]
    index = raw[0][-1]

    # reformatting data to fit output: traversal done from below to top
    out = []
    for c in range(0,len(lung)):
        if c == 0:
            out = np.column_stack(([index - c]*lung[-c].shape[0],lung[-c])).flatten()
        else:
            out = np.concatenate((out,np.column_stack(([index - c]*lung[-c].shape[0],lung[-c])).flatten()))
    return out.reshape((-1,3))

