

### Importamos las librerías
#import requests   
#import re
#import os
#import sys
#from datetime import datetime, date
#import logging

# Seteamos el idioma español para las fechas (funciones: fecha_ultimo_cambio y file_path)
#import locale
#locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')

# Modulo con las funciones creadas
#import utils

import descarga_datos_01 as des
import proces_datos_02 as proc

print('Ejecutando "main.py"...')
des.descarga_datos()
print('\nSe descargaron los datos exitosamente')
proc.proces_datos()
print('\nSe procesaron los datos y crearon 3 archivos .csv exitosamente')



