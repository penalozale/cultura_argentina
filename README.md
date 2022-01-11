# Challenge Data Analytics - Python
## Objetivo
Este proyecto consiste en crear una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos. Dicha información se obtiene de la página oficial del gobierno y hay que procesarla para luego poblar la base de datos. A continuación enunciaremos los pasos a seguir.

## Requisitos
Tener instalado los siguientes programas:
 - python3
 - PostgreSQL

## Pasos a seguir
En resumen, el código va a obtener el link de la tabla de datos y las va a descargar. Luego, va a procesar estos datos y crear tres archivos. Estos van a contener los datos que van a poblar la base de datos que crearemos por medio de PostgreSQL. 

Recomendamos usar un [entorno virtuales](https://docs.python.org/es/3/tutorial/venv.html) de Python3.
Primero abrimos una terminal y seguimos los siguientes pasos:
 - git clone https://github.com/penalozale/cultura_argentina.git   # me descarga el repositorio en una carpeta llamada "cultura_argentina"
 - cd cultura_argentina
 - python3 -m venv .venv
 - source .venv/bin/activate
 - pip install -r requirements.txt

Con esto, clonamos el repositorio, creamos un entorno virtual (.venv), lo activamos e instalamos las dependencias que necesita el proyecto. 




Los datos a utilizar se encuentran dentro de https://datos.gob.ar. 
 - museos = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d'
 - cines = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae'
 - bibliotecas populares = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7'

## Idea


## Requerimientos funcionales
El proyecto deberá cumplir con una serie de requerimientos funcionales que giran
en torno a cuatro ejes centrales:
 - a) los archivos fuentes ( si el archivo existe debe reemplazarse. La fecha de la nomenclatura es la fecha de descarga)
 - b) el procesamiento de datos,
 - c) la creación de tablas en la base de datos y  
 - d) la actualización de la base de datos.


## Archivos:
- En el archivo [Challenge Data Analytics con Python.pdf](Challenge%20Data%20Analytics%20con%20Python.pdf) pueden encontrar todos los detalles del proyecto.
- [01_tablas.ipynb](01_tablas.ipynb): descarga las tablas de datos de las páginas webs dadas
- [02_Procesamiento.ipynb](02_Procesamiento.ipynb): hace el procesamiento de los datos y guarda 3 tablas de datos diferentes,
                         q son las que se van a usar para popular una base de datos SQL.


                         



# Intrucciones para usar entornos virtuales de python
Utilizaremos entornos virtuales ya que, de esta forma, tendremos las librerías cargadas independientemente entre los distintos Kernels de ejecución del sistema.
___Se recomienda que la carpeta para el entorno virtual sea una subcarpeta de Python al que está asociado.  ¿ ?

  1) Desde la terminal del sistema, vamos a crear un directorio para el entorno y vamos a ubicarnos en este:
      **mkdir python-virtual-env && cd python-virtual-env**
      
  2) Creamos el entorno:
      Linux: python2 : **virtual-env env**
             python3 : **python3 -m venv env**
      Windows: **python -m venv env**
     
     , esto creará un carpeta "env" con: el archivo pyenv.cfg y tres subcarpetas: bin ("Scripts" en windows), include y lib.
  
  3) Activamos el entorno:
      Linux: **source env/bin/activate**
      Windows: **bin\activate**        --------------------->  C O R R E G I R   !!!!!!!
     
     , veremos que aparecerá el nombre del entorno delante del prompt.

Una vez que tenemos el entorno virtual activado, debemos instalar todas las librerías que vamos a utilizar dentro del mismo. Tener en cuenta que para que los siguientes comandos funcionen en windows, se asume que python está incluido en las variables del sistema.
 
 - instalar nuevo paquete:    **pip install nombre_paquete**  (instalará todas las dependencias también)
 - eliminar paquete:    **pip uninstall nombre:paquete**  (NO desintalará las dependencias)
 - listar paquetes instalados: **pip list** 
     ó podemos usar: **pip freeze > requirements.txt** , y obtenemos de esta manera la lista de paquetes instalados en un archivo llamado: "requirements".


 


   




  - Luego, creamos y configurar el entorno virtual con python 3:
Si no tenemos el paquete necesario para hacerlo, debemos instalarlo, para que corra con python 3, usamos pip3:
    **pip3 install virtualenv**
Creamos el entorno virtual, por ej: Challenge2022, indicando la versión de Python que queremos que corra en este entorno. (Usamos un punto al inicio del nombre del entorno para que este sea oculto y no se muestre en el listado de archivos y Notebooks del directorio en Jupyter):
   **python3 -m venv Challenge2022**  ¿ y/o ?
   
   **virtualenv env**  --> Este creará un directorio "env" que contiene a los directorios: bin ("Scripts" en Windows) , include y lib
   **virtualenv .p /usr/bin/python3.8 env**
   
Necesitarás el comando completo para el virtualenv de la versión de Python, corre entonces lo siguiente para verlo.
   **which virtualenv**
   






