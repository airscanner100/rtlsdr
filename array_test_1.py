
import numpy as np


data = np.arange(6).reshape((3, 2))
np.average(data, axis=1, keepdims=True)

