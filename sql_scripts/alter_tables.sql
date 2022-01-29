ALTER TABLE tab_provincias
  ALTER COLUMN id_provincIa TYPE int USING id_provincia::integer,
  ADD PRIMARY KEY (id_provincia),
  ALTER COLUMN provincia TYPE varchar(60),
  ALTER COLUMN provincia SET NOT NULL;



CREATE TABLE IF NOT EXISTS tab_departamentos(
                           id_provincia INT NOT NULL REFERENCES tab_provincias(id_provincia),
                           id_departamento INT NOT NULL PRIMARY KEY       --  UNIQUE (id_provincia, id_departamento)
                         );         

ALTER TABLE tab_departamentos
  ALTER COLUMN id_provincia TYPE int USING id_provincia::integer,
  ALTER COLUMN id_provincia SET NOT NULL,  
  ADD PRIMARY KEY (id_departamento),
  ALTER COLUMN id_departamento TYPE int USING id_departamento::integer;
  
  ADD FOREIGN KEY (id_provincia) REFERENCES tab_provincia(id_provincia),
  
  ADD CONSTRAINT tab_departamentos_id_provincia_fkey FOREIGN KEY (id_provincia) REFERENCES tab_provincia (id_provincia);
  ;
  
PROVINCIAS:
Indexes:
    "tab_provincias_pkey" PRIMARY KEY, btree (id_provincia)
Referenced by:
    TABLE "tab_departamentos" CONSTRAINT "tab_departamentos_id_provincia_fkey" FOREIGN KEY (id_provincia) REFERENCES tab_provincias(id_provincia)
    TABLE "tab_localidades" CONSTRAINT "tab_localidades_id_prov_fkey" FOREIGN KEY (id_prov) REFERENCES tab_provincias(id_provincia)

LOCALIDADES:
Indexes:
    "tab_departamentos_pkey" PRIMARY KEY, btree (id_departamento)
Foreign-key constraints:
    "tab_departamentos_id_provincia_fkey" FOREIGN KEY (id_provincia) REFERENCES tab_provincias(id_provincia)
Referenced by:
    TABLE "tab_localidades" CONSTRAINT "tab_localidades_id_dpto_fkey" FOREIGN KEY (id_dpto) REFERENCES tab_departamentos(id_departamento)










CREATE TABLE IF NOT EXISTS tab_localidades (
                          id_prov INT NOT NULL REFERENCES tab_provincias (id_provincia), 
                          id_dpto INT NOT NULL REFERENCES tab_departamentos (id_departamento), 
                          cod_localidad INT NOT NULL PRIMARY KEY,
                          localidad VARCHAR(100) NOT NULL
                         );

ALTER TABLE tab_
  ALTER COLUMN id_provincIa TYPE int USING id_provincia::integer,
  ADD PRIMARY KEY (id_provincia),
  ALTER COLUMN provincia TYPE varchar(60),
  ALTER COLUMN provincia SET NOT NULL;







--ALTER TABLE table_name ADD COLUMN column_name SERIAL PRIMARY KEY;
--ALTER TABLE table_name DROP CONSTRAINT primary_key_to_delete;



--It is rare to define a primary key for existing table. In case you have to do it, 
-- -- you can use the ALTER TABLE statement to add a primary key constraint.
-- -- 			ALTER TABLE table_name ADD PRIMARY KEY (column_1, column_2);

-- -- How to add an auto-incremented primary key to an existing table:
-- -- 			ALTER TABLE table_name ADD COLUMN column_name SERIAL PRIMARY KEY;

-- -- To remove an existing primary key constraint, 
-- -- you also use the ALTER TABLE statement with the following syntax:
-- -- 			ALTER TABLE table_name DROP CONSTRAINT primary_key_to_delete;
