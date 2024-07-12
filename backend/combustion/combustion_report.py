import pandas as pd

dfs = pd.read_excel(r"backend\combustion\data.xlsx", sheet_name=None)

green_data = pd.read_csv(r"backend\fermentation\biomass_data.csv")

sludge_data = pd.read_csv(r"backend\htl\sludge_production_county_data.csv")

county_names = green_data["County"].tolist()[:-1] # Not including New Jersey
county_greens = green_data["Lignocellulose (dry tons)"].tolist()[:-1] # Not including New Jersey
county_sludge = sludge_data["Flow MGD"].tolist() # Only because this sludge data does not have New Jersey


food_tons = []
food_dry_tons = []

fog_tons = []
fog_dry_tons = []

manure_lbs = []

for index, county_name in enumerate(county_names):
    try:
        print(f"{index+1}: \nCounty Name: {county_name}")
        
        # append the food waste data to the food_tons list
        food_tons.append(dfs[county_name].iloc[130]["Unnamed: 1"]) # this is in tons
        food_dry_tons.append(dfs[county_name].iloc[130]["Unnamed: 2"]) # this is in tons

        # append the fog waste data to the fog_tons list, add both
        # the food and fog waste data to the DataFrame
        fog_tons.append(dfs[county_name].iloc[131]["Unnamed: 1"] + dfs[county_name].iloc[132]["Unnamed: 1"]) # this is in tons
        fog_dry_tons.append(dfs[county_name].iloc[131]["Unnamed: 2"] + dfs[county_name].iloc[132]["Unnamed: 2"]) # this is in tons
        
        # for manure
        manure_lbs.append(dfs[county_name].iloc[119]["Unnamed: 3"]) # this is in lbs

    except KeyError:
        print(f"County Name: {county_name} not found in the combustion data")
        continue
    
print(len(county_names), len(county_greens), len(county_sludge), len(food_tons), len(food_dry_tons), len(fog_tons), len(fog_dry_tons), len(manure_lbs))
data = {
    "County": county_names,  
    "Sludge": county_sludge,  # Sludge left to be found
    "Food (tons)": food_tons,
    "Food (dry tons)": food_dry_tons,
    "Fog (tons)": fog_tons,
    "Fog (dry tons)": fog_dry_tons,
    "Green": county_greens,
    "Manure": manure_lbs, # Manure left to be found
}

df = pd.DataFrame(data)

print(df.head())  # Display the first few rows of the DataFrame
df.to_csv(r"backend\combustion\combustion_data.csv", index=False)  # Save the DataFrame to a CSV file