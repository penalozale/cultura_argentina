
import utils as ut
import pandas as pd

# Nota: Tengo que corregir muchas cosas de acá, 
#       ya que tal vez con la API se pueden corregir.

def correcciones(df):
    ''' 
    Hacemos algunas correciones en nombres de localidades
    y algunos códigos de las mismas.
    Además, ponemos en minúsculas la columna'Localidades'
    INPUT: df = df de datos (dataframe)
    '''
    ### Cambiamos la localidad "Ciudad de Buenos Aires"
    df.loc[(df.Localidad == 'Ciudad de Buenos Aires'),
              'Localidad'] = 'Ciudad Autónoma de Buenos Aires'
    
    ut.estand_escritura(df, 'Localidad')

    ### Cambiamos la localidad "capital" por el nombre de su provincia
    df.loc[df["Localidad"].str.lower() == 'capital', 'Localidad'] = df['Provincia']
    ut.estand_escritura(df, 'Localidad')
    
    ### Verificamos que los códigos de las provincias estén bien.
    # Definimos los códigos geográficos de las Provincias
    datos = {
        'Id_provincia' : ['02', '06', '10', '14', '18', '22', '26', '30', '34',
                          '38', '42', '46', '50', '54', '58', '62', '66', '70',
                          '74', '78', '82', '86', '90', '94'],
        'Provincia': ['Ciudad Autonoma de Buenos Aires', 'Buenos Aires',
                      'Catamarca', 'Córdoba', 'Corrientes', 'Chaco',
                      'Chubut', 'Entre Ríos', 'Formosa', 'Jujuy', 'La Pampa',
                      'La Rioja', 'Mendoza', 'Misiones', 'Neuquén',
                      'Río Negro', 'Salta', 'San Juan', 'San Luis', 'Santa Cruz',
                      'Santa Fé', 'Santiago del Estero', 'Tucumán',
                      'Tierra del Fuego']
        }
    codigos_prov = pd.DataFrame(datos)
    
    for key, value in codigos_prov.values:
        # Dataframe de la provincia: 'value'
        xx = df[df['Provincia']==value]
        
        # Correjimos: Provincia ID
        if any(xx['Id_provincia'] != key):
            df.loc[df['Provincia'] == value, 'Id_provincia'] = key
        
        # Verificamos también: Departamento ID y Localidad ID
        ut.corr_id_dpto_loc(df, 'Id_departamento', prov_name = value, prov_id = key)
        ut.corr_id_dpto_loc(df, 'Cod_localidad', prov_name = value, prov_id = key)
        
    ### Cambio Nombres de Localidades
    
    # "embalse, rio tercero" por "embalse", 
    # y cod de localidad 14007210 por 14007060
    if 'embalse, rio tercero' in df.values:
        condicion = df['Localidad']=='embalse, rio tercero'
        df.loc[condicion, 'Cod_localidad'] = '14007060'
        ut.cambio_localidad(df, 'Córdoba', 'embalse, rio tercero', 'embalse')
        
    ut.cambio_localidad(df, 'Mendoza', 'general guti,rrez', 'maipu' )
    ut.cambio_localidad(df, 'Neuquén', "lago barreales, cerca de mari menuco", 'mari menuco')
    ut.cambio_localidad(df, 'Neuquén', "neuqu,n" , 'neuquen')
    ut.cambio_localidad(df, 'Buenos Aires', 'gonzales chaves', 'adolfo gonzalez chaves')
    ut.cambio_localidad(df, 'San Juan', "villa seminario, rivadavia", 'rivadavia')
    
    
    ### Nombre de municipios en lugar de la Localidad
    
    ut.corr_localidad(df, '06028010', 'almirante_brown')
    ut.corr_localidad(df, '06035010', 'avellaneda')
    ut.corr_localidad(df, '06056010', 'bahia blanca') 
    ut.corr_localidad(df, '06091010', 'berazategui')  
    ut.corr_localidad(df, '06098010', 'berisso') 
    ut.corr_localidad(df, '06245010', 'ensenada') 
    ut.corr_localidad(df, '06252010', 'escobar')  
    ut.corr_localidad(df, '06260010', 'esteban echeverria')
    ut.corr_localidad(df, '06270010', 'ezeiza') 
    ut.corr_localidad(df, '06274010', 'florencio varela')
    ut.corr_localidad(df, '06315010', 'general juan madariaga')
    ut.corr_localidad(df, '06322010', 'general la madrid')
    ut.corr_localidad(df, '06371010', 'general san martín')
    ut.corr_localidad(df, '06408010', 'hurlingham')  
    ut.corr_localidad(df, '06410010', 'ituzaingo') 
    ut.corr_localidad(df, '06420020', 'mar de ajo san bernardo') 
    ut.corr_localidad(df, '06420030', 'san clemente del tuyu')
    ut.corr_localidad(df, '06420040', 'santa teresita mar del tuyu')
    ut.corr_localidad(df, '06427010', 'la matanza') 
    ut.corr_localidad(df, '06434010', 'lanus') 
    ut.corr_localidad(df, '06441030', 'la plata')
    ut.corr_localidad(df, '06483040', 'lobos') 
    ut.corr_localidad(df, '06490010', 'lomas de zamora')
    ut.corr_localidad(df, '06497060', 'lujan') 
    ut.corr_localidad(df, '06515010', 'malvinas argentinas')
    ut.corr_localidad(df, '06539010', 'merlo') 
    ut.corr_localidad(df, '06560010', 'moreno')
    ut.corr_localidad(df, '06568010', 'moron')
    # correjimos Id_departamento, moron = 06568
    cond1 = df['Cod_localidad']=='06568010'
    df.loc[cond1, 'Id_departamento'] = df.loc[cond1, 'Cod_localidad'].str.slice(0,5)
    
    ut.corr_localidad(df, '06581040', 'necochea quequen')
    ut.corr_localidad(df, '06623070', 'manueal ocampo')  
    ut.corr_localidad(df, '06638040', 'pilar')  
    ut.corr_localidad(df, '06644010', 'pinamar')
    ut.corr_localidad(df, '06658010', 'quilmes')
    ut.corr_localidad(df, '06749010', 'san fernando') 
    ut.corr_localidad(df, '06756010', 'san isidro')  
    ut.corr_localidad(df, '06760010', 'san miguel') 
    ut.corr_localidad(df, '06763050', 'san nicolas de los arroyos')
    ut.corr_localidad(df, '06778020', 'san vicente')  
    ut.corr_localidad(df, '06791050', 'tandil')  
    ut.corr_localidad(df, '06805010', 'tigre')  
    ut.corr_localidad(df, '06840010', 'tres de febrero')
    ut.corr_localidad(df, '06847020', 'tres lagunas')  
    ut.corr_localidad(df, '06861010', 'vicente lopez') 
    ut.corr_localidad(df, '10035020', 'belen')  
    ut.corr_localidad(df, '10049030', 'san fernando del valle de catamarca')
    ut.corr_localidad(df, '10063010', 'collagasta')
    ut.corr_localidad(df, '10112040', 'san isidrio')
    ut.corr_localidad(df, '14014010', 'cordoba')   
    ut.corr_localidad(df, '14049050', 'dean funes')
    ut.corr_localidad(df, '14091110', 'la cumbre') 
    ut.corr_localidad(df, '14098290', 'vicuña mackenna')
    ut.corr_localidad(df, '26007030', 'puerto piramides')
    ut.corr_localidad(df, '26105010', 'gan gan')  
    ut.corr_localidad(df, '30008020', 'colon')  
    ut.corr_localidad(df, '38014090', 'perico') 
    ut.corr_localidad(df, '38021060', 'san salvador de jujuy') 
    ut.corr_localidad(df, '38035080', 'libertador grl. san martin')
    ut.corr_localidad(df, '38042040', 'palpala')  
    ut.corr_localidad(df, '38063180', 'san pedro')
    ut.corr_localidad(df, '38094040', 'maimara')  
    ut.corr_localidad(df, '42077030', 'general san martin')
    ut.corr_localidad(df, '42105020', 'dorila')  
    ut.corr_localidad(df, '42105030', 'general pico')
    ut.corr_localidad(df, '46042010', 'chilecito')   
    ut.corr_localidad(df, '50007010', 'mendoza')   
    ut.corr_localidad(df, '50014030', 'general alvear')
    ut.corr_localidad(df, '50021010', 'godoy cruz')
    ut.corr_localidad(df, '50028020', 'guaymallen')
    ut.corr_localidad(df, '50035020', 'junin')   
    ut.corr_localidad(df, '50049050', 'las heras')
    ut.corr_localidad(df, '50063090', 'lujan de cuyo')
    ut.corr_localidad(df, '50070060', 'maipu')
    ut.corr_localidad(df, '50091030', 'eugenio bustos')
    ut.corr_localidad(df, '50098100', 'san martin')  
    ut.corr_localidad(df, '50105210', 'san rafael')  
    ut.corr_localidad(df, '50105220', '25 de mayo')  
    ut.corr_localidad(df, '54042020', 'eldorado')
    ut.corr_localidad(df, '54056030', 'san vicente')
    ut.corr_localidad(df, '58035040', 'cutral co')  
    ut.corr_localidad(df, '58042010', 'chos malal') 
    ut.corr_localidad(df, '62007080', 'san javier') 
    ut.corr_localidad(df, '62021060', 'san carlos de bariloche')   
    ut.corr_localidad(df, '62042450', 'general roca')
    ut.corr_localidad(df, '62077010', 'las grutas')  
    ut.corr_localidad(df, '66028050', 'salta')   
    ut.corr_localidad(df, '66049040', ' general güemes')
    ut.corr_localidad(df, '66112040', 'san jose de metan')
    ut.corr_localidad(df, '66126070', 'san ramon de la nueva oran')
    ut.corr_localidad(df, '66147030', 'rosario de lerma') 
    ut.corr_localidad(df, '70007020', 'villa general san martin')
    ut.corr_localidad(df, '70028010', 'san juan')  
    ut.corr_localidad(df, '70056080', 'san jose de jachal')
    ut.corr_localidad(df, '70077010', 'rawson')   
    ut.corr_localidad(df, '70077020', 'villa bolaños')
    ut.corr_localidad(df, '70084010', 'rivadavia')    
    ut.corr_localidad(df, '70119060', 'villa san agustin')
    ut.corr_localidad(df, '74007070', 'san francisco del monte de oro')
    ut.corr_localidad(df, '74035030', 'justo daract')
    ut.corr_localidad(df, '74049060', 'merlo')
    ut.corr_localidad(df, '74049070', 'santa rosa del conlara')  
    ut.corr_localidad(df, '82021010', 'aldao')   
    ut.corr_localidad(df, '82021160', 'estacion clucellas')
    ut.corr_localidad(df, '82021350', 'santa clara de saguier')  
    ut.corr_localidad(df, '82028140', ' maximo paz')
    ut.corr_localidad(df, '82035020', 'helvecia')  
    ut.corr_localidad(df, '82133170', 'vera')
    ut.corr_localidad(df, '86049110', 'santiago del estero')
    ut.corr_localidad(df, '86147150', 'villa rio hondo')
    ut.corr_localidad(df, '90084010', 'san miguel de tucuman')

    return


