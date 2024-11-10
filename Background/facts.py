import streamlit as st
from PIL import Image
# Load an image from local file
image = Image.open("images/mapa.webp")
# Set up two columns
col1, col2 = st.columns([1, 2])

# Column 1: Display the image
with col1:
    st.image(image, use_column_width=True)

# Column 2: Display formatted text
with col2:
    st.markdown(
        """
        <h2 style='color: #4a4a4a;'>Important Facts</h2>
        <p style='font-size: 1.1em; color: #6c757d;'>
            En este sentido, la revisión de la literatura permite analizar y reflexionar si la teoría y la investigación anterior sugiere una respuesta (aunque sea parcial) a la pregunta o las preguntas de investigación; o bien, si provee una orientación a seguir dentro del planteamiento del estudio (Lawrence y otros, citados por Hernández-Sampieri, 2014). 
        """, unsafe_allow_html=True
    )
