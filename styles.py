import streamlit as st

CSS = """
<style>
/* sidebar */
section[data-testid="stSidebar"][aria-expanded="true"]{ min-width:320px; }
section[data-testid="stSidebar"][aria-expanded="false"]{ min-width:0; }

[data-testid="stSidebar"] h2{ font-size:1.7rem; font-weight:800; color:#F5EEDD; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{ color:rgba(245,238,221,.8); }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] strong{
    color:#84B3CE; letter-spacing:.06em;
}

/* botones */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]{
    padding:.85rem 1.1rem;
    border-radius:14px;
    background:linear-gradient(180deg, rgba(23,89,124,.50), rgba(23,89,124,.22));
    border:1.5px solid #1F6D96;
    box-shadow:0 4px 10px rgba(4,22,33,.45),
            inset 0 1px 0 rgba(245,238,221,.12);
    transition:transform .25s ease, box-shadow .25s ease,
            background .25s ease, border-color .25s ease;
}

/* teexto */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p{
    color:#F5EEDD !important;
    font-size:1.12rem;
    font-weight:700;
}

/* botones pt2 al señalar*/
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover{
    background:linear-gradient(180deg, #1F6D96, #17597C);
    border-color:#2B80AD;
    transform:translateY(-2px);
    box-shadow:0 8px 16px rgba(4,22,33,.55),
            inset 0 1px 0 rgba(245,238,221,.18);
}

[class*="-activo"] [data-testid="stPageLink-NavLink"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:active{
    background:#17597C !important;
    border-color:#17597C !important;
    transform:translateY(0);
    box-shadow:inset 0 3px 8px rgba(4,22,33,.5),
            0 1px 0 rgba(245,238,221,.10) !important;
}

[data-testid="stSidebar"] [data-testid="stExpander"] details{
    background:transparent;
    border:1.5px solid rgba(132,179,206,.55);
    border-radius:16px;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary{ padding:.85rem 1rem; }
[data-testid="stSidebar"] [data-testid="stExpander"] summary p{
    font-size:1.15rem;
    font-weight:700;
}

[data-testid="stMain"] h1{
    width:fit-content;
    border-bottom:4px solid #84B3CE;
    padding-bottom:.3rem;
}

/* tabs */
[data-baseweb="tab-list"]{
    gap:.4rem; background:rgba(132,179,206,.30); padding:.4rem;
    border-radius:999px; width:fit-content;
}
button[data-baseweb="tab"]{ height:auto; padding:.45rem 1.3rem; border-radius:999px; }
button[data-baseweb="tab"] p{ font-weight:600; color:#0E3F59; }
button[data-baseweb="tab"][aria-selected="true"]{ background:#84B3CE; }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"]{ display:none; }

/* metricas */
[data-testid="stMetric"]{
    background:rgba(132,179,206,.30);
    border-radius:18px;
    padding:1rem 1.3rem;
}
</style>
"""

def load_css():
    st.markdown(CSS, unsafe_allow_html=True)