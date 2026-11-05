"""Utility helpers for the ``core`` app."""
from math import asin, cos, radians, sin, sqrt

#: Mean Earth radius in kilometres.
EARTH_RADIUS_KM = 6371.0


def haversine_distance(lat1, lng1, lat2, lng2):
    if None in (lat1, lng1, lat2, lng2):
        return None

    phi1, phi2 = radians(lat1), radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lng2 - lng1)

    a = (
        sin(delta_phi / 2) ** 2
        + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
    )
    c = 2 * asin(sqrt(a))

    return EARTH_RADIUS_KM * c
