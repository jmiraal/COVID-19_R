import os
import zipfile
import json

'''
    Para ejecutar este script es necesario tener las credenciales de kaggle.
    Se pueden descargar muy fácilmente siguiendo las instrucciones de su 
    página web. Nosotros hemos colocado el fichero json con el usuario y la 
    clave dentro del directorio .kaggle. 
    
    También es necesario tener installa la api de kaggle.
        
        - pip install kaggle
        
        o si se trabaja con python desde anaconda:
        
        - conda install -c conda-forge kaggle
    
'''    

# almacenamos las credenciales de kaggle   
data = {"username":"username","key":"tockenvalue"} 
with open('./.kaggle/kaggle.json', 'r') as credential:
    data = json.load(credential)
os.environ['KAGGLE_USERNAME'] = data["username"]
os.environ['KAGGLE_KEY'] = data["key"]

# obtenemos el zip con todos los datasets.
os.system('kaggle datasets download -d sudalairajkumar/novel-corona-virus-2019-dataset')

# descomprimimos el fichero descargado y almacenamos 
#covid_19_data.csv en el directorio /data.
with zipfile.ZipFile('novel-corona-virus-2019-dataset.zip','r') as zip_ref:
    zip_ref.extract('covid_19_data.csv', path = './data')


# eliminamos el fichero comprimido que hemos descargado
os.remove('novel-corona-virus-2019-dataset.zip')
