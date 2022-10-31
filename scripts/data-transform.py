from token import RARROW
from tabula import read_pdf
import PyPDF2
import pandas as pd
import numpy as np

def format_data(df: pd.DataFrame):
    # padronize nan values
    df.fillna('NO VALUE', inplace=True)

    # check for breakline in value
    df_headers = df.columns
    for index, row in df.iterrows():            
        for col in df_headers:
            if '\r' in str(row[col]):
                row.replace(row[col], row[col].replace('\r', ' '), inplace=True)
        
file_path = '/home/marcosvn/Documents/intuitive-care/scripts/Anexo1.pdf'

# getting total number of pages
file = open(file_path, 'rb')
readpdf = PyPDF2.PdfFileReader(file)
totalPages = readpdf.numPages

# getting first table from pdf and transforming into dataframe
main_df = pd.DataFrame(read_pdf(file_path, pages=3)[0])

# removing any break lines from df's headers
main_df.columns = [col.replace('\r', ' ') for col in main_df.columns.to_list()]
format_data(main_df)

main_df.to_csv('out.csv')