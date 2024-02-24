import numpy as np
from sklearn.cluster import KMeans


def inside(x, y, dia):
    return (x - (dia - 1) / 2) ** 2 + (y - (dia - 1) / 2) ** 2 < ((dia - 0.5) / 2) ** 2


def circle_mask(length, height):
    return np.tile(np.ma.fromfunction(lambda i, j: inside(i, j, length), (length, length), dtype=int).flatten() * 1, height)


def sampled(data, indices):
    shrink = np.round(np.power(len(indices), 1 / 2))
    chosen_indices = np.random.choice(indices, size=shrink.astype(int))
    return np.take(data, chosen_indices)


def thresh_kmeans(inp):
    kmeans = KMeans(n_clusters=2).fit(inp.reshape(-1, 1))
    return np.round(np.mean(kmeans.cluster_centers_))


def threshold(raw, length):
    slice_number = len(raw)
    circle = circle_mask(length, slice_number)
    circle_indices = np.where(circle == 1)[0]
    data = raw.flatten() * circle
    return thresh_kmeans(sampled(data, circle_indices))

