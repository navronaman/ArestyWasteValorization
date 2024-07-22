import plotly.express as px
import json

# Load the GeoJSON file for New Jersey counties
with open(r'symposium\counties.geojson') as f:
    counties_geojson = json.load(f)

# Create a simple map using the GeoJSON file
fig = px.choropleth(
    geojson=counties_geojson,
    locations=[feature["properties"]["COUNTY"] for feature in counties_geojson["features"]],
    featureidkey="properties.COUNTY",
    title="Map of New Jersey Counties"
)

# Set the geographical center and zoom level to focus on New Jersey
fig.update_geos(
    center={"lat": 40.0583, "lon": -74.4057},  # Center on New Jersey
    projection_scale=7,  # Adjust this value as needed
    visible=False
)

# Show the plot
fig.show()
