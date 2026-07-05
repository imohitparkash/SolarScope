from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from astropy.coordinates import get_body_barycentric, solar_system_ephemeris
from astropy.time import Time
import astropy.units as u

solar_system_ephemeris.set('builtin')

app = FastAPI()

# AU (Astronomical Unit) = average Earth-Sun distance (~150 million km).
# Used as the standard "ruler" for solar-system-scale distances.
@app.get("/api/sun")
def get_sun_distance():
    now = Time.now()
    earth_pos = get_body_barycentric('earth', now)
    sun_pos = get_body_barycentric('sun', now)
    distance_vector = earth_pos - sun_pos
    distance = distance_vector.norm()
    return {
        "distance_km": round(distance.to(u.km).value, 0),
        "distance_miles": round(distance.to(u.imperial.mile).value, 0),
        "distance_au": round(distance.to(u.AU).value, 6)
    }

# LD (Lunar Distance) = average Earth-Moon distance (~384,400 km).
# The Moon's orbit isn't a perfect circle, so real distance drifts
# slightly above/below 1 LD across the month.
@app.get("/api/moon")
def get_moon_distance():
    now = Time.now()
    earth_pos = get_body_barycentric('earth', now)
    moon_pos = get_body_barycentric('moon', now)
    distance_vector = earth_pos - moon_pos
    distance = distance_vector.norm()
    return {
        "distance_km": round(distance.to(u.km).value, 0),
        "distance_miles": round(distance.to(u.imperial.mile).value, 0),
        # AU is way too big a unit for Moon distance, so we skip it here
        # and give a smaller, more readable unit instead
        "distance_lunar_distance": round(distance.to(u.km).value / 384400, 4)
    }

app.mount("/", StaticFiles(directory="static", html=True), name="static")

