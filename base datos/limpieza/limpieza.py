import sqlite3
from pathlib import Path
import pandas as pd

# rutas
RUTA_BD_SQL = Path("/Users/nicole/Desktop/trabajo final pt2/mental_health_normalizada (1)") 
RUTA_ORIGINAL = Path("/Users/nicole/Desktop/trabajo final pt2/mental_health_normalizada.backup") 
RUTA_RAW = Path("/Users/nicole/Desktop/trabajo final/mental_health.sqlite")
RUTA_SALIDA = Path("mental_health_limpia.sqlite")  

con_norm = sqlite3.connect(RUTA_BD_SQL.resolve().as_uri() + "?mode=ro", uri=True)
con_orig = sqlite3.connect(RUTA_ORIGINAL.resolve().as_uri() + "?mode=ro", uri=True)
con_raw = sqlite3.connect(RUTA_RAW.resolve().as_uri() + "?mode=ro", uri=True)

def leer(con, tabla):
    return pd.read_sql(f'SELECT * FROM "{tabla}"', con)

def desde_2016(tabla):
    t = leer(con_orig, tabla)
    return t[t["encuestaID"] >= 2016].copy()

# carga de datos
part_norm = leer(con_norm, "participantes")
genero_norm = leer(con_norm, "Genero")
pais = leer(con_norm, "pais")
estado_eeuu = leer(con_norm, "estado_EEUU")
puesto = leer(con_norm, "puesto_trabajo")
diagnostico = leer(con_norm, "diagnostico")
encuesta = leer(con_norm, "encuesta")

part_orig = leer(con_orig, "participante")
genero_orig = leer(con_orig, "genero")

ayuda = desde_2016("ayuda_laboral")
categoria = desde_2016("categoria_laboral")
estado_mental = desde_2016("estado_mental")
impacto = desde_2016("impacto_profesional")
prejuicio = desde_2016("perjuicio_salud_mental").drop(columns=["perjuicio_laboralID"])

ids_encuestados = set(categoria["participanteID"])
part = part_orig[part_orig["participanteID"].isin(ids_encuestados)].copy()

edad_norm = part_norm.set_index("participanteID")["edad"]
part["edad"] = part["participanteID"].map(edad_norm)

# paises
pais["paistexto"] = pais["paistexto"].astype(str).str.strip()

def id_pais(texto):
    return int(pais.loc[pais["paistexto"] == texto, "paisID"].iloc[0])

ID_USA = id_pais("United States")
ID_USA_DUP = id_pais("United States of America")
ID_SIN_DATO_PAIS = id_pais("-1")

def limpiar_pais(serie):
    s = pd.to_numeric(serie, errors="coerce").astype("Int64")
    s = s.mask(s == ID_USA_DUP, ID_USA)
    s = s.mask(s == ID_SIN_DATO_PAIS)
    return s

part["paisID"] = limpiar_pais(part["paisID"])
categoria["paisID"] = limpiar_pais(categoria["paisID"])

pais = pais[~pais["paisID"].isin([ID_USA_DUP, ID_SIN_DATO_PAIS])].copy()
pais["paistexto"] = pais["paistexto"].replace({"Bahamas, The": "Bahamas"})

# estados de USA
estado_eeuu["Estadotexto"] = estado_eeuu["Estadotexto"].astype(str).str.strip()

def id_estado(texto):
    return int(estado_eeuu.loc[estado_eeuu["Estadotexto"] == texto, "estado_EEUUID"].iloc[0])

ID_DC = id_estado("District of Columbia")
ID_DC_DUP = id_estado("DC")
ID_FUERA_USA = id_estado("Not applicable / Outside US")

def limpiar_estado(estado, pais_id):
    e = pd.to_numeric(estado, errors="coerce").astype("Int64")
    e = e.mask(e == ID_DC_DUP, ID_DC)
    fuera = (pais_id.notna() & (pais_id != ID_USA)).fillna(False).astype(bool)
    e = e.mask(fuera & (e != ID_FUERA_USA).fillna(False).astype(bool), ID_FUERA_USA)
    en_usa_sin_estado = ((pais_id == ID_USA) & (e == ID_FUERA_USA)).fillna(False).astype(bool)
    e = e.mask(en_usa_sin_estado)
    return e

part["estado_EEUUID"] = limpiar_estado(part["estado_EEUUID"], part["paisID"])
categoria["estado_eeuuID"] = limpiar_estado(categoria["estado_eeuuID"], categoria["paisID"])
estado_eeuu = estado_eeuu[estado_eeuu["estado_EEUUID"] != ID_DC_DUP].copy()

paises_activos = set(part["paisID"].dropna()).union(set(categoria["paisID"].dropna()))
pais = pais[pais["paisID"].isin(paises_activos)].copy()

estados_activos = set(part["estado_EEUUID"].dropna()).union(set(categoria["estado_eeuuID"].dropna()))
estado_eeuu = estado_eeuu[estado_eeuu["estado_EEUUID"].isin(estados_activos)].copy()

# genero
HOMBRE = {"male", "masculino", "cishet male", "masculine", "male-ish", "ostensibly male", "guy (-ish) ^_^", "swm", "ostensibly male, unsure what that really means"}
MUJER = {"female", "femmina", "female-identified", "woman-identified", "female-ish"}
BASURA = {"-1", "a little about you", "p", "nah", "all", "none of your business", "43", "rr", "human", "unicorn", "i am a wookie", "i have a penis", "god king of the valajar", "sometimes", "contextual", "\\-", "none", "fm"}

def clasificar_genero(texto):
    if pd.isna(texto):
        return "Otro"
    t = str(texto).strip().lower()
    if t in BASURA or t == "": 
        return "Otro"
    if t in HOMBRE: 
        return "Masculino"
    if t in MUJER: 
        return "Femenino"
    return "Otro"

genero_orig["clase"] = genero_orig["generotexto"].map(clasificar_genero)
ids_nuevos = genero_norm.set_index("generotexto")["generoID"]
genero_orig["generoID_nuevo"] = genero_orig["clase"].map(ids_nuevos)
equivalencia = genero_orig.set_index("generoID")["generoID_nuevo"]
part["generoID"] = part["generoID"].map(equivalencia).astype("Int64")
genero = genero_norm.copy()

# eliminaar raza
if "raza" in part.columns:
    part = part.drop(columns=["raza"])

# puestos de trabajo y Jerarquías
MAPA_NIVEL = {
    "Executive Leadership": "Directivo", "Supervisor/Team Lead": "Coordinación",
    "One-person shop": "Coordinación", "Back-end Developer": "Operativo",
    "Front-end Developer": "Operativo", "DevOps/SysAdmin": "Operativo",
    "Designer": "Operativo", "Support": "Operativo", "Dev Evangelist/Advocate": "Operativo",
    "Other": "Excluir", "Sales": "Excluir", "HR": "Excluir",
}

puesto["puestotexto"] = puesto["puestotexto"].astype(str).str.strip()
puesto["nivel_jerarquico"] = puesto["puestotexto"].map(MAPA_NIVEL)

#  eliminar comapania_estech
categoria["rol_trabajo_estech"] = pd.to_numeric(categoria["rol_trabajo_estech"], errors="coerce").map({1.0: "1", 0.0: "0", -1.0: "Not Applicable"}).astype("string")
categoria["primer_trabajo"] = pd.to_numeric(categoria["primer_trabajo"], errors="coerce").map({1.0: "1", 0.0: "0", -1.0: "Not Applicable"}).astype("string").fillna("Not applicable / No experience")

if "compania_estech" in categoria.columns:
    categoria = categoria.drop(columns=["compania_estech"])

for col in ["independiente_trabajo", "puesto_trabajoID"]:
    categoria[col] = pd.to_numeric(categoria[col], errors="coerce").mask(categoria[col].isin([-1, "-1"])).astype("Int64")

categoria["encuestaID"] = categoria["encuestaID"].astype(int)
categoria["trabajo_remoto"] = categoria["trabajo_remoto"].astype("string").str.strip()

respuestas_puesto = pd.read_sql(
    "SELECT UserID AS participanteID, AnswerText AS puestotexto FROM Answer "
    "WHERE QuestionID = 117 AND SurveyID = 2016 ORDER BY rowid", con_raw)
respuestas_puesto["puestotexto"] = respuestas_puesto["puestotexto"].astype(str).str.strip()
respuestas_puesto["nivel"] = respuestas_puesto["puestotexto"].map(MAPA_NIVEL)

ORDEN_NIVEL = {"Excluir": 0, "Operativo": 1, "Coordinación": 2, "Directivo": 3}
respuestas_puesto["rango"] = respuestas_puesto["nivel"].map(ORDEN_NIVEL)
mejor = respuestas_puesto.loc[respuestas_puesto.groupby("participanteID")["rango"].idxmax()]

id_puesto = dict(zip(puesto["puestotexto"], puesto["puesto_trabajoID"]))
puesto_persona = mejor.set_index("participanteID")["puestotexto"].map(id_puesto)
categoria["puesto_trabajoID"] = categoria["participanteID"].map(puesto_persona).astype("Int64")

puestos_excluidos_ids = set(puesto[puesto["nivel_jerarquico"] == "Excluir"]["puesto_trabajoID"])
ids_a_excluir = set(categoria[categoria["puesto_trabajoID"].isin(puestos_excluidos_ids)]["participanteID"])

part = part[~part["participanteID"].isin(ids_a_excluir)].copy()
categoria = categoria[~categoria["participanteID"].isin(ids_a_excluir)].copy()
ayuda = ayuda[~ayuda["participanteID"].isin(ids_a_excluir)].copy()
estado_mental = estado_mental[~estado_mental["participanteID"].isin(ids_a_excluir)].copy()
impacto = impacto[~impacto["participanteID"].isin(ids_a_excluir)].copy()
prejuicio = prejuicio[~prejuicio["participanteID"].isin(ids_a_excluir)].copy()

# reindexacion
mauri_ids = {old_id: new_id for new_id, old_id in enumerate(sorted(part["participanteID"].unique()), start=1)}
part["participanteID"] = part["participanteID"].map(mauri_ids)
categoria["participanteID"] = categoria["participanteID"].map(mauri_ids)
ayuda["participanteID"] = ayuda["participanteID"].map(mauri_ids)
estado_mental["participanteID"] = estado_mental["participanteID"].map(mauri_ids)
impacto["participanteID"] = impacto["participanteID"].map(mauri_ids)
prejuicio["participanteID"] = prejuicio["participanteID"].map(mauri_ids)

# eliminar nulos que hayan quedado sin mapeo por el cambio de IDs
categoria = categoria.dropna(subset=["participanteID"])
ayuda = ayuda.dropna(subset=["participanteID"])
estado_mental = estado_mental.dropna(subset=["participanteID"])
impacto = impacto.dropna(subset=["participanteID"])
prejuicio = prejuicio.dropna(subset=["participanteID"])

# iompacto y perjuicio
impacto["afecta_carrera"] = pd.to_numeric(impacto["afecta_carrera"], errors="coerce").mask(impacto["afecta_carrera"].isin([-1])).astype("Int64")
impacto["afecta_productividad"] = impacto["afecta_productividad"].astype("string").str.strip().mask(lambda s: s.isin(["-1", "-1.0"]))
impacto["porcentaje_afecta_productividad"] = impacto["porcentaje_afecta_productividad"].astype("string").str.strip().mask(lambda s: s.isin(["-1", "-1.0"]))
impacto["interfiere_trabajo"] = impacto["interfiere_trabajo"].astype("string").str.strip()

prejuicio["consecuencias_negativas"] = prejuicio["consecuencias_negativas"].astype("string").str.strip().mask(lambda s: s.isin(["-1", "-1.0"]))
prejuicio["comentarios_malos"] = prejuicio["comentarios_malos"].astype("string").str.strip().mask(lambda s: s.isin(["-1", "-1.0"]))
for col in ["importancia_salud_mental", "importancia_salud_fisica"]:
    prejuicio[col] = pd.to_numeric(prejuicio[col], errors="coerce").mask(prejuicio[col].isin([-1])).astype("Int64")
prejuicio["crees_te_verian_mal"] = prejuicio["crees_te_verian_mal"].astype("string").str.strip()

for col in ["recursos_empresa_ayuda_mental", "discucion_formal_salud_mental", "conoces_opciones_ayuda", "beneficios_salud_mental", "anonimato_protegido"]:
    ayuda[col] = ayuda[col].astype("string").str.strip().mask(lambda s: s.isin(["-1"]), "Not specified")

estado_mental["cobertura_incluye_sm"] = pd.to_numeric(estado_mental["cobertura_incluye_sm"], errors="coerce").map({1.0: "Yes", 0.0: "No", -1.0: "Not applicable"}).astype("string")
estado_mental["diagnostico_oficial"] = estado_mental["diagnostico_oficial"].astype("string").str.strip().mask(lambda s: s.isin(["-1", "-1.0"]))
estado_mental["busco_tratamiento"] = pd.to_numeric(estado_mental["busco_tratamiento"], errors="coerce").mask(estado_mental["busco_tratamiento"].isin([-1])).astype("Int64")
estado_mental["diagnosticoID"] = estado_mental["diagnosticoID"].astype("string").str.strip()

# diagnosticos 
FUSION_DIAG = {
    "PDD-NOS": "Pervasive Developmental Disorder (Not Otherwise Specified)",
    "Autism (Asperger's)": "Autism Spectrum Disorder", "Asperges": "Autism Spectrum Disorder",
    "Autism": "Autism Spectrum Disorder", "Autism spectrum disorder": "Autism Spectrum Disorder",
    "Depression": "Mood Disorder (Depression, Bipolar Disorder, etc)",
    "PTSD (undiagnosed)": "Post-traumatic Stress Disorder",
    "ADD (w/o Hyperactivity)": "Attention Deficit Hyperactivity Disorder",
    "Burn out": "Stress Response Syndromes", "Sexual addiction": "Addictive Disorder",
    "Schizotypal Personality Disorder": "Personality Disorder (Borderline, Antisocial, Paranoid, etc)",
}
diagnostico["diagnosticotexto"] = diagnostico["diagnosticotexto"].astype(str).str.strip()
id_diag = dict(zip(diagnostico["diagnosticotexto"], diagnostico["diagnosticoID"]))
fusion_id = {id_diag[viejo]: id_diag[nuevo] for viejo, nuevo in FUSION_DIAG.items() if viejo in id_diag and nuevo in id_diag}

def unificar_lista(texto):
    if pd.isna(texto) or str(texto).strip() == "": 
        return texto
    ids = set()
    for x in str(texto).split("|"):
        x = x.strip()
        if x.isdigit():
            val = int(x)
            ids.add(fusion_id.get(val, val))
    return " | ".join(str(i) for i in sorted(ids))

estado_mental["diagnosticoID"] = estado_mental["diagnosticoID"].map(unificar_lista).astype("string")
diagnostico = diagnostico[~diagnostico["diagnosticoID"].isin(list(fusion_id.keys()))].copy()

# guardado en base de datos
if RUTA_SALIDA.exists(): RUTA_SALIDA.unlink()
out = sqlite3.connect(RUTA_SALIDA)
out.execute("PRAGMA foreign_keys = ON")

DDL = [
    "CREATE TABLE encuesta (encuestaID INTEGER PRIMARY KEY, Encuestatexto TEXT)",
    "CREATE TABLE genero (generoID INTEGER PRIMARY KEY, generotexto TEXT NOT NULL)",
    "CREATE TABLE pais (paisID INTEGER PRIMARY KEY, paistexto TEXT NOT NULL UNIQUE)",
    "CREATE TABLE estado_EEUU (estado_EEUUID INTEGER PRIMARY KEY, Estadotexto TEXT NOT NULL UNIQUE)",
    "CREATE TABLE puesto_trabajo (puesto_trabajoID INTEGER PRIMARY KEY, puestotexto TEXT NOT NULL UNIQUE, nivel_jerarquico TEXT NOT NULL CHECK (nivel_jerarquico IN ('Operativo','Coordinación','Directivo','Excluir')))",
    "CREATE TABLE diagnostico (diagnosticoID INTEGER PRIMARY KEY, diagnosticotexto TEXT NOT NULL UNIQUE)",
    "CREATE TABLE participantes (participanteID INTEGER PRIMARY KEY, edad INTEGER NOT NULL CHECK (edad BETWEEN 18 AND 74), generoID INTEGER REFERENCES genero(generoID), paisID INTEGER REFERENCES pais(paisID), estado_EEUUID INTEGER REFERENCES estado_EEUU(estado_EEUUID))",
    "CREATE TABLE categoria_laboral (participanteID INTEGER PRIMARY KEY REFERENCES participantes(participanteID), encuestaID INTEGER NOT NULL REFERENCES encuesta(encuestaID), puesto_trabajoID INTEGER REFERENCES puesto_trabajo(puesto_trabajoID), trabajo_remoto TEXT, paisID INTEGER REFERENCES pais(paisID), estado_eeuuID INTEGER REFERENCES estado_EEUU(estado_EEUUID), independiente_trabajo INTEGER, rol_trabajo_estech TEXT, primer_trabajo TEXT)",
    "CREATE TABLE ayuda_laboral (participanteID INTEGER PRIMARY KEY REFERENCES participantes(participanteID), encuestaID INTEGER NOT NULL REFERENCES encuesta(encuestaID), recursos_empresa_ayuda_mental TEXT, discucion_formal_salud_mental TEXT, conoces_opciones_ayuda TEXT, beneficios_salud_mental TEXT, anonimato_protegido TEXT)",
    "CREATE TABLE estado_mental (participanteID INTEGER PRIMARY KEY REFERENCES participantes(participanteID), encuestaID INTEGER NOT NULL REFERENCES encuesta(encuestaID), diagnostico_oficial TEXT, cobertura_incluye_sm TEXT, busco_tratamiento INTEGER, diagnosticoID TEXT)",
    "CREATE TABLE impacto_profesional (participanteID INTEGER PRIMARY KEY REFERENCES participantes(participanteID), encuestaID INTEGER NOT NULL REFERENCES encuesta(encuestaID), afecta_carrera INTEGER, afecta_productividad TEXT, porcentaje_afecta_productividad TEXT, interfiere_trabajo TEXT)",
    "CREATE TABLE prejuicio_salud_mental (participanteID INTEGER PRIMARY KEY REFERENCES participantes(participanteID), encuestaID INTEGER NOT NULL REFERENCES encuesta(encuestaID), importancia_salud_mental INTEGER, importancia_salud_fisica INTEGER, crees_te_verian_mal TEXT, comentarios_malos TEXT, consecuencias_negativas TEXT)",
]
for sql in DDL: out.execute(sql)

def guardar(df, tabla):
    df.astype(object).where(df.notna(), None).to_sql(tabla, out, if_exists="append", index=False)

for df, nombre in [
    (encuesta, "encuesta"), (genero, "genero"), (pais, "pais"), 
    (estado_eeuu, "estado_EEUU"), (puesto, "puesto_trabajo"), (diagnostico, "diagnostico"),
    (part, "participantes"), (categoria, "categoria_laboral"), (ayuda, "ayuda_laboral"),
    (estado_mental, "estado_mental"), (impacto, "impacto_profesional"), (prejuicio, "prejuicio_salud_mental")
]:
    guardar(df, nombre)

out.commit()
out.close()
con_norm.close()
con_orig.close()
con_raw.close()

print("todo oka, base creada con exito")