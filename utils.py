#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 15:10:29 2022

@author: penalozale
"""
# Librerías a utilizar
import logging
import requests
import re
from datetime import date
import os
import glob
import chardet
import pandas as pd
import numpy as np

# Funciones a utilizar en el proyecto:
### ----------------------------------------------------------------
def requests_get_OK(web):
    ''' Verifica el código de estado de la respuesta de requests.get
        
    INPUT: web: es objeto Response que se obtiene al ejecutar: requests.get(url)
    OUTPUT: código del estado del request
    '''
    codigo = web.status_code   # si el valor es 200 significa que funcionó el "requests.get"
    if  codigo == 200:
        logging.info(f'Requests Exitoso del link.')   # si el link es el del archivo, saco el nombre de ahí con split
    elif codigo == 504:
        logging.warning(f'Falla del Servidor. Error: {codigo} Gateway Time-out')
        sys.exit(f'Falla del Servidor. Vuelva a intentar. Error: {codigo} Gateway Time-out')
    else:
        logging.warning(f'Falló el Requests. Error: {codigo}') 
        sys.exit(f'Falló el Requests. Error: {codigo}')
    
    return

### ----------------------------------------------------------------
def obtener_link(url_pagina):
    ''' Verifica que existe la URL y obtiene el link de descarga de la tabla de datos.
    Controla que la pagina tenga el botón "DESCARGAR" que se usa para descargar el archivo.
        
    INPUT: url_pagina: enlace de la página web de la cual queremos obtener el link de descarga.
    OUPUT: link_descarga: enlace de descarga
    '''
    
    logging.info(f'__Pagina web a utilizar: {url_pagina}')
    
    # Entra y verifica la pagina
    pagina = requests.get(url = url_pagina)
    requests_get_OK(pagina)
    
    # Busca y Extrae el link
    inicio = 'href="'
    final = '">DESCARGAR'
    link_descarga = re.search(f'{inicio}(.*?){final}', pagina.text)[1]
    
    if link_descarga: 
        logging.info(f'Se ha obtenido el link de descarga: {link_descarga}')
        return link_descarga
    else:
        logging.warning(f'No se encuentra el link de descarga: {link_descarga}')
        return print('No se encuentra el link de descarga')

### ----------------------------------------------------------------
def descargar_tabla(url_descarga):
    ''' Descarga la tabla de datos en formato binario
    
    INPUT: url_descarga: enlace de descarga del archivo con los datos (archivo .csv).
    OUPUT: contenido: tabla en formato binario.    
    '''
    
    pagina = requests.get(url = url_descarga)
    requests_get_OK(pagina)

    # Extrae el contenido del archivo
    contenido = pagina.content   # Contains bytes with the raw response content.
    
    file_name = url_descarga.split("/")[-1]  # nombre del archivo de la url de descarga
    logging.info(f'Se ha descargado la información de {file_name}')

    return contenido

### ----------------------------------------------------------------
def file_path(categoria_link):
    ''' Crea la estructura de carpetas donde se guardarán las tablas.
    Por ej: Cultura_dataset/museos/2021-diciembre/museos-10-12-2021.csv
    
    INPUT: categoria_link: link de descarga de la tabla de datos
    OUTPUT: file_path: el path completo donde se guardará el archivo
    '''
    # Carpeta principal
    path = 'Cultura_dataset'
    
    # Carpeta secundaria para la categoría correspondiente
    file_name = categoria_link.split('/')[-1]
    folder_category = file_name.replace('.csv','')
    
    # Carpeta terciaria 
    year = date.today().strftime('%Y')
    month = date.today().strftime('%B')
    folder_date = year+'-'+month  # YYYY-mes
    
    # Path final para la categoría correspondiente
    path_final = os.path.join(path,folder_category, folder_date)

    # Creamos las carpetas de forma recursiva si NO existen (exist_ok=True).
    os.makedirs(path_final, exist_ok=True)
    
    # # Fecha de Descarga DD-MM-YYYY
    download_date = date.today().strftime('%d-%m-%Y')  
    # Nombre del archivo a guardar
    file = folder_category + '-' + download_date + '.csv'   
    # Path con el nombre del archivo a guardar
    file_path = os.path.join(path_final, file)
    
    logging.info(f'El path completo con el archivo es: {file_path}')
    
    return file_path

### ----------------------------------------------------------------
def guardar_archivo_bin(file_path, tabla):
    ''' Crea el archivo y guarda la tabla de datos en el mismo.
    
    INPUT: file_path: El path donde se guardarán los datos
           tabla: variable que contiene el contenido de la tabla
    OUTPUT:
    '''        
    csv_file = open(file_path, 'wb')  # "wb": escritura binaria
    csv_file.write(tabla)
    csv_file.close()
    
    logging.info(f'Se guardó la tabla en: {file_path}')
    return

### ----------------------------------------------------------------
def buscar_archivos(carpeta_ppal = 'Cultura_dataset'):
    ''' Busca la carpeta principal donde se guardaron los archivos y
    busca los archivos con los datos, i.e. las tablas
    (Los archivos fuentes los habíamos guardado dentro de la carpeta "Cultura_dataset")
    Deben haber sólo 3 carpetas dentro de "Cultura_dataset", correspondientes a las
    tres categorías (i.e. bibliotecas populares, museos y cines).
    
    INPUT: carpeta principal, creada en la función file_path
    OUTPUT: lista con los path de cada archivo a procesar
    '''
    # Buscamos la carpeta raíz donde están las carpetas con los datos
    for root, dir, files in os.walk(os.getcwd()):
        if carpeta_ppal in dir:
            path = os.path.join(root, carpeta_ppal) 
    
    p = path+'/*'
    # Carpetas de cada categoria
    folder_cat = glob.glob(p)
    # Selecciona las carpetas más nuevas de cada categoria
    last_folder = [max(glob.glob(ind+'/*'), key=os.path.getmtime) for ind in folder_cat if os.path.isdir(ind)]
    # Selecciona los archivos más nuevos de cada categoria
    last_files = [max(glob.glob(ind+'/*'), key=os.path.getmtime) for ind in last_folder]
        
    logging.info(f'Carpeta y archivos encontrados.')

    return last_files

### ----------------------------------------------------------------
def leer_archivos_DF(file):
    '''
    Chequeamos el encoding del archivo y lo abrimos.
    
    INPUT: el path del archivo a leer
    OUTPUT: DataFrame con la tabla de datos
    '''
    
    with open(file, 'rb') as data:
        result = chardet.detect(data.read(1000000))
    encode = result['encoding']    
    
    df = pd.read_csv(file, encoding = encode, dtype=str)  
    
    logging.info(f'Archivo leído: {file}')
    
    return df

### ----------------------------------------------------------------
def reemplazo_sd_NaN(df):
    '''
    Las tablas suelen tener registros nulos y tienen como valor 's/d' (sin datos).
    Chequeamos si tienen y los reemplazamos por el valor nulo: np.NaN
    
    INPUT: el dataframe de la tabla de datos
    OUTPUT: tabla de datos resultante
    '''
    if 's/d' in df.values:
        df = df.replace('s/d',np.NaN)
    return df

### ----------------------------------------------------------------
def corregir_provincias(dataframe, col_name):
    '''
    Debido a que a veces encontramos el nombre de las provincias
    sin tildes o en minúsculas, buscamos que las provincias
    estén escritas de una sóla forma, igual en todas las tablas.
    
    INPUT: dataframe: tabla con los datos (tipo dataframe de pandas)
           col_name: nombre de la columna que contiene a las provincias
    OUTPUT: dataframe estandarizado
    '''
    
    provincias = ['San Juan', 'Ciudad Autonoma de Buenos Aires',
                  'Buenos Aires', 'Entre Ríos','Santa Fé', 'Corrientes',
                  'Córdoba', 'San Luis', 'Santiago del Estero','Tucumán',
                  'Mendoza', 'La Rioja', 'Catamarca', 'Salta', 'Jujuy',
                  'Chaco', 'Formosa', 'Misiones', 'La Pampa', 'Neuquén',
                  'Río Negro', 'Santa Cruz','Tierra del Fuego', 'Chubut']
    
    # Transformo las vocales con tildes por vocales sin tildes
    # y después paso las provincias a minúsculas para luego estandarizar.
    a = 'áéíóú'
    b = 'aeiou'
    trans = str.maketrans(a,b)
    
    dataframe[col_name] = dataframe[col_name].str.translate(trans).str.lower()
    
    for p in provincias:
        mask = p.translate(trans).lower() 
        dataframe.loc[dataframe[col_name].str.contains(mask), col_name] = p
    
    return dataframe  

### ----------------------------------------------------------------
# def fecha_ultimo_cambio(url_pagina):
#     ''' Obtiene la fecha de última modificación de los datos.
#     Buscando en la página la frase "Último cambio" y luego limpiando
#     la cadena de caracteres para obtener sólo la fecha (DD/MM/YYYY).
    
#     INPUT: url_pagina: pagina web donde se encuentra la fecha deseada
#     OUPUT: ultimo_cambio: fecha en formato: "16 julio 2018"
#     '''
    
#     pagina = requests.get(url = url_pagina)
#     requests_get_OK(pagina)
    
#     meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
#              'julio', 'agosto', 'septiembre', 'setiembre', 'octubre',
#              'noviembre', 'diciembre']
    
#     # Busca y formatea la fecha
#     target = 'Último cambio'
#     f = re.search(target, pagina.text)
#     fecha_string = pagina.text[f.span()[0]+100:f.span()[1]+210]
#     ultimo_cambio = fecha_string.strip()    # Elimina los espacios en blancos
    
#     a = [True for m in meses if m in fecha_string.lower()]
#     if not a: 
#         print('No se encontró fecha de última actualización en la web')
#         logging.warning('No se encontró fecha de última actualización en la web')
#     else:
#         logging.info(f'Se encontró la fecha {ultimo_cambio}')
    
#     if 'de' in ultimo_cambio: 
#         ultimo_cambio = ultimo_cambio.replace(' de', '')
    
#     fecha = datetime.strptime(ultimo_cambio, '%d %B %Y')
#     ultima_fecha = fecha.strftime('%d/%m/%Y')
    
#     logging.info(f'Última modificación de la tabla: {ultima_fecha}')
    
#     return ultima_fecha