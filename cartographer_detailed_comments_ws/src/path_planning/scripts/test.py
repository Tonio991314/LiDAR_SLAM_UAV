#!/usr/bin/env python
# print("hello world")
import numpy as np


a = (1, 1, 2, 4, 2, 3)
b = (2, 3, 4, 5, 6, 7)
# c=[]
# for i in range(len(a)):
#     c.append((a[i], b[i], 0.1))
# print(c)

d = np.column_stack((a, b, np.full_like(a, 0.1, dtype=np.float64)))
# d = np.vstack((a, b, np.full_like(a, 0.1))).T.toli    st()
d = list(map(tuple, d))
print(d)

# indices = np.where(np.array(a) == 2)[0]
# result = indices / 2
# print(result)
