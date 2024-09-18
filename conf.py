#conf.py
from zoneinfo import ZoneInfo

import numpy as np
from astropy.coordinates import EarthLocation
import astropy.units as u

TIME_ZONE = ZoneInfo("Asia/Kolkata")
LAT = "Enter Latitude from viewing area"
LONG = "Enter Longitude of viewing area"
HEIGHT = "Enter Elevation of viewing area"
location = EarthLocation(lat = LAT * u.deg, lon = LONG * u.deg, height = HEIGHT * u.m)

NAIVE_VIEWING_TIMES = np.linspace(-3, 10, 100) * u.hour

