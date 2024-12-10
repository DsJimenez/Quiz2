import pandas as pd
import sqlite3
import os


# Extraer la ruta de donde se encuentra la BBDD.
def mapear_datos(nombre_bd, formato): 
    carpeta = os.path.dirname(__file__)
    db_path = os.path.join(carpeta, '..', 'data', f'{nombre_bd}{formato}')
    return db_path

# Traer todas las tablas que se enceuntran en la BBDD, y que se guarda como diccionario.
def cargar_datos(ruta_archivo):
    conn = sqlite3.connect(ruta_archivo)
    
    dataframes = {}
    
    tablas = pd.read_sql('SELECT name FROM sqlite_master WHERE type = "table"', conn)
    
    for tabla in tablas['name']:
        dataframes[tabla] = pd.read_sql(f'SELECT * FROM "{tabla}"', conn)
    
    conn.close()   
    
    return dataframes


# Se almacena la ruta de la BBDD.
ruta=  mapear_datos("WWI_simple",".db")
# Se utiliza la ruta para traer la BBDD.
data = cargar_datos(ruta)

dimcity = data['DimCity']
dimcustomer = data['DimCustomer']
dimemployees = data['DimEmployee']
dimstockItem = data['DimStockItem']
factsale = data['FactSale']


dataframe = pd.merge(factsale,dimemployees,left_on='Salesperson Key', right_on='Employee Key')

dataframe2 = pd.merge(dataframe,dimcity, left_on='City Key',right_on='City Key')
#dataframe2['Total Including Tax'] = dataframe2['Total Including Tax'].astype('float')

#suma_ventas =dataframe2.groupby('Employee')['Total Including Tax'].sum().reset_index(name='Total Sales').sort_values(by='Total Sales' ,ascending=False).round(2)

dataframe2.dtypes