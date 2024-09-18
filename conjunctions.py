#conjunctions.py
import warnings
from datetime import date, timedelta

from astropy import coordinates
from astropy.time import Time
import astropy.units as u

import pandas as pd
from tabulate import tabulate
from conf import location

OBSERVATION_COUNT = 100
DAY_INTERVAL = 7

REF_PLANET = 'mercury'
PLANETS = ['venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

df = pd.DataFrame([], columns=['TS'] + PLANETS)
df.set_index("TS", inplace=True)

now = date.today()
for num in range(0, OBSERVATION_COUNT):
    when = now + timedelta(days=num * DAY_INTERVAL)

    row = {
        "TS": [when]
    }
    for planet in PLANETS:
        astro_when = Time(when.strftime("%Y-%m-%d 00:00:00"))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            ref = coordinates.get_body(REF_PLANET, astro_when, location)
            target = coordinates.get_body(planet, astro_when, location)
            angle = coordinates.angular_separation(ref.ra.rad, ref.dec.rad, target.ra.rad,
                                                   target.dec.rad)
        angle = angle * u.rad.to(u.deg)
        row[planet] = [angle]

    row_df = pd.DataFrame(row)
    row_df.set_index("TS", inplace=True)
    df = pd.concat([df, row_df])

count = df.iloc[:, 1:].le(7, axis=0).sum(axis=1)
df = df.assign(count=count)

# Display
print("\n\n")
table = tabulate(df.loc[count > 1], tablefmt="plain", headers=df.columns, floatfmt=".0f")
print(table)
