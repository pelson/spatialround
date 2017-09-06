"""
Compute the

.. plot:: examples/distance_plot.py
   :include-source:

"""


import numpy as np
import pyproj


_WGS84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
_GEOCENTRIC = pyproj.Proj('+proj=geocent +datum=WGS84 +units=m +no_defs')
_GEOD = pyproj.Geod(ellps='WGS84')


def round(points, distance=5000):
    """
    Round the given spatial points to the nearest distance (m).

    Parameters
    ----------
    points : array-like
        The point to be rounded, in the shape ``(2, N)``, with axis=0 being the
        longitude, latitude pairs (in that order).
    distance : number
        The distance, in meters, to round the points to. This is an
        approximation, but serves as an upper bound to the rounding distance.
        See the README for algorithm details.

    """
    x, y, z = pyproj.transform(_WGS84, _GEOCENTRIC,
                               points[0], points[1],
                               np.full(points[0].shape, 32000))

    fac = distance
    x, y, z = (_round_to_nearest(x, fac),
               _round_to_nearest(y, fac),
               _round_to_nearest(z, fac))

    lons, lats, _ = pyproj.transform(_GEOCENTRIC, _WGS84, x, y, z)
    rounded_points = np.stack([lons, lats])
    return rounded_points


def _n_decimals(a):
    """
    Calculate how many digits the given integer has.

    >>> n_decimals([1, 9, 10, 11, 99, 100, 101, 1001, 100001312])
    array([1, 1, 2, 2, 2, 3, 3, 4, 9])

    """
    return np.ceil(np.log10(np.asanyarray(a) + 1)).astype(np.int)


def _round_to_nearest(a, nearest=1):
    """
    Round the given values to the nearest given integer value.

    >>> round_to_nearest([-60, -40, 20, 30, 1226], 50)
    array([ -50,  -50,    0,   50, 1250])

    >>> round_to_nearest([-7, 2, 14, 136, 149], 13.5)
    array([ -13.5,    0. ,   13.5,  135. ,  148.5])

    """
    # Note: Algorithm slightly more complex than
    # np.around(a / nearest) * nearest to try to preserve some more accuracy
    # (I have no evidence to suggest this is actually necessary).
    a = np.asanyarray(a)
    nearest = np.array(nearest)
    nearest_mag = _n_decimals(nearest)
    offset = (10 ** (nearest_mag - 1))
    nearest_scaled = nearest / (10 ** (nearest_mag - 1))
    rounded = np.around(a / offset / nearest_scaled) * nearest_scaled * offset
    return rounded.astype(nearest.dtype)


if __name__ == '__main__':
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
    # Round within 1.25km
    round_distance = 1250
    new_points = round(points, round_distance)
    _, _, dist = _GEOD.inv(points[0], points[1], new_points[0], new_points[1])

    plt.figure(figsize=(10, 5))
    plt.title('Rounded distance (@{}m) from original point'
              ''.format(round_distance))
    plt.contourf(x, y, dist, 10)
    plt.colorbar(label='Distance / meters')
    plt.show()
