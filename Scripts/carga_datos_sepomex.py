import pandas as pd
import os

"""
    ===========================================================
    ============== Diccionario de datos =======================
    ===========================================================
    
    ______________________________________________________________________
    CAMPO           | DESCRIPCION                           | ALIAS
    ----------------------------------------------------------------------
    d_codigo        | CP asentamiento                       | CP
    ----------------------------------------------------------------------
    d_asenta        | Nombre asentamiento                   | COLONIA
    ----------------------------------------------------------------------
    d_tipo_asenta   | Tipo asentamiento (CAtalogo SEPOMEX)  | TIPO_ASENTAMIENTO
    ----------------------------------------------------------------------
    D_mnpio         | Nombre municipio                      | MUNICIPIO_ALCALDIA
    ----------------------------------------------------------------------
    d_estado        | Nombre entidad                        | ESTADO
    ----------------------------------------------------------------------
    d_ciudad        | Nombre ciudad                         | CIUDAD
    ----------------------------------------------------------------------
    d_CP            | CP destino del correo                 | DEST_CORREO
    ----------------------------------------------------------------------
    c_estado        | Clave entidad                         | CLAVE_EDO
    ----------------------------------------------------------------------
    c_oficina       | CP destino del correo                 | DEST_CORREO_bis
    ----------------------------------------------------------------------
    c_CP            | ** EMPTY **                           | 
    ----------------------------------------------------------------------
    c_tipo_asenta   | Clave tipo asentamiento               | CLAVE_ASENT
    ----------------------------------------------------------------------
    c_mnpio         | Clave municipio                       | CLAVE_MUNI
    ----------------------------------------------------------------------
    id_asenta_cpcons| ID unico del asentamiento (nivel mun) | ID_ASENTAM
    ----------------------------------------------------------------------
    d_zona          | Rural / Urbano                        | TIPO_ZONA
    ----------------------------------------------------------------------
    c_cve_ciudad    | Clave ciudad                          | CLAVE_CIUDAD
    ----------------------------------------------------------------------
"""

# Por cuestiones de formato
converters = {'d_codigo': str, 'd_asenta': str, 'd_tipo_asenta': str, 'D_mnpio': str, 'd_estado': str, 'd_ciudad': str,
              'd_CP': str, 'c_estado': str, 'c_oficina': str, 'c_CP': str, 'c_tipo_asenta': str, 'c_mnpio': str,
              'id_asenta_cpcons': str, 'd_zona': str, 'c_cve_ciudad': str}


class CargaDatos:
    def __init__(self):
        # Carga y transforma las tablas en caso de que no exista tal tabla
        if not os.path.exists('Datos/union_estados.csv'):
            # Lee el excel
            self.data = pd.ExcelFile('Datos/CPdescarga.xls')
            self.hojas = self.data.sheet_names
            # Elimina la hoja "Nota"
            self.hojas.remove('Nota')
            self.unifica_tablas()

            self.divide_tablas()

        # # Despues de cargar/transformar la tabla, carga las 3 tablas
        # self.carga_tablas()

    def unifica_tablas(self):
        """
        Metodo que UNE todas las tablas en una sola, las DIVIDE en 3
        y las guarda en archivos CSV para no volver a procesar todas las tablas:
            - Estado
            - Municipio
            - Colonia
        :return: status_code --> 0: OK, -1:Failed
        """
        # columnas = self.data.parse(self.hojas[0]).columns
        # converters = {columna: str for columna in columnas}
        # print(converters)

        # Inicializa el primer dataframe para luego ir concatenando las demás hojas
        union_estados = self.data.parse(self.hojas[0], converters=converters)
        union_estados.fillna('', inplace=True)
        # Concatena las demás hojas al dataframe anterior
        for hoja in self.hojas[1:]:
            print(f"[DEBUG][INFO] unifica_tablas: Se concateno la hoja: {hoja}")
            temp = self.data.parse(hoja, converters=converters)
            temp.fillna('', inplace=True)
            union_estados = pd.concat([union_estados, temp]).copy()

        # Renombra las columnas para que sean mas "entendibles" segun el alias que le ~asigne~
        union_estados.rename(columns={
            'd_codigo': 'CP',
            'd_asenta': 'COLONIA',
            'd_tipo_asenta': 'TIPO_ASENTAMIENTO',
            'D_mnpio': 'MUNICIPIO_ALCALDIA',
            'd_estado': 'ESTADO',
            'd_ciudad': 'CIUDAD',
            'd_CP': 'DEST_CORREO',
            'c_estado': 'CLAVE_EDO',
            'c_oficina': 'DEST_CORREO_bis',
            'c_tipo_asenta': 'CLAVE_ASENT',
            'c_mnpio': 'CLAVE_MUNI',
            'id_asenta_cpcons': 'ID_ASENTAM',
            'd_zona': 'TIPO_ZONA',
            'c_cve_ciudad': 'CLAVE_CIUDAD'
        }, inplace=True)

        # print(union_estados.head())
        union_estados = union_estados.astype('str')

        print(union_estados.head())
        try:
            union_estados.to_csv('Datos/union_estados.csv', index=False, encoding='cp1252')
            print(f"[DEBUG][OK] unifica_tablas: Se guardo exitosamente el archivo")
            return 0
        except Exception as e:
            print(f"[DEBUG][ERROR] unifica_tablas: {str(e)}")
            return -1

    def divide_tablas(self):
        union_estados = pd.read_csv('Datos/union_estados.csv', encoding='cp1252', dtype='str')
        union_estados.fillna('', inplace=True)
        print(union_estados.head())
        # Se definen las columnas para cada una de las 3 tablas: estado, municipio y colonia
        columnas_estados = ['ESTADO', 'CIUDAD', 'CLAVE_EDO', 'CLAVE_MUNI', 'ID_ASENTAM']
        columnas_municipios = ['MUNICIPIO_ALCALDIA', 'CLAVE_MUNI', 'CLAVE_EDO', 'ID_ASENTAM', 'CP']
        columnas_colonias = ['COLONIA', 'TIPO_ASENTAMIENTO', 'DEST_CORREO', 'DEST_CORREO_bis', 'CLAVE_ASENT',
                            'ID_ASENTAM', 'TIPO_ZONA', 'CP', 'c_CP', 'CLAVE_CIUDAD']
        # Se extraen las tablas de la tabla MAESTRA
        estados = union_estados[columnas_estados]
        municipios = union_estados[columnas_municipios]
        colonias = union_estados[columnas_colonias]
        # Se quitan los duplicados
        estados.drop_duplicates(inplace=True)
        municipios.drop_duplicates(inplace=True)
        colonias.drop_duplicates(inplace=True)
        # Se guardan cada una de las 3 tablas
        estados.to_csv('Datos/estados.csv', index=False, encoding='cp1252')
        municipios.to_csv('Datos/municipios.csv', index=False, encoding='cp1252')
        colonias.to_csv('Datos/colonias.csv', index=False, encoding='cp1252')

    # def carga_tablas(self):
    #     self.estados = pd.read_csv('Datos/estados.csv', encoding='cp1252', dtype='str')
    #     self.estados.fillna('', inplace=True)
    #     self.municipios = pd.read_csv('Datos/municipios.csv', encoding='cp1252', dtype='str')
    #     self.municipios.fillna('', inplace=True)
    #     self.colonias = pd.read_csv('Datos/colonias.csv', encoding='cp1252', dtype='str')
    #     self.colonias.fillna('', inplace=True)


# loader = CargaDatos()
# # loader.print_sheets()
#
# reader = Consultor(loader.estados, loader.municipios, loader.colonias)
# reader.from_estado('Aguascalientes')
# reader.from_colonia('San Diego')
# reader.from_municipio('Acámbaro')
# reader.from_cp('38600')