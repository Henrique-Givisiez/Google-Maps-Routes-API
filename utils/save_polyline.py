# save_polylines.py
import json
from plot_routes import get_routes

# Define origin and destination
# Replace with your actual Place IDs using the https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder
origin = "placeid:YOUR_ORIGIN_PLACE_ID"
destination = "placeid:YOUR_DESTINATION_PLACE_ID"

# Get routes data
data = get_routes(origin, destination, API_KEY="YOUR_API_KEY")

# Extract and save polylines to a JSON file
polylines = []
for i, route in enumerate(data.get("routes", []), 1):
    polyline = route.get("polyline", {}).get("encodedPolyline")
    if polyline:
        polylines.append(polyline)
        print(f"Rota {i} capturada (polyline={polyline[:30]}...)")

# Save polylines to a JSON file
with open("my_routes.json", "w") as f:
    json.dump(polylines, f, indent=2)
