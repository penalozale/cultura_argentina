
def database():
    import chardet
    import os
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlalchemy.sql import text
    import psycopg2
    import sys
    import utils
    import logging
    from decouple import config
    
    logging.basicConfig(filename= 'info.log',
                        format='%(asctime)s : %(levelname)s : %(message)s',
                        datefmt='%d/%m/%y %H:%M:%S', level=logging.INFO, 
                        filemode = 'a', force=True)
    logging.info(' -- Ejecutando la creacion de la base de datos...')
        
    
    # # Buscamos y leemos los archivos
    carpeta_ppal = 'Cultura_dataset'
    for root, dir, files in os.walk(os.getcwd()):
            if carpeta_ppal in dir:
                path = os.path.join(root, carpeta_ppal) 
    
    # Nombre de los archivos con los datos:
    tabla_file = 'tabla_unica.csv'
    incaa_file = 'cines_INCAA.csv'
    conjunto_file = 'datos_conjuntos.csv'
    
    # Armamos los path para cada archivo:
    path_tabla_f = os.path.join(path,tabla_file)
    path_incaa_f = os.path.join(path, incaa_file)
    path_conjunto_f = os.path.join(path, conjunto_file)
    
    
    ### --- A) Tabla única ---
    tabla = pd.read_csv(path_tabla_f, dtype='string', encoding = 'utf-8')    
    # Agregamos la fecha de hoy, como fecha de carga
    tabla['fecha_carga'] = pd.to_datetime('today').strftime("%d-%m-%Y")
    # Pasamos los nombres de las columnas a minúsculas
    tabla.columns = [utils.str_minuscula(ch) for ch in list(tabla.columns)]
    
    ### --- Armamos las tablas que van a poblar la base de datos (BD) ---
    # Obtenemos los datos para la tabla de la BD: 'provincias'
    provincias = tabla[['id_provincia', 'provincia', 'fecha_carga']
                  ].drop_duplicates(ignore_index=True).sort_values(by='id_provincia')
    
    # Obtenemos los datos para la tabla "departamentos"
    departamentos = tabla[['id_provincia', 'id_departamento', 'fecha_carga']]
    departamentos = departamentos.drop_duplicates(ignore_index=True).sort_values(by='id_provincia')   # ignore_index PUEDE SACARSE
        
    #  --  Obtenemos los datos para la tabla "localidades"
    localidades = tabla[['id_provincia', 'id_departamento', 'cod_localidad','localidad', 'fecha_carga']]
    localidades = localidades.drop_duplicates(ignore_index=True).sort_values(by=['id_provincia','id_departamento','cod_localidad'])
    
    #  --  Obtenemos los datos para la tabla "Categorías"
    categorias = tabla[['categoria','fecha_carga']].drop_duplicates(ignore_index=True)
    
    # -- Datos para la tabla "Info"
    info = tabla[['nombre', 'domicilio', 'codigo postal', 'numero de telefono', 'email', 'web', 'fecha_carga']]
    
    
    ### --- B) Tabla: Cines INCAA ---
    cines_info = pd.read_csv(path_incaa_f, encoding = 'utf-8')
    cines_info.columns = [utils.str_minuscula(ch) for ch in list(cines_info.columns)]
    cines_info.columns
    
    # Agregamos a la tabla "provincias" estas 3 columnas
    provincias_new = pd.merge(provincias, cines_info, on='provincia')
    provincias_new = utils.mover_col_end(provincias_new, 'fecha_carga')
    
    
    ### --- C) Tabla: Datos Conjuntos ---
    # - Por definicion, esta tabla consiste en 3 sub-tablas, una abajo de la otra
    # - Cada sub-tabla comienza con una linea comentada
    
    # 1ra sub-tabla: registros por categoria
    reg_categ = pd.read_csv(path_conjunto_f, skiprows=1, nrows=3, names = ['categoria', 'cantidad'], encoding = 'utf-8')
    
    # 2da sub-tabla: registros por provincia y categoria
    reg_prov_cat = pd.read_csv(path_conjunto_f, skiprows=6, nrows=24*3, names=['provincia', 'categoria', 'cantidad'], encoding = 'utf-8') 
    #  Agregamos fecha de carga
    reg_prov_cat['fecha_carga'] = pd.to_datetime('today').strftime("%d-%m-%Y")
    
    # 3ra sub-tabla: registros por fuente (hay que normalizar los nombres)
    reg_fuente = pd.read_csv(path_conjunto_f, skiprows=8+24*3, names=['fuente', 'cantidad'], encoding = 'utf-8')
    #  Agregamos fecha de carga
    reg_fuente['fecha_carga'] = pd.to_datetime('today').strftime("%d-%m-%Y")
    
    
    # Unimos las tablas 'categorias' con 'reg_categ'
    categoria_new = pd.merge(categorias, reg_categ, on = 'categoria')
    categoria_new = utils.mover_col_end(categoria_new, 'fecha_carga')
    
    
    ### --- Conexión a la Base de Datos ---
    user = config('DB_USER')
    password = config('DB_PASSWORD')
    host = config('DB_HOST')
    port = config('DB_PORT')
    database = config('DB_NAME')
  
    database_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

    engine = create_engine(database_url)
    
    
    def centro_cult(tabla_name):
        ''' 
        Arma la tabla "centros culturales".
        
        INPUT: tabla de datos (dataframe)
        OUTPUT: Devuelve la tabla en formato dataframe
        '''
        # Datos de la tabla 'categoria' (desde la base de datos)
        sql_cat = pd.read_sql_table('tab_categorias', con = engine,
                                    columns = ['id_categoria', 'fecha_carga'])
           
        loc = tabla_name[['id_provincia', 'id_departamento', 'cod_localidad']].reset_index(drop=True)
            
        # Hacemos una especie de "Cross Join" entre 'loc' y "sql_cat"
        loc['key'] = 1
        sql_cat['key'] = 1
        centros_culturales = pd.merge(loc, sql_cat, on='key').drop("key", axis=1)
        return centros_culturales
        
    
    ### --- Creamos tablas y poblamos BD ---
    path_sql = os.path.join(os.getcwd(), 'sql_scripts','Create_Tables.sql')
    
    '''  Creamos las tablas y poblamos algunas - (ejecutar para resetear todo) '''
    with engine.connect() as conn:
        file = open(path_sql, 'r')
        conn.execute(file.read())
        logging.info('Conección y creación de tablas en la base de datos.')
                     
        provincias.to_sql('tab_provincias', con = conn, if_exists='append', index=False)
        departamentos.to_sql('tab_departamentos', con = conn, if_exists='append', index=False)
        localidades.to_sql('tab_localidades', con = conn, if_exists='append', index=False)
        categoria_new.to_sql('tab_categorias', con = conn, if_exists='append', index=False)
        centros_culturales = centro_cult(tabla)
        centros_culturales.to_sql('tab_centro_culturales', con = engine, if_exists='append', index=False)
        reg_fuente.to_sql('tab_fuentes', con = conn, if_exists='append', index=False)
        
    
    logging.info('La información ha sido guardada en la base de datos')

        
    
    
    
    
    
    
    
### ----------------------------------------------------------------
# Hasta acá funciona. Falta insertar los datos en la tabla INFO
### ----------------------------------------------------------------

# ''' Creamos la tabla "INFO" '''
# print(' --- columnas de "t"')
# print(t.columns, '\n shape', t.shape)

# print('\n --- columnas de "centros culturales"')
# cent_cult = pd.read_sql_table('tab_centro_culturales', con = engine)
# print(cent_cult.columns, '\n shape', cent_cult.shape )

# print('\n --- columnas de "categorias"')
# cat = pd.read_sql_table('tab_categorias', con = engine)
# print(cat.columns,  '\n shape',cat.shape)


# cent_cat = cent_cult.merge(cat, on = 'id_categoria', sort = 'cod_localidad')
# cent_cat = cent_cat.drop(['fecha_carga_x', 'fecha_carga_y', 'cantidad'], axis=1)
# print(cent_cat.columns,'\n shape = ', cent_cat.shape)


# t_cat = t.merge(cat, on = ['categoria'])
# t_cat = t_cat.drop(['fecha_carga_x', 'fecha_carga_y', 'cantidad'], axis=1)   # elimino columnas
# print(t_cat.columns, '\n shape = ', t_cat.shape)


# t_cat.merge(cent_cat, on = ['id_provincia', 'id_departamento',
#                             'cod_localidad', 'categoria', 'id_categoria'])
