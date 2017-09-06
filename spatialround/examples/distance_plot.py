from spatialround import _GEOD, round
import numpy as np


a = np.array([[90.2, 5.5], [80.2, 5.5]]).T

print(a.shape)

ll = round(a)
print('BEOFRE: {};\nAFTER: {}'.format(a, ll))

_, _, dist = _GEOD.inv(a[0], a[1], ll[0], ll[1])

import matplotlib.pyplot as plt

y = np.linspace(-90, 90, 250)
x = np.linspace(-180, 180, 500)
x, y = np.meshgrid(x, y)

points = np.stack([x, y])
# Round within 12.5km
round_distance = 12500
new_points = round(points, round_distance)
_, _, dist = _GEOD.inv(points[0], points[1], new_points[0], new_points[1])

plt.figure(figsize=(10, 5))
plt.title('Rounded distance (@{}m) from original point'
          ''.format(round_distance))
plt.contourf(x, y, dist, 10)
plt.colorbar(label='Distance / meters')
plt.show()
