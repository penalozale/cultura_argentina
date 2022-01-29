
def proces_datos():    
    ### Cargamos las librerías
    import glob
    import chardet
    import pandas as pd
    import numpy as np
    import os
    import logging
    
    # Donde guardo funciones a utilizar:
    import utils
    import tareas_correccion as tc
    
    # Reutilizamos el archivo info.LOG (creado anteriormente)
    logging.basicConfig(filename= 'info.log', 
                        format='%(asctime)s : %(levelname)s : %(message)s',
                        datefmt='%d/%m/%y %H:%M:%S', level=logging.INFO, 
                        filemode = 'a', force=True)
    logging.info(' -- Ejecutando el procesamiento de los datos...')
    
    # Archivos a procesar:
    archivos = utils.buscar_archivos()

    # Asignamos nombres a los archivos
    biblio = [b for b in archivos if 'biblio' in b][0]
    museos = [m for m in archivos if 'museo' in m][0]
    cines = [c for c in archivos if 'cine' in c][0]
    
    # Leemos los archivos en formato DataFrame
    biblio_df = utils.leer_archivos_DF(biblio)
    museos_df = utils.leer_archivos_DF(museos)
    cines_df = utils.leer_archivos_DF(cines)

    # Reemplazamos los 's/d' por np.NaN
    biblio_df_nan = utils.reemplazo_sd_NaN(biblio_df)
    museos_df_nan = utils.reemplazo_sd_NaN(museos_df)
    cines_df_nan = utils.reemplazo_sd_NaN(cines_df)

    
    ### --- Modificamos los nombres de las columnas ---
    # Nombre de las columnas dadas en el enunciado del Challenge:
    columnas = ['Cod_localidad', 'Id_provincia', 'Id_departamento',
                    'Categoría', 'Provincia', 'Localidad', 'Nombre', 
                    'Domicilio', 'Código postal', 'Número de teléfono',
                    'Email', 'Web', 'Fuente']

    try:
        '''  Bibliotecas Populares '''
        biblio_df_nan.rename(columns={'Cod_Loc':columnas[0], 'IdProvincia':columnas[1],
                                      'IdDepartamento':columnas[2], 'Categoría':columnas[3],
                                      'Provincia':columnas[4], 'Localidad':columnas[5],
                                      'Nombre':columnas[6], 'Domicilio':columnas[7],
                                      'CP':columnas[8], 'Teléfono':columnas[9],
                                      'Mail':columnas[10], 'Web':columnas[11]},
                             inplace=True)
        '''  Cines '''
        cines_df_nan.rename(columns={'Cod_Loc':columnas[0], 'IdProvincia':columnas[1],
                                     'IdDepartamento':columnas[2], 'Categoría':columnas[3],
                                     'Provincia':columnas[4], 'Localidad':columnas[5],
                                     'Nombre':columnas[6], 'Dirección':columnas[7],
                                     'CP':columnas[8], 'Teléfono':columnas[9],
                                     'Mail':columnas[10], 'Web':columnas[11]},
                            inplace=True)
        '''  Museos '''
        museos_df_nan.rename(columns={'Cod_Loc':columnas[0], 'IdProvincia':columnas[1],
                                      'IdDepartamento':columnas[2], 'categoria':columnas[3],
                                      'provincia':columnas[4], 'localidad':columnas[5],
                                      'nombre':columnas[6], 'direccion':columnas[7],
                                      'CP':columnas[8], 'telefono':columnas[9],
                                      'Mail':columnas[10], 'Web':columnas[11], 'fuente':columnas[12]},
                             inplace=True)
    except KeyError as err:
        logging.error(f"Revisar el nombre de las columnas relacionada con : {err}")
        print('Se ha modificado el nombre de alguna columna relacionada con : ', err)
    
    ### --- Modificamos y estandarizamos los nombres de las Provincias ---
    biblio_df_nan = utils.corregir_provincias(biblio_df_nan, 'Provincia')
    museos_df_nan = utils.corregir_provincias(museos_df_nan, 'Provincia')
    cines_df_nan = utils.corregir_provincias(cines_df_nan, 'Provincia')

    ### --- Unimos el código de área con el número de teléfono ---    
    # Primero eliminamos cualquier espacio en blanco que haya entre los números:
    biblio_df_nan['Número de teléfono'] = biblio_df_nan['Número de teléfono'].str.replace(' ','')
    museos_df_nan['Número de teléfono'] = museos_df_nan['Número de teléfono'].str.replace(' ','')
    cines_df_nan['Número de teléfono'] = cines_df_nan['Número de teléfono'].str.replace(' ','')
    
    try:
        biblio_df_nan['Número de teléfono'] = biblio_df_nan['Cod_tel'] + biblio_df_nan['Número de teléfono']
        museos_df_nan['Número de teléfono'] = museos_df_nan['cod_area'] + museos_df_nan['Número de teléfono']
        cines_df_nan['Número de teléfono'] = cines_df_nan['cod_area'] + cines_df_nan['Número de teléfono']
    except KeyError as errK:
        logging.error(f'La columna {errK} no existe. Modificar el nombre.')
        print(f'La columna {errK} no existe. Modificar el nombre.')
    
    
    ### --- Creamos la tabla con info sobre las Salas de Cines ---
    # Estandarizamos los valores que puede tomar la columna 'espacio_INCAA': sólo 0's y 1's
    cines_df_nan['espacio_INCAA'].replace(['si','Si','SI', '1'], 1, inplace=True)
    cines_df_nan['espacio_INCAA'].replace(['nan','0',np.NaN, 'no', 'NO', 'No'], 0, inplace=True)
    if len(cines_df_nan['espacio_INCAA'].unique()) != 2:
        logging.error(f'Error en la estandarización de espacio_INCAA')
        print('Error en la estandarización de espacio_INCAA')
        print('Ver que valor no se modificó por 0 o 1:')
        print(cines_df_nan['espacio_INCAA'].unique())

    # Modificamos el tipo de dato de algunas columnas
    cols = ['Provincia', 'Pantallas', 'Butacas', 'espacio_INCAA']
    cines_INCAA = cines_df_nan.astype({'Pantallas':'int', 'Butacas':'int', 'espacio_INCAA':'int'})

    # Calculamos la cantidad de Pantallas, Butacas y Espacios INCAA que hay por provincia.
    tabla_INCAA = cines_INCAA[cols].groupby(by='Provincia').sum().sort_values(by='Pantallas', ascending=False)

    # Guardamos la tabla
    path_incaa = os.path.normpath(os.path.join(cines, "..", "..", "..")) + '/cines_INCAA.csv'
    tabla_INCAA.to_csv(path_incaa, sep=',', encoding='utf8')

    print(f'se guardó la tabla de espacios INCAA en {path_incaa}')
    logging.info(f'se guardó la tabla de espacios INCAA en {path_incaa}')

    ### --- Eliminamos las columnas que no vamos a utilizar ---
    biblio_final = biblio_df_nan.drop(columns=[col for col in biblio_df_nan if col.capitalize() not in columnas])
    museos_final = museos_df_nan.drop(columns=[col for col in museos_df_nan if col.capitalize() not in columnas])
    cines_final = cines_df_nan.drop(columns=[col for col in cines_df_nan if col.capitalize() not in columnas])

    ### --- Creamos la "tabla unica" ---
    # Unimos las tres tablas en una sola
    tablas = [biblio_final, museos_final, cines_final]
    tabla_final = pd.concat(tablas, ignore_index=True)
    
    # Trabajaremos con una copia de la tabla original
    tabla = tabla_final.copy(deep=True) 
    
    # utilizo lafuncion en el archivo "tareas_correccion.py"
    tc.correcciones(tabla)
    
    # Eliminamos la columna 'Fuente'
    tabla_unica = tabla.drop(columns = 'Fuente')
    
    # Guardamos la 'tabla única'  como un archivo .csv
    path_tabla = os.path.normpath(os.path.join(cines, "..", "..", "..")) + '/tabla_unica.csv'
    tabla_unica.to_csv(path_tabla, sep=',', encoding='utf8')

    print(f'Se guardó la tabla que combina las 3 categorías en {path_tabla}')
    logging.info(f'se guardó la tabla que combina las 3 categorías en {path_tabla}')
        
    ### --- Creamos la tabla con 3 sub-tablas ---

    # Tabla 1: Cantidad de registros totales por categoría
    reg_por_categoria = tabla_final['Categoría'].value_counts()
    # Tabla 2: Cantidad de registros totales por fuente
    reg_por_fuente = tabla_final['Fuente'].value_counts()
    # Tabla 3: Cantidad de registros por Provincia y Categoría
    reg_prov_categ = tabla_final.groupby(by=['Provincia', 'Categoría']).size()

    # Guardamos las tres tablas anteriores en una misma tabla
    path_final = os.path.normpath(os.path.join(cines, "..", "..", "..")) + '/datos_conjuntos.csv'
    with open(path_final, 'w') as f:
        f.write('# Registros totales por categoría:\n')
        reg_por_categoria.to_csv(f, header = False, mode = 'a', encoding='utf8')
        f.write('\n')
        f.write('# Registros por provincia y por categoría:\n')
        reg_prov_categ.to_csv(f, header = False, mode = 'a', encoding='utf8')
        f.write('\n')
        f.write('# Registros totales por fuente:\n')
        reg_por_fuente.to_csv(f, header = False, mode = 'a', encoding='utf8')
        
        
    print(f'se guardaron 3 tablas en un mismo archivo, en  {path_final}')
    logging.info(f'Se guardó la tabla de "datos conjuntos" en {path_final}')

    logging.info('...... Terminó el Procesado de Datos (2da parte)')
    print(' \n...... Terminó el Procesado de Datos (2da parte)')

    ## ----------------------------------------------------------------
    file1 = path_incaa   #   path_tabla,  path_final
    with open(file1, 'rb') as data:
        result = chardet.detect(data.read(1000000))
        print(file1,':.... cines incaa')
        print(result)
        
    file2 = path_tabla   # ,  path_final
    with open(file2, 'rb') as data:
        result = chardet.detect(data.read(1000000))
        print(file2,':.... tabla final ')
        print(result)
        
    file3 = path_final 
    with open(file3, 'rb') as data:
        result = chardet.detect(data.read(1000000))
        print(file3,':....  datos conjuntos ')
        print(result)
    