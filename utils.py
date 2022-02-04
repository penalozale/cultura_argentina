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
import sys

# Funciones a utilizar en el proyecto:
### ----------------------------------------------------------------
def requests_get_OK(web):
    ''' Verifica el código de estado de la respuesta de requests.get
        
    INPUT: web: es objeto Response que se obtiene al ejecutar: requests.get(url)
    OUTPUT: código del estado del request
    '''
    codigo = web.status_code   # si el valor es 200 significa que funcionó el "requests.get"
    if  codigo != 200:
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
    
    # Entra y verifica la pagina
    pagina = requests.get(url = url_pagina)
    requests_get_OK(pagina)
    
    # Busca y extrae el link
    inicio = 'href="'
    final = '">DESCARGAR'
    link_descarga = re.search(f'{inicio}(.*?){final}', pagina.text)[1]
    
    return link_descarga

### ----------------------------------------------------------------
def descargar_tabla(url_descarga):
    ''' Descarga la tabla de datos en formato binario
    
    INPUT: url_descarga: enlace de descarga del archivo con los datos (archivo .csv).
    OUPUT: contenido: tabla en formato binario.    
    '''
    
    pagina = requests.get(url = url_descarga)
    requests_get_OK(pagina)

    # Extrae el contenido del archivo
    contenido = pagina.content
    
    file_name = url_descarga.split("/")[-1]  # nombre del archivo de la url de descarga
    logging.info(f'Se ha descargado la información de {file_name}')

    return contenido

### ----------------------------------------------------------------
def file_path(categoria):
    ''' Crea la estructura de carpetas donde se guardarán las tablas.
    Por ej: Cultura_dataset/museos/2021-diciembre/museos-10-12-2021.csv
    
    INPUT: categoria: link de descarga de la tabla de datos
    OUTPUT: file_path: el path completo donde se guardará el archivo
    '''
    # Carpeta principal
    path = 'Cultura_dataset'
    
    # Carpeta secundaria: Categoría
    folder_cat = categoria
    
    # Carpeta terciaria: Fecha
    year = date.today().strftime('%Y')
    month = date.today().strftime('%B')
    folder_date = year+'-'+month  # YYYY-mes
    
    # Path final para la categoría correspondiente
    path_final = os.path.join(path,folder_cat, folder_date)

    # Creamos las carpetas de forma recursiva si NO existen.
    os.makedirs(path_final, exist_ok=True)
    
    # # Fecha de Descarga: DD-MM-YYYY
    download_date = date.today().strftime('%d-%m-%Y')  
    # Nombre del archivo a guardar
    file = folder_cat + '-' + download_date + '.csv'   
    # Path con el nombre del archivo a guardar
    file_path = os.path.join(path_final, file)
    
    return file_path

### ----------------------------------------------------------------
def guardar_archivo_bin(file_path, tabla):
    ''' Crea el archivo y guarda la tabla de datos en el mismo.
    
    INPUT: file_path: El path donde se guardarán los datos
           tabla: variable que contiene el contenido de la tabla
    '''        
    csv_file = open(file_path, 'wb')  # "wb": escritura binaria
    csv_file.write(tabla)
    csv_file.close()
    
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
def corregir_provincias(df, col_name):
    '''
    Debido a que a veces encontramos el nombre de las provincias
    sin tildes o en minúsculas, buscamos que las provincias
    estén escritas de una sóla forma, igual en todas las tablas.
    
    INPUT: df: dataframe con los datos (tipo dataframe de pandas)
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
    
    df[col_name] = df[col_name].str.lower().str.translate(trans)
    
    for p in provincias:
        mask = p.lower().translate(trans)
        df.loc[df[col_name].str.contains(mask), col_name] = p
    
    return df  

### ----------------------------------------------------------------
def estand_escritura(df, col_name):
    ''' Les saca las tildes a los strings de una columna, 
        y los cambia a minúsculas
    '''
    a = 'áéíóú'
    b = 'aeiou'
    trans = str.maketrans(a,b)
    
    df[col_name] = df[col_name].str.lower().str.translate(trans) 
    return

### ----------------------------------------------------------------
def corr_id_dpto_loc(df, col_name, prov_name, prov_id):
    '''
    Verifica y corrige si los primeros dos caracteres de la
    columna "col_name" (id_departamento o cod_localidad)
    se corresponden con el id de la provincia.
    
    INPUT: 
    df: dataframe, al menos, con las columnas: 
        'Provincia', 'Id_provincia', 'Id_departamento' y 'Cod_localidad'
    col_name: nombre de la columna a verificar
    prov_name: nombre de la provincia, ej: 'Salta'
    prov_id: ID de la provincia: ej: '66'
    
    OUTPUT:
    Sobreescribe la tabla (dataframe) con las correcciones hechas.
    '''
    value = prov_name
    key = prov_id
    xx = df[df['Provincia']==value] 
    mask_dpto = xx[col_name].str[:2] != key
    idx = mask_dpto.index[mask_dpto].to_list()
    if idx:
        for i in idx:
            new = key + df.loc[i, col_name][2:]
            df.loc[i, col_name] = new
    return

### ----------------------------------------------------------------
def cambio_localidad(df, prov_name , old, new):
    ''' prov_name: con tilde y las primeras letras mayúsculas'''
    if old in df['Localidad'].values:
        condicion = df['Localidad'] == old
        if df.loc[condicion, 'Provincia'].values == prov_name:
            df.loc[condicion, 'Localidad'] = new
    return

### ----------------------------------------------------------------
def corr_localidad(df, cod_localidad, new_localidad):
    ''' 
    Modifica el nombre de la localidad con el codigo dado, 
    por una nuevo nombre. 
    Tal vez con la API de la web, se puede corregir esto.
    INPUT: 
        df: tabla de datos (dataframe) 
        cod_localidad: código de la localidad ("correcto")
        new_localidad: nuevo nombre de la localidad
    OUTPUT: 
        Se sobreescribe la localidad en el mismo dataframe
    '''
    df.loc[df['Cod_localidad']==cod_localidad, 'Localidad'] = new_localidad
    return 

### ----------------------------------------------------------------
def str_minuscula(str):
    ''' Convierte a minúscula y sin tildes una cadena (un string) '''
    a = 'áéíóú'
    b = 'aeiou'
    trans = str.maketrans(a,b)
    
    return(str.lower().translate(trans))

### ----------------------------------------------------------------
def mover_col_end(df, col_name):
    ''' Mueve la columna que elijamos al final del dataframe'''
    col = df.pop(col_name)
    return pd.concat([df, col], axis=1)











#def lista_diferencias(lista_larga, lista_corta):
#    ''' Devuelve una lista con los elementos que tiene la "lista larga" 
#        y que no está en la "lista corta" (listas de strings)
#    '''
#    loc_hp = [lista_larga[i] for i in range(len(lista_larga)) if lista_larga[i] not in lista_corta]
#    return(loc_hp)



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