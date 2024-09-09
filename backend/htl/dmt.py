"""
What does this file do?

This file extracts the county total from the sludgeproductiondata2021.pdf using pdfplumber.
It then stores that data as a CSV file.
This data would then be used to calculate the dry metric tonnes for each county in the HTL reports.
This data would also be used to in the combustion extraction files.
"""

# Import statements
import pandas as pd
import pdfplumber

# URL of the PDF file on the web - https://dep.nj.gov/wp-content/uploads/dwq/sludgeproductiondata2021.pdf
# We have locally installed it on the repository

pdf_path = r'backend\htl\sludgeproductiondata2021.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # The table that has the content for each county in dry metric tonnes a year is on page 7
    for table in pdf.pages[6].extract_tables():
        if table:
            print("\nRaw Table:")
            print(table)
            print(table[0]) # These are the headers
            print(table[0][0])
            print(table[1]) # This is all the data, we need to split this up based on the '\n' character
            print("First row of data: ")
            print(table[1][0])
            print(type(table[1]))
            print(type(table[1][0]))
            print("Last line of data: ")
            print(table[2]) # This is the last line of the data, we add this later
            df = pd.DataFrame(table[2:], columns=table[1]) # Create a dataframe from the table data
            print("Dataframe:")
            print(df)
            print(df.columns)
            print(df.shape)
            
            