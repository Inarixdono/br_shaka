
import pandas as pd
import pyperclip as ctrl

# Origen de información

fam_salidas = pd.read_csv('Archivos\FamSalidas.csv', delimiter = ';', index_col = 'Hogar')['ID'].tolist()
ben_salidos = pd.read_csv('Archivos\BenSalidos.csv', delimiter = ';', index_col = 'Ben')['ID'].tolist()
XPATH = pd.read_csv('Archivos\XPATH.csv', delimiter = ";", index_col = "ID",)
Servir = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)
