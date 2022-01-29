#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import psycopg2
import sys
import utils


# # Buscamos y leemos los archivos
carpeta_ppal = 'Cultura_dataset'

for root, dir, files in os.walk(os.getcwd()):
        if carpeta_ppal in dir:
            path = os.path.join(root, carpeta_ppal) 

print(f'El path de la carpeta {carpeta_ppal} es: {path}')

# Nombre de los archivos con los datos:
tabla_file = 'tabla_unica.csv'
incaa_file = 'cines_INCAA.csv'
conjunto_file = 'datos_conjuntos.csv'

# Armamos los path para cada archivo:
path_tabla_f = os.path.join(path,tabla_file)
path_incaa_f = os.path.join(path, incaa_file)
path_conjunto_f = os.path.join(path, conjunto_file)

# # **A) Tabla única**
# TABLA ÚNICA (dtype=string, x los números q empiezan con 0, si pongo "int" lo pierden)
tabla_unica = pd.read_csv(path_tabla_f, dtype='string')

print('cant de localidades únicas en la tab original ', len(tabla_unica['Localidad'].unique()))
print('cant de codigo localidades únicas en la tab original ', len(tabla_unica['Cod_localidad'].unique()))

''' Hacemos copia de la tabla original '''
t = tabla_unica.copy(deep=True)

''' Agregamos la "fecha de carga" como última columna '''
t['fecha_carga'] = pd.to_datetime('today').strftime("%d-%m-%Y")

''' Pasamos los nombres de las columnas a minúsculas'''
t.columns = [utils.str_minuscula(ch) for ch in list(t.columns)]

# ### para SQL

# Obtenemos los datos para la primer tabla de la BD: 'provincias', (sin filas repetidas)
# eliminando los "pares de valores" duplicados y luego, ordenamos la tabla.
provincias = t[['id_provincia', 'provincia', 'fecha_carga']].drop_duplicates(ignore_index=True).sort_values(by='id_provincia')
print('Provincias = ',len(provincias))

#   --  Obtenemos los datos para la tabla "departamentos"
departamentos = t[['id_provincia', 'id_departamento', 'fecha_carga']]
departamentos = departamentos.drop_duplicates(ignore_index=True).sort_values(by='id_provincia')   # ignore_index PUEDE SACARSE
print('id_prov, id_dpto = ',len(departamentos))

#  --  Obtenemos los datos para la tabla "localidades"
localidades = t[['id_provincia', 'id_departamento', 'cod_localidad','localidad', 'fecha_carga']]
localidades = localidades.drop_duplicates(ignore_index=True).sort_values(by=['id_provincia','id_departamento','cod_localidad'])
print('id_prov, id_dpto, cod_loc, localidad = ',len(localidades))

#  --  Obtenemos los datos para la tabla "Categorías"
categorias = t[['categoria','fecha_carga']].drop_duplicates(ignore_index=True)
print('categorias =', len(categorias))

# -- Datos para la tabla "Info"
info = t[['nombre', 'domicilio', 'codigo postal', 'numero de telefono', 'email', 'web', 'fecha_carga']]
print('INFO table : ',len(info))


# # **B) Tabla: Cines INCAA**
cines_info = pd.read_csv(path_incaa_f)
cines_info.columns = [utils.str_minuscula(ch) for ch in list(cines_info.columns)]
cines_info.columns

# Agregamos a la tabla "provincias" estas 3 columnas
provincias_new = pd.merge(provincias, cines_info, on='provincia')
provincias_new = utils.mover_col_end(provincias_new, 'fecha_carga')


# # **C) Tabla: Datos Conjuntos**
# - Por definicion, esta tabla consiste en 3 tablas, una abajo de la otra
# - Cada sub-tabla comienza con una linea comentada
# - Al final de c/sub-tabla hay una línea en blanco

conjunto = pd.read_csv(path_conjunto_f, names = ['cat_fuent_provcat','rc','rf','rpc']) #, comment='#')

'2 columnas: registros por categoria '
reg_categ = pd.read_csv(path_conjunto_f, skiprows=1, nrows=3, names = ['categoria', 'cantidad'])

'3 columnas: registros por provincia y categoria'
reg_prov_cat = pd.read_csv(path_conjunto_f, skiprows=6, nrows=24*3, names=['provincia', 'categoria', 'cantidad'])
#  Agregamos fecha de carga
reg_prov_cat['fecha_carga'] = pd.to_datetime('today').strftime("%d-%m-%Y")

'2 columnas: registros por fuente, hay que no rmalizar'
reg_fuente = pd.read_csv(path_conjunto_f, skiprows=8+24*3, names=['fuente', 'cantidad'])
#  Agregamos fecha de carga
reg_fuente['fecha_carga'] = pd.to_datetime('today').strftime("%d-%m-%Y")


''' unimos las tablas 'categorias' con 'reg_categ'  '''
categoria_new = pd.merge(categorias, reg_categ, on = 'categoria')
print('\ncategorias_new 1 : ', categoria_new)
categoria_new = utils.mover_col_end(categoria_new, 'fecha_carga')
# print('\ncategorias_new 2 : ', categoria_new)

print(categoria_new.columns)
print(reg_prov_cat.columns)
print(reg_fuente.columns)


# ## **Tablas finales  desde tabla original para BD**
# Conexión a la Base de Datos
database = 'postgres'  # por default
user = 'postgres'      # por default
password = 'abc123'    # se setea al instalar PostgreSQL. (algunas por default: postgres, 1234, )
host = 'localhost'     
port = '5432'          # por default

default_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(default_url)

path_sql = os.path.join(os.getcwd(), 'sql_scripts','Create_Tables.sql')

### Armamos los datos para la tabla "Centros_Culturales"
# Saco la tabla categoria, desde la base de datos, para obtener el id_cat
sql_cat = pd.read_sql_table('tab_categorias', con = engine,
                            columns = ['id_categoria', 'fecha_carga'])
   
loc = t[['id_provincia', 'id_departamento', 'cod_localidad']].reset_index(drop=True)
    
''' Hacemos "CROOS JOIN" entre 'loc' y "sql_cat" ''' 
loc['key'] = 1
sql_cat['key'] = 1
centros_culturales = pd.merge(loc, sql_cat, on='key').drop("key", axis=1)
    

# ## **Creamos tablas y poblamos BD**
'''  Creamos las tablas y poblamos algunas - (ejecutar para resetear todo) '''
with engine.connect() as conn:
    file = open(path_sql, 'r')
    conn.execute(file.read())
    
    logging.info(f'Se han creado las tablas en la base de datos')
    
    provincias.to_sql('tab_provincias', con = conn, if_exists='append', index=False)
    departamentos.to_sql('tab_departamentos', con = conn, if_exists='append', index=False)
    localidades.to_sql('tab_localidades', con = conn, if_exists='append', index=False)
    categoria_new.to_sql('tab_categorias', con = conn, if_exists='append', index=False)
    centros_culturales.to_sql('tab_centro_culturales', con = engine, if_exists='append', index=False)
    reg_fuente.to_sql('tab_fuentes', con = conn, if_exists='append', index=False)
    
    logging.info(f'Se han poblado las tablas con los datos.')
    
'''
Me falta insertar los datos en la tabla INFO.
Y hacer lo de la actualización
'''    


    
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
