# Programa principal
# Challenge - Data analytics

import a_descarga_datos as des
import b_proces_datos as proc

# Se descargan los datos de las fuentes
des.descarga_datos()

# Se procesan dichos datos y se crean las tres tablas solicitadas
print('\nCreando las tablas...')
proc.proces_datos()