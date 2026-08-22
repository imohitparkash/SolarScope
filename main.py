import logging
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from astropy.coordinates import get_body_barycentric, solar_system_ephemeris
from astropy.time import Time
import astropy.units as u

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
solar_system_ephemeris.set('builtin')

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
        "distance_lunar_distance": round(distance.to(u.km).value / 384400, 4)
    }

@app.get("/api/health")
def health_check(response: Response):
    try:
        now = Time.now()
        get_body_barycentric('earth', now)
        return {"status": "ok", "checked_at": now.isot}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        response.status_code = 503
        return {"status": "error"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")