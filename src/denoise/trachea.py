import numpy as np
from scipy.io import loadmat
from skimage import measure

# implementation isolating trachea and removing it
# does not include trachea branches that go up as traversal is done from top to bottom
# no continuity blocks are isolated
# maybe make it recursive
size = 512
path = "C:\\Users\\Pablo\\Documents\\professional\\idesp-2023\\maria-felicia\\projects\\segmentation\\out\\C1-P16" \
       "\\20200109\\ST0\\SE1-INSPI"


def isolate_trachea(inp):
    # make sure data in array mode
    data = np.array(inp)
    # find breaking points in data when layer is changed
    change = np.where(data[0, 1:] - data[0, :-1] > 0)[0]
    change = np.insert(change, 0, 0)
    # settings (make sure stop is multiple of cut)
    cut = 1
    thresh = len(change) // 3 * 2

    # end array initialization
    trachea = np.array([[0], [0], [0]])
    memory = trachea
    stop, trachea_done = -1, False
    # work way up from top to end of zone 1 (with a bit of overlap to avoid problems)
    for i in range(0, thresh, cut):
        if i == stop: stop += cut - 1; break
        print(i)
        # initialization
        block, ini, lung_hit = data[:, change[i] + 1:change[i + cut] + 1], data[0][change[i]], False
        # base case (does not give right answer)
        if i == 0: ini -= 1
        block_op = np.concatenate((block[0] - ini, block[1], block[2])).reshape((3, -1)).transpose()
        arr = np.zeros((cut + 1, size, size))
        if i != 0:
            for r in memory.transpose(): arr[tuple(r)] = 1
        for r in block_op: arr[tuple(r)] = 1
        # measure label
        labels = measure.label(arr)
        regions = measure.regionprops(labels)
        regions.sort(key=lambda x: (x.bbox[0], x.area))

        # count number of trachea parts + find if lung hit in process
        parts = 0
        for count, r in enumerate(regions):
            if r.bbox[0] == 0:
                if r.area > 5000: lung_hit = True
            else:
                parts = count; break
        if parts == 0: parts = 1
        # add all parts of trachea_chunk together
        trachea_chunk = np.array([[0], [0], [0]])
        for r in regions[0:parts]: trachea_chunk = np.append(trachea_chunk, np.asarray(np.where(labels == r.label)), axis = 1)

        # if branch hit lung, relabelling to identify part and remove:
        if lung_hit:
            # repeat labelling process without top layer
            print("Lung Hit")
            trachea_chunk -= np.array([1, 0, 0])[:, None]
            arr = np.zeros((cut, size, size))
            for r in trachea_chunk[:,1:].transpose():
                if r[0] != -1: arr[tuple(r)] = 1
            labels = measure.label(arr)
            regions = measure.regionprops(labels)
            regions.sort(key=lambda x: -x.area)
            for r in regions: print(r.bbox[0], r.area)
            parts = 0
            for count, r in enumerate(regions):
                if r.area < 5000:
                    parts = count; break
            if parts == 0: return trachea[:,1:]
            trachea_chunk = np.array([[0], [0], [0]])
            for r in regions[parts:]: trachea_chunk = np.append(trachea_chunk, np.asarray(np.where(labels == r.label)),
                                                                 axis=1)
            trachea_chunk += np.array([1, 0, 0])[:, None]
        # if all branches hit lung, ie trachea done, stop
        # keep last layer of chunk as memory
        chunk_end = np.where(trachea_chunk[0] == cut)
        memory = trachea_chunk[:, chunk_end].reshape(3, -1) - np.array([cut, 0, 0])[:, None]
        # memory chunk added twice
        trachea = np.append(trachea, trachea_chunk[:,1:] + np.array([ini, 0, 0])[:, None], axis=1)
    print("Fail")
    return 0

test = isolate_trachea(loadmat(path + "\\mask.mat")['out'])
print(test)
