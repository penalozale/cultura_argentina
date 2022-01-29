# Challenge Data Analytics - Python

## Objetivo
Este proyecto consiste en crear una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos. Dicha información se obtiene de la página oficial del gobierno y hay que procesarla para luego poblar la base de datos. 

**NOTA**: Lamentablemente no está terminado el challenge completamente. Además de algunas cosas por corregir (en eso sigo)

## Datos y fuentes
Los datos a utilizar son públicos y se encuentran dentro de https://datos.gob.ar.
 - museos = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d'
 - cines = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae'
 - bibliotecas populares = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7'

## Requisitos
Tener instalado los siguientes programas:
 - git
 - python3
 - PostgreSQL (además: libpq-dev)

**NOTA**: Los comandos utilizados acá son para usar en sistemas operativos LINUX. Para usuarios de Windows, se aclararán los comandos que difieren a los de linux al lado del otro y entre paréntesis.


## Pasos a seguir
El código va a obtener el link de la tabla de datos y las va a descargar. Luego, va a procesar estos datos y crear tres archivos (tablas). Estos van a contener los datos que van a poblar la base de datos que crearemos por medio de PostgreSQL. 

Recomendamos usar un [entorno virtuales](https://docs.python.org/es/3/tutorial/venv.html) de Python3.

Primero abrir una terminal, ubicarse en el directorio donde se quiere guardar el repositorio y seguir los siguientes pasos:
 - git clone https://github.com/penalozale/cultura_argentina.git
 - cd cultura_argentina
 - python3 -m venv .venv
 - source .venv/bin/activate (en Windows: .venv\Scripts\activate)
 - pip3 install -r requirements.txt (en Windows: pip install -r requirements.txt)

Con esto, se clona el repositorio, se crea un entorno virtual (.venv), se activa e instala las dependencias que necesita el proyecto.
Una vez se tiene activado el entorno virtual, ejecutar el archivo **main.py**.
Este se encargará de descargar los datos, crear los archivos en sus carpetas correspondientes y poblar una base de datos PostgreSQL.

## Archivos:
- [main.py](main.py): Programa principal, el cual obtiene los datos y crea la base datos.
- [utils.py](utils.py): Contiene las funciones que se utilizan en el proyecto.
- [a_descarga_datos.py](a_descarga_datos.py): Descarga las tablas de datos de las páginas webs dadas.
- [b_proces_datos.py](b_proces_datos.py): Hace el procesamiento de los datos y guarda tres tablas de datos diferentes, que luego se utilizarán para poblar la base de datos.
- [tareas_correcion.py](tareas_correcion.py): Función que intenta normalizar nombres de localidades (se puede mejorar utilizando la API de la web)
- [c_database.py](c_database.py): Ordena los datos y se insertan en distintas tablas dentro de la base de datos.
- [requirements.txt](requirements.txt): listado de librerías de python que se necesitan para ejecutar los código.
- [info.log](info.log): detalla los distintos procesos por los que pasa el proyecto y si ocurre algún error, acá se debe acudir.
                         
## Notas finales
A pesar de que pueden aparecer errores al ejecutar el proyecto, sigo trabajando en el mismo para mejorarlo. 
Estoy entusiasmado por la oportunidad de participar de la aceleración, donde aprender mucho más sobre esto, y nada mejor que con prácticas reales.
