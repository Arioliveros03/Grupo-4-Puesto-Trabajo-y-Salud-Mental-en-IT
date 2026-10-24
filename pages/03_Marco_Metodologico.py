import streamlit as st

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


