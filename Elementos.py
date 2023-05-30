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

servicios = {'1.9':'//*[@id="MainContent_cboyn_art_retention"]',
             '1.40':'//*[@id="MainContent_cboOtherWashMaterialDistribution"]',
             '5.9':'//*[@id="MainContent_cboFoodDeliveryservice"]'}

donante = {'1.40':'//*[@id="MainContent_cboOtherWashMaterialDistribution_dnr"]',
           '5.9':'//*[@id="MainContent_cboFoodDeliveryservice_dnr"]'}

dominio = {'Salud':'//*[@id="MainContent_mainPanal"]/a[3]',
           'Fortalecimiento':'//*[@id="MainContent_mainPanal"]/a[7]'}

guardar = {'Salud':'//*[@id="MainContent_btnsaveHealth"]',
           'Fortalecimiento':'//*[@id="MainContent_btnsave"]',}