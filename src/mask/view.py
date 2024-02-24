import numpy as np
from matplotlib import pyplot as plt
from scipy.io import loadmat

data = loadmat("C:\\Users\\Pablo\\Documents\\professional\\idesp-2023\\maria-felicia\\projects\\segmentation\\out"
                  "\\C1-P16\\20200109\\ST0\\SE1-INSPI\\trachea.mat")["out"]

length = len(data[0])
ndinx = list(np.random.randint(0,length,np.round(np.power(length, 15/20)).astype(int)))
sample = data[:, ndinx]
z = np.array(sample[0])
y = np.array(sample[1])
x = np.array(sample[2])


# Creating figure
fig = plt.figure(figsize=(10, 7))
ax = plt.axes(projection="3d")

# Creating plot
ax.scatter3D(x, y, z, color="green")
plt.title("simple 3D scatter plot")

# show plot
plt.show()
