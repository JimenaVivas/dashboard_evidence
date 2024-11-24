import streamlit as st
from PIL import Image

# Load an image from local file
image = Image.open("images/votaciones2021.jpg")

# Display image with a caption
st.image(image, caption="Elecciones de México 2024", use_container_width=True)

# Center and style the subheader and text
st.markdown("<h2 style='text-align: left; color: dimgray;'>Un Momento Histórico en la Política Mexicana</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: left; padding-top: 20px;'>
        <p style='font-size: 1.1em; color: dimgray;'>
        Las elecciones presidenciales de México en 2024 marcaron un momento histórico al ser las más grandes en términos de participación y relevancia. Por primera vez, dos mujeres lideraron las principales coaliciones políticas en una contienda por la presidencia, destacando un cambio significativo en el panorama político del país. Este hecho atrajo atención nacional e internacional, generando un fuerte debate sobre la equidad de género, las políticas sociales y las prioridades del electorado mexicano.
        </p>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: left; color: dimgray;'>El Rol Transformador de las Redes Sociales</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: left; padding-top: 20px;'>
        <p style='font-size: 1.1em; color: dimgray;'>
            Un elemento crucial en estas elecciones fue el impacto de las redes sociales como plataformas de comunicación y persuasión. Candidatas, partidos y ciudadanos utilizaron estas herramientas no solo para difundir propuestas políticas, sino también para movilizar votantes y generar discusiones. Las redes sociales sirvieron como espacios para debates abiertos, pero también intensificaron los desafíos relacionados con la desinformación y las noticias falsas. Las campañas digitales se caracterizaron por su creatividad, con el uso de memes, transmisiones en vivo y estrategias de segmentación para conectar con votantes jóvenes y urbanos.
        </p>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: left; color: dimgray;'>Visibilización y Polarización: Dos Caras de la Moneda</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: left; padding-top: 20px;'>
        <p style='font-size: 1.1em; color: dimgray;'>
        Además, las redes sociales jugaron un papel determinante en la visibilización de temas clave, como la inclusión de grupos minoritarios y la urgencia de políticas climáticas. Sin embargo, también expusieron la polarización entre diferentes sectores de la sociedad, haciendo evidente la necesidad de un diálogo más constructivo. En conjunto, estas dinámicas reflejan cómo el entorno digital transformó la manera en que se desarrollaron las elecciones, marcando un precedente para futuros procesos democráticos en México.        </p>
    </div>
    """, unsafe_allow_html=True
)