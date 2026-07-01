from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from astropy.coordinates import get_body_barycentric, solar_system_ephemeris
from astropy.time import Time
import astropy.units as u

solar_system_ephemeris.set('builtin')

app = FastAPI()

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
app.mount("/", StaticFiles(directory="static", html=True), name="static")