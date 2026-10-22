import os
import duckdb
import streamlit as st
from dotenv import load_dotenv
from styles import load_css

# config de la pagina
st.set_page_config(page_title="Salud mental en IT", page_icon="🧠", layout="wide")
load_css()

# paginas (mismos archivos de pages/)
inicio        = st.Page("pages/00_Inicio.py",             title="Inicio",             icon="🏠", default=True)
planteamiento = st.Page("pages/01_Planteamiento.py",      title="Planteamiento",      icon="🔍")                
marco_teorico = st.Page("pages/02_Marco_Teorico.py",      title="Marco Teórico",      icon="📚")
marco_metodo  = st.Page("pages/03_Marco_Metodologico.py", title="Marco Metodológico", icon="🧪")
cuestionario  = st.Page("pages/05_Cuestionario_SQL.py",   title="Cuestionario SQL",   icon="🗄️")
conclusiones  = st.Page("pages/04_Conclusiones.py",       title="Conclusiones",       icon="✅")
bibliografia  = st.Page("pages/06_Bibliografia.py",       title="Bibliografía",       icon="🔗")

pg = st.navigation(
    [inicio, planteamiento, marco_teorico, marco_metodo, cuestionario, conclusiones, bibliografia],
    position="hidden",
)

def boton(pagina, n):
    activo = "-activo" if pagina.title == pg.title else ""
    with st.container(key=f"btn-{n}{activo}"):
        st.page_link(pagina)


# sidebar
with st.sidebar:
    st.markdown("## 🧠 Salud mental en IT")
    st.caption("Percepción de perjuicio profesional · Sector tecnológico")
    st.write("")

    boton(inicio, 6)                     
    st.write("")

    st.caption("**INVESTIGACIÓN**")
    boton(planteamiento, 0)
    boton(marco_teorico, 1)
    boton(marco_metodo,  2)

    st.write("")
    st.caption("**RESULTADOS**")
    boton(cuestionario, 3)
    boton(conclusiones, 4)

    st.write("")
    with st.expander("📎 Referencias y equipo", expanded=False):
        boton(bibliografia, 5)
        st.write("")
        st.markdown("**👥 Equipo**")
        for n in ["Nicole Altera", "Danmara Dos Ramos", "Arianna Oliveros",
                "Camila Santiago", "Sebastian Soto"]:
            st.write(n)

# conexión a motherduck
load_dotenv()

@st.cache_resource(show_spinner="Conectando a MotherDuck...")
def get_conn():
    return duckdb.connect("md:puesto de trabajo y salud mental")

try:
    st.session_state["conn"] = get_conn()
except Exception as e:
    st.session_state["conn"] = None
    st.sidebar.error(f"Sin conexión a la base de datos: {e}")
pg.run()