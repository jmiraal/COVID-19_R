import requests
import json
import pandas as pd
import numpy as np
import time


def obtenerListaLocalizaciones(file):
    '''
       FUNCIÓN 
                Lee un un fichero con todos los datos dataframe 
                con los valores únicos de las localizaciones. Estos valores
                serán el resultado de juntar las columnnas Province/State y 
                Country/Region.
        ENTRADA 
                file: Ubicación del fichero csv con los datos.
        SALIDA 
                df: Dataframe con lista de ubicaciones únicas.
    '''
    df = pd.read_csv(file, index_col='SNo')
    
    df = df[['Province/State', 'Country/Region']]
    df['Province/State'] = df['Province/State'].str.replace('Recovered', '')
    df = df.replace({'None': ''})
    df.fillna(value='', inplace=True)
    df.columns = ['PROVINCE_STATE',  'COUNTRY_REGION']
    df.drop_duplicates(subset =['PROVINCE_STATE', 'COUNTRY_REGION'], inplace = True)
    df['LOCALIZACION'] = df['PROVINCE_STATE'] + '-' + df['COUNTRY_REGION']
    return df

def ejecutarRequest(localizacion, key):

    '''
       FUNCIÓN 
                Dada una ubicación e formato String y la lave key, envía una 
                cosulta API REST a la página LocationsIQ para obtener sus
                coordenadas.
        ENTRADA 
                localizacion: Texto con el nombre del lugar.
        SALIDA 
                key: clave para poder usar la API de location IQ
    '''
    
    try:
        url = 'https://us1.locationiq.com/v1/search.php?key=' + key + '&q=' + localizacion + '&format=json'
        response = requests.get(url)
        json_data = json.loads(response.text)
        time.sleep(1)
        return pd.Series([json_data[0]['lat'], json_data[0]['lon']])
    except:
        print(localizacion)
        print(json_data)
        return [np.nan, np.nan]


def ejecutarListaRequests(key, df):
    '''
       FUNCIÓN 
                Dado un dataframe con las localizaciones en la columna 
                'LOCALIZACION', devuelve ese dataframe con dos columnas adicio-
                nales con la latitud y la longitud
        ENTRADA 
                key: clave para poder usar la API de location IQ
                df: df con las localizaciones
        SALIDA 
                df: df con las localizaciones y la información de coordenadas.
    '''

    df[['lat', 'long']] = df.apply(lambda row: ejecutarRequest(row['LOCALIZACION'], key), axis=1)

    return df
 
key = '27a77321a056ec'
df_loc = obtenerListaLocalizaciones('./data/covid_19_data.csv')
df_loc = ejecutarListaRequests(key, df_loc)
df_loc.to_csv (r'./data/localizaciones.csv', index = False, header=True)
