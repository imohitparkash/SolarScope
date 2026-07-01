from astropy.coordinates import get_body_barycentric, solar_system_ephemeris
from astropy.time import Time
import astropy.units as u

solar_system_ephemeris.set('builtin')

now = Time.now()

earth_pos = get_body_barycentric('earth', now)
sun_pos = get_body_barycentric('sun', now)

distance_vector = earth_pos - sun_pos
distance = distance_vector.norm()

distance_km = distance.to(u.km)
distance_miles = distance.to(u.imperial.mile)   

print(f"Distance from Earth to Sun right now: {distance_km:.0f}")
print(f"In miles: {distance_miles:.0f}")         
print(f"In AU: {distance.to(u.AU):.6f}")