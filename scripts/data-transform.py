from tabula import read_pdf

import PyPDF2
import pandas as pd
import shutil
import os

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
output_dir = '/home/marcosvn/Documents/intuitive-care/Teste_Marcos'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# getting total number of pages
file = open(file_path, 'rb')
readpdf = PyPDF2.PdfFileReader(file)
totalPages = readpdf.numPages

# getting first table from pdf and transforming into dataframe
main_df = pd.DataFrame(read_pdf(file_path, pages=3)[0])

# appending every other table in pdf to the main dataframe
for i in range(4, totalPages):
    aux_df = pd.DataFrame(read_pdf(file_path, pages=i)[0])
    main_df = pd.concat([main_df, aux_df], ignore_index=True)

# removing any break lines from df's headers
main_df.columns = [col.replace('\r', ' ') for col in main_df.columns.to_list()]
format_data(main_df)

# extra - replace OD and AMB column values
main_df['OD'] = main_df['OD'].replace(['OD'], 'Seg. Odontológica')
main_df['AMB'] = main_df['AMB'].replace(['AMB'], 'Seg. Ambulatorial')

main_df.to_csv(output_dir+'/Teste_Marcos.csv')

# zip folder
shutil.make_archive('Teste_Marcos', 'zip', output_dir)
# deleting output folder leaving only .zip
shutil.rmtree(output_dir)