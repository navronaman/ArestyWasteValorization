"""
What does this file do?

This file extracts the county total from the sludgeproductiondata2021.pdf using pdfplumber.
It then stores that data as a CSV file.
This data would then be used to calculate the dry metric tonnes for each county in the HTL reports.
This data would also be used to in the combustion extraction files.

By the end of this file: in the CSV file sludge_data_dmt.csv, we would have the following data:
County,Incineration,Class A Beneficial Use,Class B Beneficial Use,Out-Of-State Beneficial Use,Out-Of-State State Disposal,In-State Beneficial Use Landfill Cover,Other DTW,County Total (Dry Metric Tonnes/Year)
Atlantic,8368.0,316.4,0.0,0.0,0.0,0.0,307.3,8991.7
...
Warren,0.0,0.0,0.0,0.0,0.0,0.0,1098.7,1098.7
"""

# Import statements
import pandas as pd
import pdfplumber
import csv

# URL of the PDF file on the web - https://dep.nj.gov/wp-content/uploads/dwq/sludgeproductiondata2021.pdf
# We have locally installed it on the repository

pdf_path = r'backend\htl\sludgeproductiondata2021.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # The table that has the content for each county in dry metric tonnes a year is on page 7
    for table in pdf.pages[6].extract_tables():
        if table:
            print(table[0][0])
            row_data = table[1][0]
            

header_row = "County, Incineration, Class A Beneficial Use, Class B Beneficial Use, Out-Of-State Beneficial Use, Out-Of-State State Disposal, In-State Beneficial Use Landfill Cover, Other DTW, County Total (Dry Metric Tonnes/Year)"
# Header row from the PDF

# We need to work this data, as it all in one line
# Current format: Cape May 0.0 84.0 0.0
row_maybe = row_data.replace(" ", ", ") 
row_maybe = row_maybe.replace("Cape, May", "Cape May")
# New Format: Cape May, 0.0, 84.0, 0.0
print(row_maybe)

# Let's split this big string into a list
rows = row_maybe.splitlines() # Converts the string into a list of strings
rows.insert(0, header_row) # Insert the header row at the beginning of the list
print("\n")
print(type(rows)) # This is a list
print("\n")
print(rows) # This is the list of strings
print("\n")
print(rows[0]) # This is the first element of the list

filename = "backend\\htl\\sludge_data_dmt.csv" # The name of the file that we want to write to

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    for row in rows:
        column = row.split(", ")
        writer.writerow(column)
        
# Now let's add a final row to the CSV file for the county total
# We will sum the values of all the columns for each county
df = pd.read_csv(filename)

totals = df.select_dtypes(include="number").sum()
totals_row = pd.DataFrame([["New Jersey"] + totals.tolist()], columns=df.columns)

df_with_totals = pd.concat([df, totals_row], ignore_index=True)
print(df_with_totals)

df_with_totals.to_csv(filename, index=False) # Save the file without the index column