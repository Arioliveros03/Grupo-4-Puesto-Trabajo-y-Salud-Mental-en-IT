import streamlit as st
import pandas as pd

st.set_page_config(page_title="Marco Metodológico", page_icon="🧪", layout="wide")

st.header("Marco Metodológico")

st.subheader("1. Enfoque y Diseño de la Investigación")
col1, col2 = st.columns(2, gap="medium")

with col1:
    with st.container(border=True):
        st.markdown("### Enfoque")
        st.markdown(
            "**Cuantitativo.** La investigación se basa en la recolección y el análisis de "
            "datos numéricos para probar hipótesis y establecer patrones de comportamiento "
            "en la población estudiada."
        )

with col2:
    with st.container(border=True):
        st.markdown("### Diseño")
        st.markdown(
            "**No experimental, transversal y descriptivo-inferencial.** "
            "No se manipulan las variables; los datos se recolectan en un único momento "
            "para describir las variables y analizar su incidencia e interrelación."
        )

st.subheader("2. Población y Muestra")

st.info(
    "**Población:** Profesionales que desarrollan su actividad en el sector tecnológico, "
    "cuyos datos fueron recolectados a través de las encuestas OSMI (Open Sourcing Mental Illness)."
)

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    st.metric(label="Sector de estudio", value="Tecnológico")
with col_p2:
    st.metric(label="Fuente de datos", value="OSMI Survey")
with col_p3:
    st.metric(label="Tipo de muestreo", value="No probabilístico")

st.write("")
st.markdown(
    "La muestra se compone de los registros válidos de la base OSMI que cumplen con los "
    "criterios de inclusión: pertenecer al sector tecnológico y haber respondido a las "
    "variables de interés (nivel jerárquico, edad y percepción de perjuicio)."
)

st.divider()

st.header("4.2. Proceso de limpieza y normalización de datos")
st.markdown(
    "El tratamiento, depuración y normalización de la base de datos se llevó a cabo "
)
st.subheader("Fases técnicas de la limpieza")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Integridad y Tiempo", 
    "Datos Demográficos", 
    "Nivel Jerárquico", 
    "Salud Mental y Edad", 
    "Otros Ajustes"
])
with tab1:
    st.markdown("### Corrección de integridad referencial y temporal")
    st.markdown(
        "Al eliminar los registros del año 2014, las tablas de respuestas se enumeraron "
        "secuencialmente del 1 al 2958, mientras que la tabla de participantes conservaba "
        "los IDs originales. Para corregir esto, se realizó el siguiente proceso:"
    )
    st.markdown(
        "- Se leyeron las tablas desde la base de datos original filtrando solo los años **2016 a 2019**.\n"
        "- Se implementó una tabla temporal para reorganizar secuencialmente a los participantes restantes.\n"
        "- Se verificó que todas las tablas tuvieran exactamente los mismos **2,958 participantes**."
    )
    st.success("**Resultado:** Integridad referencial garantizada y consistencia estructural asegurada.")
    
    st.warning(
        "**¿Por qué se eliminó 2014?** Se excluyó debido a la alta proporción de valores nulos "
        "y a la ausencia de preguntas clave en el cuestionario original, lo que impedía realizar "
        "un estudio comparativo fiable."
    )

with tab2:
    st.markdown("### Estandarización de variables sociodemográficas")
    
    with st.container(border=True):
        st.markdown("**País y Estado**")
        st.markdown(
            "Se unificaron las etiquetas *'United States'* y *'United States of America'*. "
            "El código `-1` (valor nulo) se convirtió en dato faltante real y se validó la coherencia entre estado y país."
        )
        
    with st.container(border=True):
        st.markdown("**Género**")
        st.markdown(
            "Se agruparon los 101 textos originales en tres macrocategorías: "
            "**Femenino, Masculino y Otro**. Las respuestas sin sentido se marcaron como faltantes."
        )
        
    st.error(
        "**Variable Raza descartada:** Se decidió prescindir de esta variable por múltiples "
        "limitaciones metodológicas: solo se preguntó de 2017 a 2019 (excluyendo a la muestra principal de 2016), "
        "hubo alta abstención, muy poca variabilidad en las respuestas y no forma parte de los objetivos de la investigación."
    )

with tab3:
    st.markdown("### Creación de la variable `nivel_jerarquico`")
    st.markdown("Se creó la columna con las categorías a partir de las siguientes reglas de asignación:")
    
    st.table({
        "Nivel Asignado": ["Directivo", "Coordinación", "Operativo", "Excluir"],
        "Puestos Originales": [
            "Executive Leadership", 
            "Supervisor/Team Lead y One-person shop", 
            "Back-end, Front-end, DevOps, Designer, Support, Dev Evangelist", 
            "Other, Sales y HR"
        ]
    })
    
    st.warning(
        "**El problema de 2016 (Multiselección):** En 2016, la pregunta permitía marcar varias opciones. "
        "La base normalizada conservaba solo un puesto (a veces el de menor jerarquía), alterando la "
        "clasificación de 204 personas (ej. alguien que marcaba 'Executive Leadership' y 'Support' quedaba como Support)."
    )
    
    st.info(
        "**La solución:** Se implementó una ruta de lectura directa a la base original (`ruta_raw`). "
        "El script calculó el nivel jerárquico más alto según los puestos marcados (Directivo > Coordinación > Operativo). "
        "Las categorías excluidas solo se consideraron si no se marcó ninguna otra opción."
    )

with tab4:
    st.markdown("### Tratamiento de variables de salud mental")
    st.markdown(
        "- **Impacto profesional:** El código `-1` se convirtió en dato faltante y se restauró la columna `consecuencias_negativas`.\n"
        "- **Diagnóstico:** Se unificaron 11 diagnósticos que estaban duplicados (ej. distintas formas de escribir autismo) "
        "y se actualizaron las listas asociadas a cada participante."
    )
    
    st.write("")
    st.markdown("### Tratamiento de la Edad (Filtro y Corrección)")
    st.markdown(
        "Se detectaron valores absurdos (personas trabajando a los 5 años, 0 años, o 323 años). "
        "Dado que esto no está permitido en ningún país, se aplicó el siguiente filtro:"
    )
    st.success(
        "**Solución aplicada:** Se filtraron las edades válidas entre **18 y 75 años**. "
        "Las edades fuera de rango o mal contestadas **NO se eliminaron**; en su lugar, "
        "fueron reemplazadas por la **media ponderada** para obtener un valor estimado y conservar al participante."
    )

with tab5:
    st.markdown("### Manejo de valores nulos y columnas descartadas")
    
    with st.container(border=True):
        st.markdown("**Etiquetas 'Not applicable'**")
        st.markdown(
            "En las variables `categoria_laboral` y `cobertura_incluye_sm` se incorporó la etiqueta "
            "*'not applicable'* (en lugar de null) para evitar el rechazo de personas y conservar el volumen de registros."
        )
        
    with st.container(border=True):
        st.markdown("**Columna `compania_estech` descartada**")
        st.markdown(
            "Se eliminó por redundancia y ambigüedad. La validación evidenció que sus datos eran 100% idénticos "
            "a los de `primer_trabajo` (preguntaba por el empleador anterior de 2017-2019, no el actual). "
            "Además, la clasificación del tipo de empresa no resulta relevante para los objetivos del análisis."
        )

st.divider()

st.header("5. Diccionario de Datos")
st.markdown("A continuación se detalla la estructura de las tablas que conforman la base de datos normalizada, indicando el tipo de dato y el uso de cada variable en el análisis estadístico.")

dict_tab1, dict_tab2, dict_tab3, dict_tab4 = st.tabs([
    "👤 Participantes", 
    "💼 Categoría Laboral", 
    "🧠 Estado Mental", 
    "📚 Catálogos"
])

with dict_tab1:
    st.subheader("Tabla: Participantes")
    df_participantes = pd.DataFrame({
        "Variable": ["participanteID", "edad", "generoID", "paisID", "estado_EEUUID"],
        "Tipo": ["Integer", "Integer", "Integer", "Integer", "Integer"],
        "Descripción": [
            "Identificador único del participante (PK)", 
            "Edad del participante", 
            "Indicador del género (FK)", 
            "Indicador del país donde vive (FK)", 
            "Indicador del estado de EEUU donde vive (FK)"
        ],
        "Uso en el Proyecto": [
            "Identificación primaria", 
            "Variable independiente (Agrupada en rangos)", 
            "Perfil descriptivo (Objetivo 1)", 
            "Perfil descriptivo (Objetivo 1)", 
            "Contexto geográfico"
        ]
    })
    st.dataframe(df_participantes, hide_index=True, use_container_width=True)

with dict_tab2:
    st.subheader("Tabla: Categoría Laboral")
    df_categoria = pd.DataFrame({
        "Variable": ["participanteID", "encuestaID", "puesto_trabajoID", "trabajo_remoto", "paisID", "estado_EEUUID", "independiente_trabajo"],
        "Tipo": ["Integer", "Integer", "Integer", "Varchar", "Integer", "Integer", "Integer"],
        "Descripción": [
            "Indicador del participante (FK/PK)", 
            "Indicador de la encuesta (FK/PK)", 
            "Indicador del puesto de trabajo (FK)", 
            "Identifica si trabaja a distancia", 
            "Indicador del país donde trabaja (FK)", 
            "Indicador del estado donde trabaja (FK)", 
            "Identifica si trabaja de forma independiente"
        ],
        "Uso en el Proyecto": [
            "Llave de unión", 
            "Trazabilidad temporal", 
            "Variable independiente (Nivel)", 
            "Análisis descriptivo", 
            "Contexto geográfico", 
            "Contexto geográfico", 
            "Contexto laboral"
        ]
    })
    st.dataframe(df_categoria, hide_index=True, use_container_width=True)

    st.subheader("Tabla: Puesto de Trabajo")
    df_puesto = pd.DataFrame({
        "Variable": ["puesto_trabajoID", "puestotexto", "nivel_jerarquico"],
        "Tipo": ["Integer", "Text", "Text"],
        "Descripción": [
            "Identificador único del puesto de trabajo (PK)", 
            "Nombre del puesto de trabajo", 
            "Nivel jerárquico de los trabajos"
        ],
        "Uso en el Proyecto": [
            "Identificación primaria", 
            "Clasificación original", 
            "Variable independiente principal para el ANOVA"
        ]
    })
    st.dataframe(df_puesto, hide_index=True, use_container_width=True)

with dict_tab3:
    st.subheader("Tabla: Estado Mental")
    df_estado = pd.DataFrame({
        "Variable": ["participanteID", "encuestaID", "diagnostico_oficial", "busco_tratamiento", "condiciones_diagnosticadas"],
        "Tipo": ["Integer", "Integer", "Varchar", "Integer", "Text (Json)"],
        "Descripción": [
            "Indicador del participante (FK/PK)", 
            "Indicador de la encuesta (FK/PK)", 
            "Identifica si el participante presenta algún diagnóstico", 
            "Identifica si ha buscado tratamiento", 
            "Describe los diagnósticos múltiples o únicos"
        ],
        "Uso en el Proyecto": [
            "Llave de unión", 
            "Trazabilidad temporal", 
            "Contexto clínico", 
            "Perfil descriptivo", 
            "Análisis secundario"
        ]
    })
    st.dataframe(df_estado, hide_index=True, use_container_width=True)

    st.subheader("Tabla: Prejuicio Salud Mental")
    df_prejuicio = pd.DataFrame({
        "Variable": ["participanteID", "encuestaID", "crees_te_verian_mal", "comentarios_malos", "consecuencias_negativas"],
        "Tipo": ["Integer", "Integer", "Varchar", "Varchar", "Varchar"],
        "Descripción": [
            "Indicador del participante (FK/PK)", 
            "Indicador de la encuesta (FK/PK)", 
            "Identifica si cree que sería mal visto por tener problemas de salud mental", 
            "Identifica si ha escuchado comentarios negativos", 
            "Identifica si ha visto consecuencias negativas en personas que expresaron sus padecimientos"
        ],
        "Uso en el Proyecto": [
            "Llave de unión", 
            "Trazabilidad temporal", 
            "Variable dependiente principal para el ANOVA", 
            "Variable de apoyo (Estigma observado)", 
            "Variable de apoyo (Perjuicio observado)"
        ]
    })
    st.dataframe(df_prejuicio, hide_index=True, use_container_width=True)

    st.subheader("Tabla: Impacto Profesional")
    df_impacto = pd.DataFrame({
        "Variable": ["participanteID", "encuestaID", "afecta_carrera", "interfiere_trabajo"],
        "Tipo": ["Integer", "Integer", "Varchar", "Varchar"],
        "Descripción": [
            "Indicador del participante (FK/PK)", 
            "Indicador de la encuesta (FK/PK)", 
            "Identifica si los problemas de salud mental afectan su carrera", 
            "Identifica si los problemas afectan su trabajo"
        ],
        "Uso en el Proyecto": [
            "Llave de unión", 
            "Trazabilidad temporal", 
            "Variable alternativa de perjuicio", 
            "Análisis de contexto"
        ]
    })
    st.dataframe(df_impacto, hide_index=True, use_container_width=True)

    st.subheader("Tabla: Ayuda Laboral")
    df_ayuda = pd.DataFrame({
        "Variable": ["participanteID", "encuestaID", "recursos_empresa_ayuda_mental", "discucion_formal_salud_mental", "conoces_opciones_ayuda", "beneficios_salud_mental", "anonimato_protegido"],
        "Tipo": ["Integer", "Integer", "Varchar", "Varchar", "Varchar", "Varchar", "Varchar"],
        "Descripción": [
            "Indicador del participante (FK/PK)", 
            "Indicador de la encuesta (FK/PK)", 
            "Percepción de si la empresa ofrece recursos de ayuda", 
            "Percepción de si hay discusiones formales sobre el tema", 
            "Percepción de si conoce opciones de ayuda", 
            "Percepción de si la empresa ofrece beneficios", 
            "Percepción de si la empresa ofrece anonimato y seguridad"
        ],
        "Uso en el Proyecto": [
            "Llave de unión", 
            "Trazabilidad temporal", 
            "Variables de confianza en el liderazgo", 
            "Variables de confianza en el liderazgo", 
            "Variables de confianza en el liderazgo", 
            "Variables de confianza en el liderazgo", 
            "Variables de confianza en el liderazgo"
        ]
    })
    st.dataframe(df_ayuda, hide_index=True, use_container_width=True)

with dict_tab4:
    st.subheader("Tablas Catálogo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Encuesta**")
        df_encuesta = pd.DataFrame({
            "Variable": ["encuestaID", "encuestatexto"],
            "Descripción": ["Identificador único de la encuesta (PK)", "Nombre y año de la encuesta"]
        })
        st.dataframe(df_encuesta, hide_index=True, use_container_width=True)

        st.markdown("**Género**")
        df_genero = pd.DataFrame({
            "Variable": ["generoID", "generotexto"],
            "Descripción": ["Identificador único del género (PK)", "Nombre de los géneros"]
        })
        st.dataframe(df_genero, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("**País**")
        df_pais = pd.DataFrame({
            "Variable": ["PaisID", "paistexto"],
            "Descripción": ["Identificador único del país (PK)", "Nombre del país"]
        })
        st.dataframe(df_pais, hide_index=True, use_container_width=True)

        st.markdown("**Estados EEUU**")
        df_estados = pd.DataFrame({
            "Variable": ["estado_EEUUID", "estadotexto"],
            "Descripción": ["Identificador único para el estado (PK)", "Nombre del estado de EEUU"]
        })
        st.dataframe(df_estados, hide_index=True, use_container_width=True)
