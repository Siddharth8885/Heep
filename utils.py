def haversine_km(lat1, lon1, lat2, lon2):
  from math import radians, sin, cos, atan2
  R = 6371.0
  phi1, phi2 = radians(lat1), radians(lat2)
  dphi = radians(lat2 - lat1); dlambda = radians(lon2 - lon1)
  a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
  c = 2*atan2(a**0.5, (1-a)**0.5)
  return R*c
