import plotly.express as px # For plotting the New Jersey county map
import pandas as pd # For reading the data
import json # For reading the GeoJSON file

# Read the data
df = pd.read_csv(r"backend\fermentation\biomass_imperial.csv")

# Capitalize the each word in the 'County' column
df['County'] = df['County'].str.upper()

print(df.head())    # Print the first 5 rows of the data

# Read the GeoJSON file
with open(r'symposium\counties.geojson') as f:
    counties_geojson = json.load(f)
    
# Check if the GeoJSON file works
# print(counties_geojson['features'][0]) # Print the first feature in the GeoJSON file
print(json.dumps(counties_geojson['features'][0], indent=4)) # Print the GeoJSON file with indentation

# Plot the New Jersey county map
fig = px.choropleth(
    df, # Data
    geojson=counties_geojson, # GeoJSON file
    locations="County", # Column in the data that contains the county names
    featureidkey="properties.COUNTY", # Key in the GeoJSON file that contains the county names
    color="Price ($/gal)", # Column in the data that contains the biomass values
    color_continuous_scale="Viridis", # Color scale
    scope="usa", # Scope of the map
    title="Price of Ethanol by Fermentation in New Jersey") # Title of the map

# Set the geographical center and zoom level to focus on New Jersey
fig.update_geos(
    center={"lat": 40.0583, "lon": -74.4057},  # Center on New Jersey
    projection_scale=7,  # Adjust this value as needed
    visible=False
)

# Update the layout for better visualization
# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.show() # Show the map
