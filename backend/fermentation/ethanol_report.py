from lignocellulose import lignocellulose_calc
import pandas as pd
"""
We are going to use the data from https://ecocomplex.rutgers.edu/biomass-energy-potential.html 
for our reports in this.
Let's look at the lignocellulose data for New Jersey from slide 34 of this presentation:
This is based on current gross quantity of dry tons based on estimated lignocellulosic biomass

New Jersey: 2,124,461
Atlantic: 118,397
Bergen: 93,737
Burlington: 214,810
Camden: 73,270
Cape May: 90,167
Cumberland: 128,487
Essex: 40,659
Gloucester: 81,807
Hudson: 4,129
Hunterdon: 134,938
Mercer: 119,709
Middlesex: 73,388
Monmouth: 125,283
Morris: 113,251
Ocean: 158,073
Passaic: 57,969
Salem: 118,525
Somerset: 50,999
Sussex: 151,081
Union: 36,023
Warren: 139,757
"""

ETHANOL_DENSITY_KG_GAL_CONVERSION = 2.98668849

def imperial(data):
    data["Kilogram"] = data["Lignocellulose (dry tons)"] * 907.185
    data["Kilogram/hr"] = data["Kilogram"] / (365*24*0.96)
    data["Annual Ethanol (gal/yr)"] = None
    data["Price ($/gal)"] = None
    data["GWP (kg CO2e/gal)"] = None
    print(data)

    # Traverse throught the data and calculate the annual ethanol price and GWP
    for i in range(len(data)):
        print(f"\n{data['County'][i]} County")
        print(f"Annual estimated lignocellulose in dry tons: {data['Lignocellulose (dry tons)'][i]}")
        ethanol, price, gwp = lignocellulose_calc(data['Kilogram/hr'][i])
        data["Annual Ethanol (gal/yr)"][i] = ethanol
        data["Price ($/gal)"][i] = price
        data["GWP (kg CO2e/gal)"][i] = gwp
        
    print(data)
    # Export data into an updated data csv
    data.to_csv(r'backend\fermentation\biomass_imperial.csv', index=False)
        
def metric(data):
    data["Lignocellulose (metric tonnes)"] = data["Lignocellulose (dry tons)"] * (907.185/1000)
    data["Kilogram"] = data["Lignocellulose (dry tons)"] * 907.185
    data["Kilogram/hr"] = data["Kilogram"] / (365*24*0.96)
    data["Annual Ethanol (kg/yr)"] = None
    data["Price ($/kg)"] = None
    data["GWP (kg CO2e/kg)"] = None
    
    for i in range(len(data)):
        print(f"\n{data['County'][i]} County")
        print(f"Annual estimated lignocellulose in tonnes: {data['Lignocellulose (metric tonnes)'][i]}")
        ethanol, price, gwp = lignocellulose_calc(data['Kilogram/hr'][i])
        data["Annual Ethanol (kg/yr)"][i] = ethanol * ETHANOL_DENSITY_KG_GAL_CONVERSION
        data["Price ($/kg)"][i] = price / ETHANOL_DENSITY_KG_GAL_CONVERSION
        data["GWP (kg CO2e/kg)"][i] = gwp / ETHANOL_DENSITY_KG_GAL_CONVERSION
        
    print(data)
    # Export data into an updated data csv
    data.to_csv(r'backend\fermentation\biomass_metric.csv', index=False)

if __name__ == '__main__':
    data1 = pd.read_csv(r'backend\fermentation\biomass_data.csv')
    data2 = data1.copy()
    imperial(data1)
    metric(data2)