import streamlit as st

# --- Configuración inicial --- (esto debe ir al inicio del script)
st.set_page_config(page_title="Data Analytics App", page_icon=":bar_chart:", layout="wide")


# --- Página de introducción como "main page" ---
if "main_page" not in st.session_state:
    st.session_state.main_page = True  # Indica si estamos en la página principal

if st.session_state.main_page:
    # --- Logo y Título ---
    st.image("images/images.jpeg", use_container_width=False, width=200)
    st.title("Data Analytics App")

    # --- Contenido de la introducción ---
    st.header("¡Bienvenido!")
    st.write(
        """
        Bienvenido a la aplicación de análisis de datos. Aquí podrás explorar información detallada sobre 
        interacciones de usuarios, análisis de sentimientos, y más. ¡Comencemos!
        """
    )
    st.write("---")

    # --- Botón para ir a Hipótesis ---
    if st.button("Ir a Introducción"):
        st.session_state.main_page = False  # Cambiar el estado
        st._set_query_params(page="hipotesis")  # Actualizar los parámetros
        # No es necesario hacer "rerun", Streamlit detectará el cambio automáticamente.

else:
    # --- Importar navegación normal ---
    intro = st.Page(
        "Background/intro.py",
        title="Introducción",
    )

    facts = st.Page(
        "Background/facts.py",
        title="Hipótesis",
    )

    statistics = st.Page(
        "EDA/eda.py",
        title="Interacciones según publicación",
    )

    interactive_charts = st.Page(
        "Visualization/visualization.py",
        title="Comportamiento de usuarios",
    )

    ml = st.Page(
        "ml/ml_analysis.py",
        title="Análisis de Sentimientos",
    )

    clust = st.Page(
        "ml/clustering.py",
        title="Clustering",
    )

    about = st.Page(
        "Background/about.py",
        title="Sobre Nosotros",
    )

    cr = st.Page(
        "Background/example.py",
        title="Copyright",
    )

    # --- Navegación ---
    intro_pages = [intro, facts]
    eda_pages = [statistics, interactive_charts]
    ml_pages = [ml, clust]
    about_pages = [about, cr]

    page_dict = {
        "Introducción": intro_pages,
        "Análisis": eda_pages,  # Sección combinada de Statistics e Interactive Charts
        "Predicción": ml_pages,
        "Sobre Nosotros": about_pages,
    }

    # --- Generar el menú lateral ---
    pg = st.navigation(page_dict)
    pg.run()
