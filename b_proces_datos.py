def proces_datos():    
    ### Cargamos las librerías
    import utils
    import glob
    import chardet
    import pandas as pd
    import numpy as np
    import os
    import logging
    
    # -----------------------------------------------
    # Usamos el archivo info.LOG creado anteriormente
    logging.basicConfig(filename= 'info.log', 
                        format='%(asctime)s : %(levelname)s : %(message)s',
                        datefmt='%d/%m/%y %H:%M:%S', level=logging.INFO, 
                        filemode = 'a', force=True)
    logging.info('EJECUTANDO LA PARTE 2 (2do archivo....')
    
    # -----------------------------------------------
    # Archivos a procesar:
    archivos = utils.buscar_archivos()

    # -----------------------------------------------
    ### ---- Abrimos archivos y reemplazamos 's/d' por np.NaN ----
    # Asignamos nombres a los archivos
    biblio = archivos[0]
    museos = archivos[1]
    cines = archivos[2]

    # Abrimos los archivos en formato DataFrame
    biblio_df = utils.leer_archivos_DF(biblio)
    museos_df = utils.leer_archivos_DF(museos)
    cines_df = utils.leer_archivos_DF(cines)

    # Reemplazamos los 's/d' por np.NaN
    biblio_df_nan = utils.reemplazo_sd_NaN(biblio_df)
    museos_df_nan = utils.reemplazo_sd_NaN(museos_df)
    cines_df_nan = utils.reemplazo_sd_NaN(cines_df)

    # -----------------------------------------------
    ### ---- Modificamos los nombres de las columnas ----
    # Nombre de las columnas dadas en el enunciado del Challenge:
    columnas = ['Cod_localidad', 'Id_provincia', 'Id_departamento',
                    'Categoría', 'Provincia', 'Localidad', 'Nombre', 
                    'Domicilio', 'Código postal', 'Número de teléfono',
                    'Email', 'Web', 'Fuente']

    '''  Bibliotecas Populares '''
    biblio_df_nan.rename(columns={'Cod_Loc':columnas[0], 'IdProvincia':columnas[1],
                                  'IdDepartamento':columnas[2], 'Categoría':columnas[3],
                                  'Provincia':columnas[4], 'Localidad':columnas[5], 
                                  'Nombre':columnas[6], 'Domicilio':columnas[7],
                                  'CP':columnas[8], 'Teléfono':columnas[9],
                                  'Mail':columnas[10], 'Web':columnas[11]},
                         inplace=True)

    '''  Museos '''
    museos_df_nan.rename(columns={'localidad_id':columnas[0], 'provincia_id':columnas[1],
                                  'provincia':columnas[4], 'localidad':columnas[5], 
                                  'nombre':columnas[6], 'direccion':columnas[7],
                                  'codigo_postal':columnas[8], 'telefono':columnas[9],
                                  'mail':columnas[10], 'web':columnas[11], 'fuente':columnas[12]},
                         inplace=True)

    # Agregamos la columna 'Id_departamento' a partir del Código de Localidad y la columna 'Categoría' = 'Museos'
    for ind in range(len(museos_df_nan)):
        museos_df_nan.loc[ind, 'Id_departamento'] = int(str(museos_df_nan['Cod_localidad'][ind])[:-3])
    museos_df_nan['Id_departamento'] = museos_df_nan['Id_departamento'].astype('Int64')
    museos_df_nan['Categoría'] = 'Museos'

    '''  Cines '''
    cines_df_nan.rename(columns={'Cod_Loc':columnas[0], 'IdProvincia':columnas[1],
                                 'IdDepartamento':columnas[2], 'Categoría':columnas[3],
                                 'Provincia':columnas[4], 'Localidad':columnas[5], 
                                 'Nombre':columnas[6], 'Dirección':columnas[7],
                                 'CP':columnas[8], 'Teléfono':columnas[9],
                                 'Mail':columnas[10], 'Web':columnas[11]},
                        inplace=True)

    # -----------------------------------------------
    ### ---- Modificamos y estandarizamos los nombres de las Provincias ----
    # NOTA: Nuestro país está dividido en 24 jurisdicciones: 23 provincias y un distrito federal (Ciudad Autónoma de Buenos Aires). Tomaremos al distrito federal (CABA) como la 24ta provincia.
    biblio_df_nan = utils.corregir_provincias(biblio_df_nan, 'Provincia')
    museos_df_nan = utils.corregir_provincias(museos_df_nan, 'Provincia')
    cines_df_nan = utils.corregir_provincias(cines_df_nan, 'Provincia')

    # -----------------------------------------------
    ### ---- Unimos el código de área con el número de teléfono ----
    # Si hay algún error, verificar si no cambiaron los nombres de las columnas.

    biblio_df_nan['Número de teléfono'] = biblio_df_nan['Cod_tel'] + biblio_df_nan['Número de teléfono']
    museos_df_nan['Número de teléfono'] = museos_df_nan['codigo_indicativo_telefono'] + museos_df_nan['Número de teléfono']
    cines_df_nan['Número de teléfono'] = cines_df_nan['cod_area'] + cines_df_nan['Número de teléfono']

    # -----------------------------------------------
    ### ---- Creamos una tabla con información sobre las Salas de Cines ----

    # Estandarizamos los valores que puede tomar la columna 'espacio_INCAA': sólo 0's y 1's (No y Si)
    cines_df_nan['espacio_INCAA'].replace(['si','Si','SI', '1'], 1, inplace=True)
    cines_df_nan['espacio_INCAA'].replace(['nan','0',np.NaN, 'no', 'NO', 'No'], 0, inplace=True)
    if len(cines_df_nan['espacio_INCAA'].unique()) != 2: 
        print('Error en la estandarización INCAA')  # verificar q sólo hay 1 y 0
        print('Verificar que valor no se modificó por 0 o 1')
        print(cines_df_nan['espacio_INCAA'].unique())

    # Cambiamos el dtype de algunas columnas (sino algunas dan error)
    cols = ['Provincia', 'Pantallas', 'Butacas', 'espacio_INCAA']
    cines_INCAA = cines_df_nan.astype({'Pantallas':'int', 'Butacas':'int', 'espacio_INCAA':'int'})

    # Agrupamos por provincia y calculamos la cantidad de Pantallas, Butacas y espacios INCAA que hay.
    tabla_INCAA = cines_INCAA[cols].groupby(by='Provincia').sum().sort_values(by='Pantallas', ascending=False)

    # Guardamos la tabla como un archivo .csv
    path_incaa = os.path.normpath(os.path.join(cines, "..", "..", "..")) + '/cines_INCAA.csv'
    tabla_INCAA.to_csv(path_incaa, sep=',')

    print(f'se guardó la tabla de espacios INCAA en {path_incaa}')
    logging.info(f'se guardó la tabla de espacios INCAA en {path_incaa}')

    # -----------------------------------------------
    ### ---- Eliminamos las columnas que no vamos a utilizar ----
    biblio_final = biblio_df_nan.drop(columns=[col for col in biblio_df_nan if col.capitalize() not in columnas])
    museos_final = museos_df_nan.drop(columns=[col for col in museos_df_nan if col.capitalize() not in columnas])
    cines_final = cines_df_nan.drop(columns=[col for col in cines_df_nan if col.capitalize() not in columnas])

    # -----------------------------------------------
    ### ---- Creamos y guardamos la tabla con los datos conjuntos ----

    # Unimos las tres tablas en una única tabla
    tablas = [biblio_final, museos_final, cines_final]
    tabla_final = pd.concat(tablas, ignore_index=True)

    # Eliminamos la columna 'Fuente' (no es necesaria en esta tabla)
    tabla_unica = tabla_final.drop(columns = 'Fuente')

    # Guardamos la tabla única  como un archivo .csv
    path_tabla = os.path.normpath(os.path.join(cines, "..", "..", "..")) + '/tabla_unica.csv'
    tabla_unica.to_csv(path_tabla, sep=',')

    print(f'Se guardó la tabla que combina las 3 categorías en {path_tabla}')
    logging.info(f'se guardó la tabla que combina las 3 categorías en {path_tabla}')

    # -----------------------------------------------
    ### ---- Creamos una tabla con las siguientes sub-tablas ----
    # 1) Cantidad de registros totales por categoría
    # 2) Cantidad de registros totales por fuente
    # 3) Cantidad de registros por provincia y categoría
    # usamos la tabla_final (que tiene la columna 'Fuente')

    # Tabla 1: Cantidad de registros totales por categoría
    reg_por_categoria = tabla_final['Categoría'].value_counts()
    # Tabla 2: Cantidad de registros totales por fuente
    reg_por_fuente = tabla_final['Fuente'].value_counts()
    # Tabla 3: Cantidad de registros por Provincia y Categoría
    reg_prov_categ = tabla_final.groupby(by=['Provincia', 'Categoría']).size()

    # Guardamos las tres tablas anteriores en una misma tabla
    path_final = os.path.normpath(os.path.join(cines, "..", "..", "..")) + '/datos_conjuntos.csv'
    with open(path_final, 'w') as f:
        f.write('# Cantidad de registros totales por categoría:')
        reg_por_categoria.to_csv(f, header = False, mode = 'a')
        f.write('\n')
        f.write('# Cantidad de registros totales por fuente:')
        reg_por_fuente.to_csv(f, header = False, mode = 'a')
        f.write('\n')
        f.write('# Cantidad de registros por provincia y por categoría:')
        reg_prov_categ.to_csv(f, header = False, mode = 'a')

    print(f'se guardaron 3 tablas en un mismo archivo, en  {path_final}')
    logging.info(f'se guardaron las 3 tablas juntas en  {path_final}')

    logging.info('.........Terminó el Procesado de Datos (2da parte)')
    print(' \n    Terminó el Procesado de Datos (2da parte)')
