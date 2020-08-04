/*****************************************************/
/*3.  Total de casos positivos confirmados por país.**/
/* Primero creamos una tabal countries_data en la que*/
/* seleccionamos los valores más recientes de cada ***/
/* provincia o localización.                       ***/
/* Sobre esta tabla agrupamos el total de confirmados*/
/* por país (para todas las provincias) y sustituimos*/
/* el id del país por su nombre.                     */
/*****************************************************/

WITH countries_data
AS
   (	   
	     SELECT   f.id_location                     AS id_location,
                  f.confirmed                       AS confirmed,
				  f.id_date                         AS id_date,
				  ROW_NUMBER() OVER 
				      (PARTITION BY (f.id_location)
                       ORDER     BY f.id_date DESC) AS rn1
         FROM     fact_covid_19 f
    )
	
SELECT   cr.name           AS country_region,
         SUM(c.confirmed)  AS total_confirmed
FROM     countries_data c
JOIN     dim_location l
ON       c.id_location = l.id_location
JOIN     dim_country_region cr
ON       l.id_country_region = cr.id_country_region
WHERE    (c.rn1 = 1)
GROUP BY 1
ORDER BY 2 DESC;

/******************************************************/
/* 4. Ratio de mortalidad del virus como              */
/* 100 * Numero de fallecidos / Numero de Confirmados.*/
/* Almacena este dato en la misma tabla que has creado*/ 
/* para guardar los datos. Usa ALTER TABLE y UPDATE   */
/******************************************************/

/* Añadimos la nueva columna deaths_ratio             */

ALTER  TABLE  covid_19.fact_covid_19 
ADD    COLUMN deaths_ratio FLOAT NULL 
AFTER  recovered;

/* Añadimos los datos a la nueva columna              */

UPDATE fact_covid_19
SET    deaths_ratio = CASE
       WHEN confirmed > 0 THEN deaths / confirmed * 100
       WHEN confirmed = 0 THEN 0
       END
WHERE  id >= 0;


/* Hemos incluido la key en la consulta para no tener  */
/* que modificar el safe mode, aunque podríamos haberlo*/
/* desactivado con 'SET SQL_SAFE_UPDATES = 0;' he      */
/* preferido hacerlo así.                              */

          