import streamlit as st
from PIL import Image

# Título y descripción
st.markdown(
    """
    <div style='text-align: center; padding: 2em; background-color: #f8f9fa;'>
        <h2 style='font-size: 2em; color: #4a4a4a;'>About Us</h2>
        <p style='font-size: 1.2em; color: #6c757d; line-height: 1.5;'>
            Somos un equipo multidisciplinario del Tec de Monterrey interesados en el análisis de datos y sus aplicaciones.
        </p>
    </div>
    """, unsafe_allow_html=True
)

# Definir las imágenes, los miembros del equipo y carrera
team_members = [
    {"name": "Raymundo Aarón Toledo González", "image": "images/Ray.jpg", "text": "IIS"},
    {"name": "Miguel Ponce de León", "image": "images/Mike.jpg", "text": "LAF"},
    {"name": "Jimena Vivas Hernández", "image": "images/io.png", "text": "IMD"},
    {"name": "Daniel Borja Farfán", "image": "images/Borja.jpg", "text": "LEM"},
    {"name": "José María Juárez Villar", "image": "images/Chema.jpg", "text": "IBT"},
]

# Crear columnas para cada miembro del equipo
cols = st.columns(len(team_members))
for col, member in zip(cols, team_members):
    with col:
        # Mostrar la imagen de cada miembro
        image = Image.open(member["image"])
        st.image(image, use_container_width=True)
        # Mostrar el nombre del miembro con un tamaño más pequeño
        st.markdown(
            f"<h3 style='text-align: center; color: #4a4a4a; font-size: 1.3em;'>{member['name']}</h3>", unsafe_allow_html=True
        )
        # Mostrar iniciales de carrera correspondiente debajo del nombre
        st.markdown(
            f"<p style='text-align: center; color: #6c757d; font-size: 0.8em;'>{member['text']}</p>", unsafe_allow_html=True
        )

# Imagen adicional (QR) centrada con st.image
col1, col2, col3, col4, col5 =st.columns(5)
with col3:
    st.image("images/qr.png", width=200)