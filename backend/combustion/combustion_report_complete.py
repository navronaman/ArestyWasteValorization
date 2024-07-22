import pandas as pd # Read the data
from combustion import combustion_county # Import the combustion_county function

df = pd.read_csv(r"backend\combustion\combustion_data.csv")

# Create a column for the total food waste
list_of_wastes = ["sludge", "food", "fog", "green", "manure"]

for waste in list_of_wastes:
    df[f"{waste.title()} Mass kg/hr"] = 0
    df[f"{waste.title()} Electricity (MWH)"] = 0
    df[f"{waste.title()} Avoided Emissions (million metric tonnes)"] = 0
    df[f"{waste.title()} Avoided Emissions Percentage"] = 0


print(df.head())    
# Traverse every row in the df
for index, row in df.iterrows():
    county = row["County"]
    for waste in list_of_wastes:
        name, waste_type, mass, electricity, avoided_emissions, avoided_emissions_percentage = combustion_county(county, waste)
        df.at[index, f"{waste.title()} Mass kg/hr"] = mass
        df.at[index, f"{waste.title()} Electricity (MWH)"] = electricity
        df.at[index, f"{waste.title()} Avoided Emissions (million metric tonnes)"] = avoided_emissions
        df.at[index, f"{waste.title()} Avoided Emissions Percentage"] = avoided_emissions_percentage

print(df.head())
    
df.to_csv(r"backend\combustion\combustion_data_final.csv", index=False)

# Now we will conduct data analysis on the data using Google Colab