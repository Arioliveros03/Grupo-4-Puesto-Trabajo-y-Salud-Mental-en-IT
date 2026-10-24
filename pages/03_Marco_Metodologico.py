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

