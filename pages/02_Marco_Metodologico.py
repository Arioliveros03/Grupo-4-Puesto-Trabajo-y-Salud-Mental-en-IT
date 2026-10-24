import streamlit as st
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
