drop table if exists tab_fuentes cascade;
drop table if exists tab_info cascade;
drop table if exists tab_centro_culturales cascade;
drop table if exists tab_categorias cascade;
drop table if exists tab_localidades cascade;
drop table if exists tab_departamentos cascade;
drop table if exists tab_provincias cascade;

CREATE TABLE IF NOT EXISTS tab_provincias(
						id_provincia INT NOT NULL PRIMARY KEY, 
                        provincia VARCHAR(50) NOT NULL,
                        fecha_carga DATE NOT NULL
                        );
            
CREATE TABLE IF NOT EXISTS tab_departamentos(
                           id_provincia INT NOT NULL REFERENCES tab_provincias(id_provincia),
                           id_departamento INT NOT NULL PRIMARY KEY,
                           fecha_carga DATE NOT NULL,
                           UNIQUE (id_provincia, id_departamento)
                         );                         
 
CREATE TABLE IF NOT EXISTS tab_localidades (
                          id_provincia INT NOT NULL REFERENCES tab_provincias (id_provincia), 
                          id_departamento INT NOT NULL REFERENCES tab_departamentos (id_departamento), 
                          cod_localidad INT NOT NULL PRIMARY KEY,
                          localidad VARCHAR(100) NOT NULL,
                          fecha_carga DATE NOT NULL
                         );

CREATE TABLE IF NOT EXISTS tab_categorias (
							id_categoria INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
							categoria VARCHAR(35) NOT NULL,
							cantidad INT NOT NULL,
							fecha_carga DATE NOT NULL
							);

CREATE TABLE IF NOT EXISTS tab_centro_culturales (
							id_centro_cultural INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
							id_provincia INT NOT NULL REFERENCES tab_provincias (id_provincia), 
                            id_departamento INT NOT NULL REFERENCES tab_departamentos (id_departamento), 
                            cod_localidad INT NOT NULL REFERENCES tab_localidades (cod_localidad),
                            id_categoria INT NOT NULL REFERENCES tab_categorias(id_categoria),
                            fecha_carga DATE NOT NULL
                            );                           

 CREATE TABLE IF NOT EXISTS tab_info (
					 id_contacto INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
					 id_centro_cultural INT NOT NULL REFERENCES tab_centro_culturales (id_centro_cultural), 
                     nombre VARCHAR(100) NOT NULL, 
                     domicilio VARCHAR(100) NOT NULL,
                     codigo_postal VARCHAR(10),
                     numero_de_telefono INT,
                     email VARCHAR(100),
                     web VARCHAR(100),
                     fecha_carga DATE NOT NULL
                   );                           

CREATE TABLE IF NOT EXISTS tab_fuentes (
						id_fuente INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
						fuente VARCHAR(100) NOT NULL,
						cantidad INT NOT NULL,
						fecha_carga DATE NOT NULL
					 );               



--  posting_date DATE NOT NULL DEFAULT CURRENT_DATE
-- SELECT TO_CHAR(NOW() :: DATE, 'dd/mm/yyyy');    -- crea la fecha de hoy en un formato específico
-- https://www.postgresqltutorial.com/postgresql-date/





-- ------------------------------------------------------------------------
-- ------------------------------------------------------------------------

-- -- dentro del create table: 
-- --	FOREIGN KEY (clvae_foranea) REFERENCES tabla_2(calve_primaria_a_la_q_apunta);

-- -- By default, PostgreSQL uses table-name_pkey as the default name for the primary key constraint

-- -- to add a primary key constraint.
-- -- 		ALTER TABLE table_name ADD PRIMARY KEY (column_1, column_2);

-- ------------------------------------------------------------------------
-- ------------------------------------------------------------------------


-- --Probar esto cdo recién instalás el postgreSQL (sacado para MAC)

-- --from sqlalchemy import create_engine
-- --engine = create_engine('postgresql://localhost/[YOUR_DATABASE_NAME]')


-- --In your settings.py, add an entry to your DATABASES setting:


-- --DATABASES = {
-- --   "default": {
-- --        "ENGINE": "django.db.backends.postgresql_psycopg2",
-- --        "NAME": "[YOUR_DATABASE_NAME]",
-- --        "USER": "[YOUR_USER_NAME]",
-- --        "PASSWORD": "",
-- --        "HOST": "localhost",
-- --       "PORT": "",
-- --    }
-- --}
		

