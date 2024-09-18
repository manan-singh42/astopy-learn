#optimal_view1.py
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo

from astropy.visualization import astropy_mpl_style, quantity_support
from astropy.coordinates import AltAz, SkyCoord, get_sun, get_body
from astropy.time import Time
import matplotlib.pyplot as plt

from conf import location, NAIVE_VIEWING_TIMES, TIME_ZONE


def get_viewing_times(timezone):
    tomorrow = date.today() + timedelta(days=1)
    midnight = datetime.combine(tomorrow, time())
    midnight = midnight.astimezone(timezone)

    midnight = midnight.astimezone(ZoneInfo("UTC"))
    text = midnight.strftime("%Y-%m-%d %H:%M")
    midnight = Time(text)

    return NAIVE_VIEWING_TIMES + midnight


plt.style.use(astropy_mpl_style)
quantity_support()

if __name__ == "__main__":
    target = input("What is the desired viewing object? ")
    coordinates = SkyCoord.from_name(target)

    viewing_hours = get_viewing_times(TIME_ZONE)
    frame = AltAz(obstime=viewing_hours, location=location)
    target_altazs = coordinates.transform_to(frame)

    fig, (top, bottom) = plt.subplots(2, figsize=(10, 8), sharex=True,
                                      height_ratios=[1, 2])
    fig.suptitle(f"{target} Optimal Viewing")
    plt.subplots_adjust(hspace=0.1)

    plt.plot(NAIVE_VIEWING_TIMES, target_altazs.alt, color="m", label=target)

    sun_coordinates = get_sun(viewing_hours).transform_to(frame)
    moon_altazs = get_body("moon", viewing_hours).transform_to(frame)

    bottom.axhspan(ymin=-18, ymax=0, color="black", alpha=0.1)
    bottom.plot(NAIVE_VIEWING_TIMES, sun_coordinates.alt, linestyle="--", color='r',
             label="Sun")
    bottom.plot(NAIVE_VIEWING_TIMES, moon_altazs.alt, linestyle="-.",
             color="grey", label="Moon")

    bottom.set_xlim(-3, 10)
    bottom.set_ylim(-90, 90)
    bottom.set_xlabel(f"Hours from {TIME_ZONE.key} Midnight")
    bottom.set_ylabel("Altitude")
    bottom.legend()

    target_airmass = target_altazs.secz
    mass_line = top.plot(NAIVE_VIEWING_TIMES, target_airmass, label="Airmass")
    top.set_ylabel("Airmass [Sec(z)]")
    top.legend()

    plt.show()
