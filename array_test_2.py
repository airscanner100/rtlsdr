
import numpy as np

data1 = np.arange(6).reshape((3, 2))
print(data1)

# Average column values
data2 = np.average(data, axis=0)
print(data2)

# Average row values
data3 = np.average(data, axis=1)
print(data3)