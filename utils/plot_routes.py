# utils/plot_routes.py
import requests
import datetime as dt
import folium
import polyline

# Google Maps Routes API endpoint
ROUTES_ENDPOINT = "https://routes.googleapis.com/directions/v2:computeRoutes"
# Replace with your actual API key or set it as an environment variable
API_KEY = "YOUR_API_KEY"

# Helper to build origin/destination payload
def origin_dest_payload(token: str):
    token = token.strip()
    if token.lower().startswith("placeid:"):
        return {"placeId": token.split(":", 1)[1]}
    # Assume lat,lng format
    lat, lng = token.split(",", 1)
    return {"location": {"latLng": {"latitude": float(lat), "longitude": float(lng)}}}

# Function to get routes from origin to destination
def get_routes(origin, destination, API_KEY=API_KEY):
    # Prepare request headers and body
    headers = {
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }
    body = {
        "origin": origin_dest_payload(origin),
        "destination": origin_dest_payload(destination),
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
        "departureTime": {"seconds": int(dt.datetime.now(dt.UTC).timestamp())},
        "computeAlternativeRoutes": True
    }

    # Make the POST request to the Routes API
    resp = requests.post(ROUTES_ENDPOINT, headers=headers, json=body, timeout=30)
    resp.raise_for_status()
    return resp.json()

# Function to plot routes on a map and save as HTML
def plot_routes(data, output="mapa.html"):
    routes = data.get("routes", [])
    if not routes:
        raise ValueError("Nenhuma rota retornada")

    # Create a folium map centered at the start of the first route
    first_polyline = routes[0]["polyline"]["encodedPolyline"]
    first_coords = polyline.decode(first_polyline)
    m = folium.Map(location=first_coords[0], zoom_start=12)

    # Add each route to the map with different colors
    colors = ["blue", "green", "red"]
    for i, r in enumerate(routes):
        enc = r["polyline"]["encodedPolyline"]
        coords = polyline.decode(enc)
        # Add polyline to the map
        folium.PolyLine(coords, color=colors[i % len(colors)], weight=5, opacity=0.7,
                        tooltip=f"Rota {i+1}: ETA {r['duration']} / static {r['staticDuration']}").add_to(m)

    m.save(output)
    print(f"Mapa salvo em {output}")

if __name__ == "__main__":
    # You can replace these with actual place IDs using the https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder
    origin = "placeid:YOUR_ORIGIN_PLACE_ID"
    destination = "placeid:YOUR_DESTINATION_PLACE_ID"

    # Get route data
    data = get_routes(origin, destination)
    plot_routes(data)
