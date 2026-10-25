--encuesta
DELETE FROM encuesta 
WHERE encuestaID  = 2014 

--ayuda laboral
DELETE FROM ayuda_laboral  
WHERE encuestaID  = 2014 
--orden de los usuarios 
CREATE TABLE ayuda_laboral_temp AS 
SELECT 
    ROW_NUMBER() OVER (ORDER BY participanteID) AS participanteID,
    ayuda_laboral.*
FROM ayuda_laboral;
DROP TABLE ayuda_laboral ;
ALTER TABLE ayuda_laboral_temp RENAME TO Ayuda_Laboral;

UPDATE ayuda_laboral 

--categoria laboral
DELETE FROM categoria_laboral 
WHERE encuestaID  = 2014 
--nuevo orden de los pacientes
CREATE TABLE categoria_laboral_temp AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY participanteID) AS participanteID,
    encuestaID,
    puesto_trabajoID,
    trabajo_remoto,
    paisID,
    estado_eeuuID,
    independiente_trabajo,
    rol_trabajo_estech,
    compania_estech,
    primer_trabajo
FROM categoria_laboral
DROP TABLE categoria_laboral;
ALTER TABLE categoria_laboral_temp RENAME TO Categoria_Laboral;
    --colimnas compania_estech y primer trabajo 
SELECT 
    participanteID , 
    compania_estech, 
    primer_trabajo
FROM categoria_laboral
WHERE compania_estech IS NOT NULL AND primer_trabajo IS NOT NULL;

SELECT 
    participanteID,
    COALESCE(compania_estech, 'Not applicable / No experience') AS compania_estech,
    COALESCE(primer_trabajo, 'Not applicable / No experience') AS primer_trabajo
FROM categoria_laboral;

UPDATE categoria_laboral
SET 
    compania_estech = COALESCE(compania_estech, 'Not applicable / No experience'),
    primer_trabajo = COALESCE(primer_trabajo, 'Not applicable / No experience');

--participante
BEGIN TRANSACTION;
DELETE FROM encuesta 
WHERE encuestaID  = 2014;

DELETE FROM participante 
WHERE participanteID NOT IN (
    SELECT participanteID FROM encuesta
);

--borrando 2014 y ennumerado nuevamente los participantes 
CREATE TABLE participante_temp AS 
SELECT 
    ROW_NUMBER() OVER (ORDER BY participanteID) AS participanteID,
    edad,
    generoID,
    paisID,
    estado_EEUUID,
    raza
FROM participante;

DROP TABLE participante;
ALTER TABLE participante_temp RENAME TO participantes;

--edad 
SELECT ROUND(
    (SUM(p.edad * 
        CASE 
            WHEN pt.nivel_jerarquico = 'Operativo' THEN 1
            WHEN pt.nivel_jerarquico = 'Coordinación' THEN 2
            WHEN pt.nivel_jerarquico = 'Directivo' THEN 3
            ELSE 0 
        END
    ) * 1.0) / 
    NULLIF(SUM(
        CASE 
            WHEN pt.nivel_jerarquico = 'Operativo' THEN 1
            WHEN pt.nivel_jerarquico = 'Coordinación' THEN 2
            WHEN pt.nivel_jerarquico = 'Directivo' THEN 3
            ELSE 0 
        END
    ), 0), 2
) AS media_ponderada_calculada
FROM participantes p
JOIN Categoria_Laboral cl ON cl.participanteID = p.participanteID
JOIN puesto_trabajo pt ON cl.puesto_trabajoID = pt.puesto_trabajoID 
WHERE p.edad BETWEEN 18 AND 75
  AND cl.encuestaID = 2016 
  AND pt.nivel_jerarquico IS NOT NULL;
	
PRAGMA foreign_keys = OFF;
	
CREATE TABLE trabajo_2016 (
	    participanteID   INTEGER NOT NULL,
	    encuestaID       INTEGER NOT NULL,
	    puesto_trabajoID INTEGER NOT NULL,
	    trabajo_remoto   TEXT,
	    PRIMARY KEY (participanteID, encuestaID),
	    FOREIGN KEY (participanteID)   REFERENCES participantes(participanteID),
	    FOREIGN KEY (encuestaID)       REFERENCES encuesta(encuestaID),
	    FOREIGN KEY (puesto_trabajoID) REFERENCES puesto_trabajo(puesto_trabajoID)
	);

--estado mental
DELETE FROM Estado_Mental  
WHERE encuestaID  = 2014 
CREATE TABLE estado_mental_temp AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY participanteID) AS participanteID,
    encuestaID,
    diagnostico_oficial,
    cobertura_incluye_sm,
    busco_tratamiento,
    diagnosticoID
FROM Estado_mental;
DROP TABLE estado_mental ;
ALTER TABLE Estado_Mental_temp   RENAME TO Estado_Mental;

---cobertura 
SELECT 
    cobertura_incluye_sm,
    COUNT(*) AS total_registros
FROM estado_mental
GROUP BY cobertura_incluye_sm;

SELECT 
    CASE cobertura_incluye_sm
        WHEN 1 THEN 'Yes'
        WHEN 0 THEN 'No'
        WHEN -1 THEN 'Not applicable' -- O el texto que prefieras para el -1
        ELSE 'Unknown'
    END AS cobertura_incluye_sm,
    COUNT(*) AS total_registros
FROM estado_mental
GROUP BY cobertura_incluye_sm;

UPDATE estado_mental
SET cobertura_incluye_sm = CASE cobertura_incluye_sm
    WHEN '1' THEN 'Yes'
    WHEN '0' THEN 'No'
    WHEN '-1' THEN 'Not applicable'
    ELSE 'Unknown'
END;

--impacto profesional 

CREATE TABLE impacto_profesional_temp AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY participanteID) AS participanteID,
    encuestaID,
    afecta_carrera,
    afecta_productividad,
    porcentaje_afecta_productividad,
    interfiere_trabajo
FROM impacto_profesional;
DROP TABLE impacto_profesional  ;
ALTER TABLE impacto_profesional_temp   RENAME TO Impacto_profesional
