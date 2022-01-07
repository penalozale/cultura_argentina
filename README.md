# Cultura Argentina
Descripción: Challenge de la aceleradora en análisis de datos

## Objetivo
Crear un proyecto que consuma datos desde tres fuentes distintas para popular una base de datos SQL
con información cultural sobre bibliotecas, museos y salas de cines argentinos.

## Requerimientos funcionales
El proyecto deberá cumplir con una serie de requerimientos funcionales que giran
en torno a cuatro ejes centrales:
 - a) los archivos fuentes ( si el archivo existe debe reemplazarse. La fecha de la nomenclatura es la fecha de descarga)
 - b) el procesamiento de datos,
 - c) la creación de tablas en la base de datos y  
 - d) la actualización de la base de datos.


## Archivos:
- En el archivo "Challenge Data Analytics con Python.pdf" pueden encontrar todos los detalles del proyecto.
- 01_tablas.ipynb: descarga las tablas de datos de las páginas webs dadas
- 02_Procesamiento.ipynb: hace el procesamiento de los datos y guarda 3 tablas de datos diferentes,
                         q son las que se van a usar para popular una base de datos SQL.


                         



# Intrucciones para usar entornos virtuales de python
Para usar entornos virtuales de Python (venv o virtualenv) instalados con el gestor de paquetes PIP en el entorno de ejecución de código Jupyter debemos de usar los pasos que se indican a continuación. De esta forma tendremos las librerías cargadas independientemente entre los distintos Kernels de ejecución del sistema.

 - Acceso al sistema
Primero debemos de crear el entorno virtual en nuestro sistema, en donde tengamos Jupyter instalado.

 - Acceso desde la terminal de Jupyter
Podemos acceder al Sistema Operativo accediendo desde la terminal de la interfaz Web, ya que esta muestra el Prompt del propio sistema en donde se encuentra corriendo Jupyter.  (New/Terminal)

 - Crear directorio para el entorno
Es buena práctica crear un directorio para los Notebooks que usaremos en este entorno virtual. Por ejemplo, vamos a crear un entorno para el Challenge, por lo que creamos el directorio y nos situamos en el mismo:
        **mkdir Alkemy**
        **cd Alkemy**
 
 - Crear y configurar el entorno virtual con python 3:
Si no tenemos el paquete necesario para hacerlo, debemos instalarlo, para que corra con python 3, usamos pip3:
    **pip3 install virtualenv**
Creamos el entorno virtual, por ej: Challenge202, indicando la versión de Python que queremos que corra en este entorno. (Usamos un punto al inicio del nombre del entorno para que este sea oculto y no se muestre en el listado de archivos y Notebooks del directorio en Jupyter):
   **python3 -m venv Challenge2022**  ¿ y/o ?
   
   **virtualenv env**  --> Este creará un directorio "env" que contiene a los directorios: bin ("Scripts" en Windows) , include y lib
   **virtualenv .p /usr/bin/python3.8 env**
   
Necesitarás el comando completo para el virtualenv de la versión de Python, corre entonces lo siguiente para verlo.
   **which virtualenv**
   






