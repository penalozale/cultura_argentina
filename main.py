# Programa principal
# Alkemy Challenge - Data analytics con Python

import a_descarga_datos as des
import b_proces_datos as proc
import c_database as db

if __name__ == "__main__":
    # Se descargan los datos de las fuentes
    des.descarga_datos()
    
    # Se procesan dichos datos y se crean las tres tablas solicitadas
    print('\nCreando las tablas...')
    proc.proces_datos()
    
    # Creamos y poblamos con datos la base de datos
    print('\nCreando DB...')
    db.database()

    print(' - La información ha sido guardada en la base de datos')
    