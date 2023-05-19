import pandas as pd

# Origen de información

fam_salidas = pd.read_csv('Archivos\FamSalidas.csv', delimiter = ';', index_col = 'Hogar')['ID'].tolist()
ben_salidos = pd.read_csv('Archivos\BenSalidos.csv', delimiter = ';', index_col = 'Ben')['ID'].tolist()
XPATH = pd.read_csv('Archivos\XPATH.csv', delimiter = ";", index_col = "ID",)
HOGAR = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Hogar'].tolist()
FECHA = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['FechaVisita'].tolist()
MOTIVO = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['MotivoVisita'].tolist()
LUGAR = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['EntregaEn'].tolist()
CUIDADOR = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Idcare'].tolist()