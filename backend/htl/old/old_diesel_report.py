import pandas as pd
import requests
from io import BytesIO 
import os
import pdfplumber

# URL of the PDF file on the web
pdf_url = 'https://dep.nj.gov/wp-content/uploads/dwq/sludgeproductiondata2021.pdf'
pdf_path = r'backend\htl\sludgeproductiondata2021.pdf'

# Use requests to get the PDF file
response = requests.get(pdf_url)
dataframes = []

def clean_df(df):
    """
    Clean the dataframe by:
    - Removing rows and columns with all NaN and None values
    - After reaching any rows that don't start with the district name, remove all rows after that
    - After this, replace all the \n with a space
    
    Parameters:
    df (pd.DataFrame): The dataframe to clean
    """
    
    # Print all the columns
    
    district_name = df.iloc[0, 0]
    print(f"District Name: {district_name}")
    indices_of_rows_to_remove = []
    for i, row in df.iterrows():
        if row.iloc[0] != district_name or row.iloc[0] == 'None':
            indices_of_rows_to_remove.append(i)

    df.drop(indices_of_rows_to_remove, inplace=True) # Remove rows after the district name
    df.dropna(how='all', inplace=True) # Remove rows with all NaN values
    # Identify columns with None as the header
    columns_to_drop = [col for col in df.columns if col is None]

    # Drop these columns from the DataFrame
    df.drop(columns=columns_to_drop, inplace=True)    
    
    # Replace all \n with a space in the DataFrame
    df.columns = df.columns.str.replace('\n', ' ', regex=True)
    df.replace(to_replace='\n', value=' ', regex=True, inplace=True)
                
    return df
    
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages[7:37]): # Only these pages contain the required content
        print(f"\nProcessing page {i+8} of {len(pdf.pages)}")
        try:
            # Extract tables from page
            tables = page.extract_tables()
            for table in tables:
                if table:
                    df = pd.DataFrame(table[2:], columns=table[1]) # Create a dataframe from the table data
                    if len(df.columns) > 10: # If the dataframe has more than 10 columns, it's the correct table
                        df = clean_df(df)
                        print(df.shape) # Print the shape of the dataframe, should have 14 columns
                        dataframes.append(df) # Append to the final df
                    
        except Exception as e:
            print(f"\nError on page {i+8}: {e}")
            continue
        
# Combine all the dataframes into one
final_df = pd.concat(dataframes, ignore_index=True)
print(final_df.shape)
print(final_df.head())
print(final_df.tail())
print(final_df.columns)
        
# Save the final dataframe to a CSV file
final_df.to_csv(r'backend\htl\old\old_sludge_production_data.csv', index=False)

def get_county_data(df):
    """
    Takes the data from the dataframe and returns a dataframe of the county data:
    - Scrapes the existing flow mgd from each county 
    - Totals each county's flow mgd
    - Stores the data into a new dataframe with the county name and the total flow mgd

    Parameters:
    df (pd.DataFrame): The dataframe to scrape the county, which is the sludge_production_data.csv
    """
    
    # Create a new dataframe to store the county data
    county_data = pd.DataFrame(columns=['County', 'Flow MGD'])
    
    # Traverse through the data
    for i, row in df.iterrows():
        county = row['COUNTY']
        flow_mgd = float(row['EXISTING FLOW (MGD)'])
        
        # Check if the county is already in the dataframe
        if county in county_data['County'].values:
            # Add the flow mgd to the existing flow mgd
            county_data.loc[county_data['County'] == county, 'Flow MGD'] += flow_mgd
        else:
            # Add the county and flow mgd to the dataframe
            new_row = pd.DataFrame({'County': county, 'Flow MGD': flow_mgd}, index=[0])
            county_data = pd.concat([county_data, new_row], ignore_index=True)
            
    return county_data

final_county_data = get_county_data(final_df)
# I want to add a last row with the county name "New Jersey" and the total flow mgd
new_row = pd.DataFrame({'County': 'New Jersey', 'Flow MGD': final_county_data['Flow MGD'].sum()}, index=[0])
# Add the new row to the final county data
final_county_data = pd.concat([final_county_data, new_row], ignore_index=True)
print(final_county_data.shape)
print(final_county_data.head())
print(final_county_data.tail())
print(final_county_data.columns)

# Save the final county data to a CSV file
final_county_data.to_csv(r'backend\htl\old\old_sludge_production_county_data.csv', index=False)