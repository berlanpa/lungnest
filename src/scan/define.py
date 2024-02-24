import os
import numpy as np
import pydicom


class Scan:
    def __init__(self, path: str):
        # !!!
        # dependent on file names and not metadata (faster but not optimal)
        self.content = ["IM" + str(s) for s in range(0, len(next(os.walk(path))[2]))]
        self.size = len(self.content)
        self.top = pydicom.dcmread(path + "\\" + self.content[0])
        self.path = path

        # only info from metadata that we want or need
        self.date = self.top[0x0008, 0x0023].value
        self.type = self.top[0x0008, 0x103e].value
        self.patient = self.top[0x0010, 0x0010].value
        # first is intercept, second is slope
        self.rescale = [self.top[0x0028, 0x1052].value, self.top[0x0028, 0x1053].value]


# processed data
class DataScan(Scan):
    def __init__(self, path: str):
        Scan.__init__(self, path)
        self.data = self.load()

    def load_slice(self, name):
        # flatten in case you want to export pixel array as .csv in export.py
        return pydicom.dcmread(self.path + "\\" + name).pixel_array

    def linear(self, m):
        return m * self.rescale[1] + self.rescale[0]

    def transform(self, layer):
        return np.vectorize(self.linear)(np.array(layer))

    def load(self):
        return np.array([self.transform(self.load_slice(s)) for s in self.content])

