import numpy as np
from skimage import measure
# very funky for when top lung ends - collects a bit trachea - needs fixing
# no continuity blocks are isolated

def remove_trachea(inp):
    # make sure data in array mode
    data = np.array(inp)

    # find breaking points in data when layer is changed
    change = np.where(data[0, 1:] - data[0, :-1] > 0)[0]

    # settings
    cut = 1
    thresh = len(change) // 3 * 2

    # split data into relevant data, and other
    zone_rest, zone_3 = data[:, :change[thresh]], data[:, change[thresh]:]

    # end array initialization
    data_out = np.array([[0], [0], [0]])

    # work way up from top of zone_3 to top
    for i in range(thresh, 0, -cut):
        # initialization
        block, ini = data[:, change[i - cut] + 1:change[i]], data[0][change[i - cut] + 1]
        block_op = np.concatenate((block[0] - ini, block[1], block[2])).reshape((3, -1)).transpose()
        arr = np.zeros((cut, max(block[1]) + 1, max(block[2]) + 1))
        for r in block_op: arr[tuple(r)] = 1

        # measure label
        labels = measure.label(arr)
        regions = measure.regionprops(labels)
        regions.sort(key=lambda x: x.area_bbox, reverse=True)

        # if just trachea, remove rest, aka zone 1
        if len(regions) == 1 and i < thresh // 2:
            break
        # else do process as usual
        else:
            # for top of lung
            center = [cut / 2, max(block[1]) / 2 + 1, max(block[2]) / 2 + 1]
            if 1 < len(regions) <= 3 and np.mean([r.area_bbox for r in regions]) / regions[1].area_bbox < 0.2:
                regions.sort(key=lambda x: np.linalg.norm(x.centroid - center), reverse=True)
            if len(regions) != 1:
                left_lung, right_lung = np.where(labels == regions[0].label), np.where(labels == regions[1].label)
                lung = np.concatenate((left_lung, right_lung), axis=1)
                # in case one of two regions highlighted is trachea
                if i < thresh // 2:
                    if abs(regions[0].centroid[1] - 512/2) < 20: lung = right_lung
                    elif abs(regions[1].centroid[1] - 512/2) < 20: lung = left_lung

                lung += np.array([ini, 0, 0])[:, None]
            else:
                lung = np.where(labels == regions[0].label) + np.array([ini, 0, 0])[:, None]
            data_out = np.append(data_out, lung, axis=1)

    return np.append(data_out[:, 1:], zone_3, axis=1)
