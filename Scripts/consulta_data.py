from pandasql import sqldf as sql
import pandas as pd

columnas_ordenadas = ['CP', 'COLONIA', 'TIPO_ASENTAMIENTO', 'MUNICIPIO_ALCALDIA', 'ESTADO', 'CIUDAD', 'DEST_CORREO',
                      'CLAVE_EDO', 'DEST_CORREO_bis', 'c_CP', 'CLAVE_ASENT', 'CLAVE_MUNI', 'ID_ASENTAM', 'TIPO_ZONA',
                      'CLAVE_CIUDAD']

class Consultor:
    def __init__(self):
        self.carga_tablas()

    def carga_tablas(self):
        self.estados = pd.read_csv('Datos/estados.csv', encoding='cp1252', dtype='str')
        self.estados.fillna('', inplace=True)
        self.municipios = pd.read_csv('Datos/municipios.csv', encoding='cp1252', dtype='str')
        self.municipios.fillna('', inplace=True)
        self.colonias = pd.read_csv('Datos/colonias.csv', encoding='cp1252', dtype='str')
        self.colonias.fillna('', inplace=True)

    def from_estado(self, estado):
        # data = sql(f"select * from self.estados where ESTADO == '{estado}'")
        data = self.estados[self.estados['ESTADO'].str.upper() == estado.upper()]
        # Realiza los cruces con las demas tablas
        data = data.merge(self.municipios, how='inner', left_on=['CLAVE_EDO', 'CLAVE_MUNI', 'ID_ASENTAM'], right_on=['CLAVE_EDO', 'CLAVE_MUNI', 'ID_ASENTAM'])
        data = data.merge(self.colonias, how='inner', left_on=['CP', 'ID_ASENTAM'], right_on=['CP', 'ID_ASENTAM'])

        # print(data[columnas_ordenadas])
        return data[columnas_ordenadas].to_json(orient="table")

    def from_municipio(self, municipio):
        # data = sql(f"select * from self.estados where ESTADO == '{estado}'")
        data = self.municipios[self.municipios['MUNICIPIO_ALCALDIA'].str.upper() == municipio.upper()]
        # Realiza los cruces con las demas tablas
        data = data.merge(self.estados, how='inner', left_on=['CLAVE_EDO', 'CLAVE_MUNI', 'ID_ASENTAM'], right_on=['CLAVE_EDO', 'CLAVE_MUNI', 'ID_ASENTAM'])
        data = data.merge(self.colonias, how='inner', left_on=['CP', 'ID_ASENTAM'], right_on=['CP', 'ID_ASENTAM'])

        # print(data[columnas_ordenadas])
        return data[columnas_ordenadas].to_json(orient="table")

    def from_colonia(self, colonia):
        # data = sql(f"select * from self.estados where ESTADO == '{estado}'")
        data = self.colonias[self.colonias['COLONIA'].str.upper() == colonia.upper()]
        # Realiza los cruces con las demas tablas
        data = data.merge(self.municipios, how='inner', left_on=['CP', 'ID_ASENTAM'], right_on=['CP', 'ID_ASENTAM'])
        data = data.merge(self.estados, how='inner', left_on=['CLAVE_EDO', 'CLAVE_MUNI', 'ID_ASENTAM'], right_on=['CLAVE_EDO', 'CLAVE_MUNI', 'ID_ASENTAM'])

        # print(data[columnas_ordenadas])
        return data[columnas_ordenadas].to_json(orient="table")

    def from_cp(self, cp):
        # data = sql(f"select * from self.estados where ESTADO == '{estado}'")
        data = self.colonias[self.colonias['CP'].str.upper() == cp.upper()]
        # Realiza los cruces con las demas tablas
        data = data.merge(self.municipios, how='inner', left_on=['CP', 'ID_ASENTAM'], right_on=['CP', 'ID_ASENTAM'])
        data = data.merge(self.estados, how='inner', left_on=['CLAVE_EDO', 'CLAVE_MUNI', 'ID_ASENTAM'], right_on=['CLAVE_EDO', 'CLAVE_MUNI', 'ID_ASENTAM'])

        # print(data[columnas_ordenadas])
        return data[columnas_ordenadas].to_json(orient="table")
