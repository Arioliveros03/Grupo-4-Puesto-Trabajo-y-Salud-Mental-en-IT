import streamlit as st

st.set_page_config(page_title="Salud Mental en IT", page_icon="🔍", layout="wide")

# css para el contenedor de los parrafos
CSS ="""
<style>
div[class*="st-key-lectura"] {
    border: 2px solid #17597C;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    background-color: transparent; 
    box-shadow: 0 0 12px rgba(23, 89, 124, 0.4), 
                inset 0 0 8px rgba(23, 89, 124, 0.15);
}
.question-simple {
    text-align: center;
    margin: 0 auto 3rem auto;
    max-width: 850px;
}
.question-simple .label {
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7DA7D9;
    margin-bottom: 0.8rem;
}
.question-simple .main-text {
    font-size: 1.6rem;
    font-weight: 700;
    line-height: 1.4;
    color: #17597C; 
    margin-bottom: 1rem;
}
.question-simple .sub-text {
    font-size: 1rem;
    color: #6B7280; 
    font-style: italic;
}
div[class*="st-key-obj_esp"] {
    border: 1.5px solid #17597C !important; 
    border-radius: 12px;
    padding: 1.5rem;
    background: transparent;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
div[class*="st-key-obj_esp"]:hover {
    transform: translateY(-4px); 
    border-color: #84B3CE !important; 
    box-shadow: 0 8px 16px rgba(23, 89, 124, 0.15);
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# session state para que se quden primero los banners
if "seccion" not in st.session_state:
    st.session_state.seccion = "🔍 Planteamiento"

# banners
if st.session_state.seccion == "🔍 Planteamiento":
    st.image("assets/Planteamiento.png", use_container_width=True)
elif st.session_state.seccion == "🎯 Objetivos":
    st.image("assets/objetivos.png", use_container_width=True)
elif st.session_state.seccion == "💡 Justificación":
    st.image("assets/justificacion.png", use_container_width=True)

st.write("") 

# menu para cambiar entre planteamiento, objetivos, justificacion 
st.selectbox(
    "**Explora por la investigación:**",
    ["🔍 Planteamiento", "🎯 Objetivos", "💡 Justificación"],
    key="seccion"
)

st.divider()

# planteamiento 
if st.session_state.seccion == "🔍 Planteamiento":
    # Pregunta central de la investigación
    st.markdown(
        """
        <div class="question-simple">
            <div class="label">Pregunta Central de Investigación</div>
            <div class="main-text">
                ¿Difiere la percepción de perjuicio profesional por motivos de salud mental
                según el nivel jerárquico y el grupo de edad en el sector tecnológico?
            </div>
            <div class="sub-text">
                Responderla permitirá identificar los segmentos más vulnerables y
                diseñar políticas basadas en evidencia.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    parrafos = [
        "La salud mental se ha consolidado como una de las principales preocupaciones "
        "de la salud pública a nivel mundial. La Organización Mundial de la Salud estima "
        "que los trastornos mentales generan pérdidas económicas globales cercanas al "
        "billón de dólares anuales por concepto de productividad no realizada, y advierte "
        "que aproximadamente el 15% de los trabajadores presenta algún trastorno de este "
        "tipo. Dado que cerca del 60% de la población mundial desarrolla su actividad en "
        "un entorno laboral, la salud mental en el trabajo ha dejado de ser un asunto "
        "privado hasta el punto de que hoy ocupa un eje central tanto en las organizaciones "
        "como en las políticas públicas de empleo a nivel mundial.",

        "Desde una perspectiva más específica hacia el sector tecnológico, los estudios "
        "disponibles documentan una prevalencia de malestar psicológico superior a otras "
        "industrias, asociada a una cultura que normaliza las jornadas prolongadas y, con "
        "el avance exponencial de la tecnología en los últimos años, la constante presión "
        "por innovar y la exigencia constante de actualización de habilidades. A ello se "
        "suma que una amplia mayoría de los empleados percibe estigma en su entorno "
        "laboral, lo que constituye una barrera formidable para buscar ayuda y agrava el "
        "problema de fondo (Rado & Neagu, 2019; Sharma et al., 2018). Esta combinación de "
        "alta exigencia y estigma convierte al sector tecnológico en un caso especialmente "
        "relevante para el estudio de la salud mental.",

        "Ahora bien, en este contexto el estigma da lugar a lo que la literatura denomina "
        "**percepción de perjuicio profesional**: la creencia de que divulgar una condición "
        "de salud mental tendrá consecuencias negativas en el desarrollo de la carrera, las "
        "oportunidades de ascenso o el estatus dentro de la organización. No obstante, "
        "persisten vacíos significativos sobre cómo esta percepción varía según el nivel "
        "jerárquico del puesto y el grupo de edad del trabajador. Respecto a la jerarquía, "
        "la teoría de demandas-control de Karasek (1979) sugiere que los puestos inferiores, "
        "con menor autonomía y control, deberían presentar mayor vulnerabilidad al estrés "
        "laboral. Sin embargo, no se ha examinado empíricamente si esa vulnerabilidad se "
        "traduce en una mayor percepción de perjuicio profesional por motivos de salud "
        "mental, ni si el nivel jerárquico modula esa percepción.",

        "En cuanto a la edad, existen indicios de diferencias generacionales y de "
        "limitaciones de carrera asociadas a la edad en el sector tecnológico (CWJobs, 2019; "
        "Mental Health at Work Report, 2019), pero no se ha examinado si la percepción de "
        "perjuicio difiere entre grupos etarios ni cómo interactúa con la jerarquía. Por "
        "consiguiente, aunque se sabe que la salud mental es crítica en el sector tecnológico, "
        "no se ha establecido empíricamente si la percepción de perjuicio varía según la "
        "combinación de ambos factores.",
    ]
    with st.container(key="lectura"):
        for p in parrafos:
            st.markdown(p)
# objetivos
elif st.session_state.seccion == "🎯 Objetivos":
    
    st.subheader("🎯 Objetivo General")
    st.info(
        "**Determinar si la percepción de perjuicio profesional por motivos de salud "
        "mental difiere según el nivel jerárquico del puesto de trabajo y el grupo "
        "de edad del trabajador en el sector tecnológico.**",
        icon="✨"
    )
    
    st.write("")
    st.subheader("📌 Objetivos Específicos")
    st.write("")
    
    objetivos = [
        "Caracterizar socio-demográficamente a la muestra de trabajadores del sector tecnológico (edad, género, nivel jerárquico y país).",
        "Describir la distribución de la percepción de perjuicio profesional por nivel jerárquico y grupo de edad.",
        "Analizar la relación entre la edad y la percepción de perjuicio dentro de cada nivel jerárquico.",
        "Determinar si existen diferencias significativas en la percepción de perjuicio según el nivel jerárquico y el grupo de edad, y si existe interacción entre ambos factores."
    ]
    
    col1, col2 = st.columns(2, gap="medium")
    
    for i, obj in enumerate(objetivos):
        columna = col1 if i % 2 == 0 else col2
        with columna:
            with st.container(border=True, key=f"obj_esp_{i}"):
                st.markdown(f"**0{i+1}.** {obj}")
            st.write("")     

# justificacion
elif st.session_state.seccion == "💡 Justificación":
    justificacion = [
        "Esta investigación se justifica teóricamente porque aborda "
        "un área poco explorada empíricamente en la salud mental. Si bien la teoría de "
        "demandas-control de Karasek (1979) sugiere que los puestos con menor control son "
        "más vulnerables al estrés, típicamente los niveles operativos, no se ha probado "
        "si esa falta de control se traduce en una mayor percepción de perjuicio "
        "profesional. Es decir, si el miedo a que divulgar una condición de salud mental "
        "afecte la carrera es significativamente mayor en quienes tienen menos poder de "
        "decisión. Además, los estudios sobre las diferencias generacionales en el sector "
        "tecnológico son escasos, por lo que probar cómo interactúan la jerarquía y la "
        "edad en este contexto aporta evidencia novedosa para actualizar los modelos "
        "clásicos de estrés organizacional.",

        "Desde el punto de vista práctico, los hallazgos "
        "ofrecerán información aplicable al diseño de políticas organizacionales. "
        "Identificar qué segmentos de la fuerza laboral tecnológica combinando jerarquía "
        "y edad, perciben mayor riesgo de perjuicio permitirá a las empresas dirigir sus "
        "recursos e intervenciones hacia los grupos más vulnerables. Dado que el sector "
        "enfrenta altos niveles de rotación y un estigma que silencia a los trabajadores, "
        "el estudio permitirá crear evidencia sobre dónde duele más el estigma. Por último, "
        "y no menos importante, podrá favorecer el diseño de programas de apoyo "
        "diferenciados, mejorar los canales de comunicación interna y reducir las barreras "
        "que impiden buscar ayuda, impactando positivamente en la retención de talento y "
        "el ambiente laboral.",

        "A nivel social y metodológico, el estudio "
        "atiende al llamado de organismos internacionales como la Organización Mundial de "
        "la Salud (OMS) y la Organización Internacional del Trabajo (OIT) de proteger la "
        "salud mental en el trabajo. Al utilizar datos abiertos de la encuesta Open "
        "Sourcing Mental Illness (OSMI), la investigación visibiliza las desigualdades "
        "internas de [COMPLETAR: p. ej. las organizaciones del sector tecnológico, "
        "desnaturaliza el estigma y aporta evidencia sobre justicia organizacional].",
    ]

    with st.container(key="lectura"):
        for p in justificacion:
            st.markdown(p)