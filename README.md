# Challenge Data Analytics - Python

## Objetivo
Este proyecto consiste en crear una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos. Dicha información se obtiene de la página oficial del gobierno y hay que procesarla para luego poblar la base de datos. 

A gran escala, los pasos a seguir son:
 1) Descargar los archivos fuentes.
 2) Procesar los datos y crear tres nuevas tablas.
 3) Crear una Base de datos y las tablas.
 4) Mantener actualizada la Base de Datos.

**NOTA**: Lamentablemente no he terminado el challenge, he llegado hasta el punto 2) inclusive.

## Datos y fuentes
Los datos a utilizar se encuentran dentro de https://datos.gob.ar. 
 - museos = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d'
 - cines = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae'
 - bibliotecas populares = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7'

## Requisitos
Tener instalado los siguientes programas:
 - git
 - python3
 - PostgreSQL (además: libpq-dev)
    - Durante su instalación, en Windows pide una contraseña, pero en Linux no. En linux hay que escribirla a mano: "sudo passwd postgres"

**NOTA**: Los comandos utilizados acá son para usar en sistemas operativos LINUX. Para usuarios de Windows, se aclararán los comandos que difieren a los de linux al lado del otro y entre paréntesis.

## Pasos a seguir
El código va a obtener el link de la tabla de datos y las va a descargar. Luego, va a procesar estos datos y crear tres archivos. Estos van a contener los datos que van a poblar la base de datos que crearemos por medio de PostgreSQL. 

Recomendamos usar un [entorno virtuales](https://docs.python.org/es/3/tutorial/venv.html) de Python3.

Primero abrimos una terminal, nos ubicamos en el directorio donde queramos guardar el repositorio y seguimos los siguientes pasos:
 - git clone https://github.com/penalozale/cultura_argentina.git
 - cd cultura_argentina
 - python3 -m venv .venv
 - source .venv/bin/activate (en Windows: .venv\Scripts\activate)
 - pip3 install -r requirements.txt (en Windows: pip install -r requirements.txt)

Con esto, clonamos el repositorio, creamos un entorno virtual (.venv), lo activamos e instalamos las dependencias que necesita el proyecto.
Una vez tenemos activado el entorno virtual, vamos a ejecutar el archivo **main.py** desde una terminal.
Este va a descargar las fuentes, procesar los datos y crear las tres tablas que solicita el challenge en el apartado "Procesamiento de Datos".

## Archivos:
- En el archivo [Challenge Data Analytics con Python.pdf](Challenge%20Data%20Analytics%20con%20Python.pdf) pueden encontrar todos los detalles del proyecto.
- [main.py](main.py): Programa principal, por el cual se obtienen las tablas y se crea la base datos.
- [utils.py](utils.py): Contiene las funciones que se utilizan en el proyecto.
- [a_descarga_datos.py](a_descarga_datos.py): Descarga las tablas de datos de las páginas webs dadas
- [b_proces_datos.py](b_proces_datos.py): Hace el procesamiento de los datos y guarda tres tablas de datos diferentes, q son las que se van a usar para popular una base de datos SQL.
- [requirements.txt](requirements.txt): listado de librerías de python que se necesitan para ejecutar los códigos.
                         
## Notas finales
Lamentablemente no he alcanzado a crear la base datos y las tablas, que era el objetivo final del desafío. 
De todas maneras, voy a continuar para terminarlo lo antes posible y mantendré actualizado este repositorio hasta lograrlo.
Espero de esta manera poder participar del challenge en esta o la siguiente oportunidad. 
