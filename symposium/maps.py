import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Path to NJ county shape file
nj_counties = gpd.read_file(r"symposium\County_Boundaries_of_NJ\County_Boundaries_of_NJ.shp")
print(nj_counties.head())
print(nj_counties.shape)

# Load the biomass data
biomass_data = pd.read_csv(r"backend\fermentation\biomass_imperial.csv")
biomass_data = biomass_data[biomass_data["County"] != "New Jersey"]
biomass_data["COUNTY"] = biomass_data["County"].str.upper()
print(biomass_data.head())
print(biomass_data.shape)

nj_counties_merged = nj_counties.merge(biomass_data, on='COUNTY')
print(nj_counties_merged.head())
print(nj_counties_merged.shape)

colormap = plt.get_cmap("YlOrRd")  # Adjust 'YlOrRd' for your preference

fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size as needed
nj_counties_merged.plot(column='Annual Ethanol (gal/yr)', cmap=colormap, ax=ax, legend=True)

# Add title, labels, etc.
plt.title("NJ County Annual Ethanol Production (gal/yr)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()


fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size as needed
nj_counties_merged.plot(column='Annual Ethanol (gal/yr)', cmap=colormap, ax=ax, legend=True)

# Add title, labels, etc.
plt.title("NJ County Annual Ethanol Production (gal/yr)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
