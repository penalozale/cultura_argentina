# Challenge Data Analytics - Python

## Objetivo
Este proyecto consiste en crear una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos. Dicha información se obtiene de la página oficial del gobierno y hay que procesarla para luego poblar una base de datos PostreSQL. 

## Datos y fuentes
Los datos a utilizar son públicos y se encuentran dentro de https://datos.gob.ar.
 - museos = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d'
 - cines = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae'
 - bibliotecas populares = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7'

## Requisitos
Tener instalado los siguientes programas:
 - Git
 - Python 3
 - PostgreSQL 13

**NOTA**: Los comandos utilizados acá son para usar en sistemas operativos LINUX. Para usuarios de Windows, se aclararán los comandos que difieren a los de linux al lado del otro y entre paréntesis.


## Pasos a seguir
El código va a obtener el link de la tabla de datos y las va a descargar. Luego, va a procesar estos datos y crear tres archivos (tablas). Estos van a contener los datos que van a poblar la base de datos que crearemos por medio de PostgreSQL. 

Recomendamos usar un [entorno virtuales](https://docs.python.org/es/3/tutorial/venv.html) de Python3.

Primero abrir una terminal (puede ser PowerShell de windows o git bash, entre otras), 
ubicarse en el directorio donde se quiere guardar el repositorio y 
seguir los siguientes pasos, ejecutando las siguientes líneas:

 - `git clone https://github.com/penalozale/cultura_argentina.git`
 - `cd cultura_argentina`
 - `python3 -m venv .venv`
 - `source .venv/bin/activate (en Windows: .venv\Scripts\activate)`
 - `pip install -r requirements.txt (en Windows: pip3 install -r requirements.txt)`
 
**Nota**: Antes del paso final, ya que uso la base **"postgres"** que viene por default, 
se debe modificar la variable donde se guarda la contraseña, por la clave que hayas establecido
para dicha base de datos:  **DB_PASSWORD = tu_postgres_db_password**

Por último, luego de clonar el repositorio e instalar las dependencias en el entorno virtual
(.venv), ejecutamos el archivo principal de la siguiente manera:
> python main.py 

## Archivos:
- [main.py](main.py): Programa principal, el cual obtiene los datos y crea la base datos.
- [utils.py](utils.py): Contiene las funciones que se utilizan en el proyecto.
- [a_descarga_datos.py](a_descarga_datos.py): Descarga las tablas de datos de las páginas webs dadas.
- [b_proces_datos.py](b_proces_datos.py): Hace el procesamiento de los datos y guarda tres tablas de datos diferentes, que luego se utilizarán para poblar la base de datos.
- [tareas_correcion.py](tareas_correcion.py): Función que intenta normalizar nombres de localidades (se puede mejorar utilizando la API de la web)
- [c_database.py](c_database.py): Ordena los datos y se insertan en distintas tablas dentro de la base de datos.
- [requirements.txt](requirements.txt): listado de librerías de python que se necesitan para ejecutar los código.
- [info.log](info.log): detalla los distintos procesos por los que pasa el proyecto y si ocurre algún error, acá se debe acudir.
- [.env](.env): datos para la conexión a la base de datos (uso "postgres", que viene por default)
- [sql_scripts](sql_scripts): carpeta donde se encuentra el archivo  
- se encuentra dentro de la carpeta `sql_scripts` y  es el que crea las tablas de la base de datos. 
## Notas finales
A pesar de que pueden aparecer errores al ejecutar el proyecto, sigo trabajando en el mismo para mejorarlo. 
Estoy entusiasmado por la oportunidad de participar de la aceleración, donde aprender mucho más sobre esto, y nada mejor que con prácticas reales.
