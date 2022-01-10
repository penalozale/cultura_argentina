
### Cargamos las librerías
import utils
import logging
import locale
locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')

def descarga_datos():
    
    ### URLs dadas, de donde descargamos las tablas de datos
    url_museos = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d'
    url_cines = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae'
    url_bibliotecas = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7'

    # Lista con las paginas webs.
    urls = ['url_museos', 'url_cines', 'url_bibliotecas']

    # Creamos el archivo "info.log"
    logging.basicConfig(filename= 'info.log', format='%(asctime)s : %(levelname)s : %(message)s',
                        datefmt='%d/%m/%y %H:%M:%S', level=logging.INFO,
                        filemode = 'w', force=True)
    logging.info('EJECUTANDO LA DESCARGA DE LOS DATOS... ')

    # Ejecutamos las funciones para descargar las tablas de datos
    for site in urls:
        print(f'guardando la tabla de {site}')
        link = utils.obtener_link(eval(site))
        tabla = utils.descargar_tabla(link)
        path = utils.file_path(link)    
        utils.guardar_archivo_bin(path, tabla)

    logging.info('.........Terminó la descarga de las tablas (1ra Parte) ')
    print('\n.........Terminó la descarga de las tablas (1ra Parte) ')
