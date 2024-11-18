import streamlit as st

# Páginas individuales
intro = st.Page(
    "Background/intro.py",
    title="Introduction",
    icon=":material/help:",
)

facts = st.Page(
    "Background/facts.py",
    title="Facts",
    icon=":material/help:",
)

# Eliminamos visualization y agregamos su contenido a eda_pages
statistics = st.Page(
    "EDA/eda.py",
    title="Statistics",
    icon=":material/person_add:",
)

interactive_charts = st.Page(
    "Visualization/visualization.py",
    title="Interactive Charts",
    icon=":material/bar_chart:",
)

ml = st.Page(
    "ml/ml_analysis.py",
    title="Sentiment Analysis",
    icon=":material/healing:",
)

about = st.Page(
    "Background/about.py",
    title="About Us",
    icon=":material/person_add:",
)

cr = st.Page(
    "Background/example.py",
    title="Copyright",
    icon=":material/person_add:",
)

# Reorganización de las secciones
intro_pages = [intro, facts]
eda_pages = [statistics, interactive_charts]  # Ahora Data Analysis incluye ambas páginas
ml_pages = [ml]
about_pages = [about, cr]

# Actualizamos el diccionario de navegación
page_dict = {
    "Introduction": intro_pages,
    "Data Analysis": eda_pages,  # Sección combinada de Statistics e Interactive Charts
    "Prediction": ml_pages,
    "About Us": about_pages,
}

# Interfaz principal
# Agregar logo
# st.title("Data Analytics ")
st.logo("images/images.jpeg", icon_image="images/images.jpeg")

# Navegación y ejecución de la página seleccionada
pg = st.navigation(page_dict)
pg.run()
