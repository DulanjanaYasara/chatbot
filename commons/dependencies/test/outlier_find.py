import numpy as np

points = [0.6, 15, 17, 16]
median = np.median(points)
print points - median
print (points - median) ** 2
x = np.sum((points - median) ** 2)
med_abs_deviation = np.sqrt(x / len(points))


# return modified_z_score > thresh
