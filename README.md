# Spatial-Rounding

Round a spatial (longitude & latitude) coordinate to the nearest physical distance.

For example, given a latitude of 40.7127 and a longitude of -74.0059, rounding this to the nearest 500km produces a latitude of ??? and a longitude of ???, which turns out to be ???km away from the original point.


# Algorithm

In order to compute the rounding, we convert the coordinate into 3d cartesian space (meters), and round each coordinate to ``rounding_distance^-3``, and then
convert the rounded coordinate back to latitudes and longitudes.

This approach allows us to put an upper-bound on the rounding radius, although in practice it will often result in rounding that is much smaller
than the given ``rounding_distance``. For small ``rounding_distance`` where curvature of the earth has little effect, the actual rounding distance will be
closer to ``rounding_distance ^ (2 / 3)`` (TODO: verify this).


# The ``spatialround`` python package

The algorithm above has been implemented in Python, and can be used in the following manner:

```
import spatialround

new_york = -74.0059, 40.7127

# Round the coordinate to the nearest 500km
ny_rounded = spatialround.round(new_york, distance=5e6)

ny_rounded


# Calculate how far we are actually away from NY using the Vincety formula
import vincety

vincety.distance(new_york, ny_rounded)
```
