import pandas as pd
from backend.htl.old.old_liquefication import htl_calc

df = pd.read_csv(r"backend\htl\sludge_production_county_data.csv")

# New Columns to be added
df["Flow m3/d"] = 0 # For daily sludge supply in an alternative unit

# Different price units
df["Price ($/gal)"] = 0
df["Price ($/kg)"] = 0
df["Price ($/m3)"] = 0
df["Price ($/MMBTU)"] = 0
df["Price ($/MJ)"] = 0

# Different GWP units
df["GWP (lb CO2e/gal)"] = 0
df["GWP (kg CO2e/kg)"] = 0
df["GWP (kg CO2e/m3)"] = 0
df["GWP (kg CO2e/MMBTU)"] = 0
df["GWP (kg CO2e/MJ)"] = 0

print(df.head()) # Print the first 5 rows of the dataframe

# Conversion factors
galToM3 = 0.00378541
kgToLbsConversion = 2.20462
galToMMBTUConversion = 0.12845
galToKg = 0.838*3.78541
BTUToMJ = 0.00105506

# Traverse every row in the df
for index, row in df.iterrows():
    
    print(f"\nProcessing row {index+1} of {len(df)}")
    
    flow_mgd = row["Flow MGD"]
    df.at[index, "Flow m3/d"] = flow_mgd * galToM3 * 1e6

    price, gwp = htl_calc(flow_mgd)
    print(f"Price: {price}, GWP: {gwp}")
    df.at[index, "Price ($/gal)"] = price
    df.at[index, "Price ($/kg)"] = price / galToKg # divide by 0.838*3.78541 to get $/kg
    df.at[index, "Price ($/m3)"] = price / galToM3 # divide by 0.00378541 to get $/m3
    df.at[index, "Price ($/MMBTU)"] = price / (galToMMBTUConversion * galToKg) # divide by 0.12845*0.838*3.78541 to get $/MMBTU
    df.at[index, "Price ($/MJ)"] = price / (galToMMBTUConversion * galToKg * BTUToMJ * 1e6) # divide by 0.12845 * 0.838 * 3.78541 * 0.00105506 to get $/MJ
    df.at[index, "GWP (lb CO2e/gal)"] = gwp
    df.at[index, "GWP (kg CO2e/kg)"] = gwp / (kgToLbsConversion*galToKg) # divide by 2.20462*0.838*3.78541 to get kg CO2e/kg
    df.at[index, "GWP (kg CO2e/m3)"] = gwp / (kgToLbsConversion*galToM3) # divide by 2.20462*0.00378541 to get kg CO2e/m3
    df.at[index, "GWP (kg CO2e/MMBTU)"] = gwp / (kgToLbsConversion*galToMMBTUConversion) # divide by 2.20462*0.12845 to get kg CO2e/MMBTU
    df.at[index, "GWP (kg CO2e/MJ)"] = gwp / (kgToLbsConversion * galToMMBTUConversion * BTUToMJ * 1e6) # divide by 2.20462 * 0.12845 * 0.00105506 to get kg CO2e/MJ
    
    print(f"\nRow {index+1} processed")

print(df.head())
print(df.tail())    
df.to_csv(r"backend\htl\sludge_data_final.csv", index=False)

    
    
