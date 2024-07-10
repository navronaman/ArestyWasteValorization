import pandas as pd

dfs = pd.read_excel(r"backend\combustion\data.xlsx", sheet_name=None)

green_data = pd.read_csv(r"backend\fermentation\biomass_data.csv")

county_names = green_data["County"].tolist()
county_greens = green_data["Lignocellulose (dry tons)"].tolist()



food_tons = []
food_dry_tons = []
fog_tons = []
fog_dry_tons = []

for index, county_name in enumerate(county_names):
    try:
        print(f"{index+1}: \nCounty Name: {county_name}")
        
        # append the food waste data to the food_tons list
        food_tons.append(dfs[county_name].iloc[130]["Unnamed: 1"])
        food_dry_tons.append(dfs[county_name].iloc[130]["Unnamed: 2"])

        # append the fog waste data to the fog_tons list, add both
        # the food and fog waste data to the DataFrame
        fog_tons.append(dfs[county_name].iloc[131]["Unnamed: 1"] + dfs[county_name].iloc[132]["Unnamed: 1"])
        fog_dry_tons.append(dfs[county_name].iloc[131]["Unnamed: 2"] + dfs[county_name].iloc[132]["Unnamed: 2"])

    except KeyError:
        food_tons.append(0) # if the county name is not found, append 0 to the food_tons list
        food_dry_tons.append(0) # if the county name is not found, append 0 to the food_dry_tons list
        fog_tons.append(0) # if the county name is not found, append 0 to the fog_tons list
        fog_dry_tons.append(0) # if the county name is not found, append 0 to the fog_dry_tons list
        continue
    
data = {
    "County": county_names,  
    "Sludge": 0 * len(county_names),  # Sludge left to be found
    "Food (tons)": food_tons,
    "Food (dry tons)": food_dry_tons,
    "Fog (tons)": fog_tons,
    "Fog (dry tons)": fog_dry_tons,
    "Green": county_greens,
    "Manure": 0 * len(county_names), # Manure left to be found
}

df = pd.DataFrame(data)

print(df.head())  # Display the first few rows of the DataFrame
df.to_csv(r"backend\combustion\combustion_data.csv", index=False)  # Save the DataFrame to a CSV file