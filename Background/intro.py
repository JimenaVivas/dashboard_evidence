import streamlit as st
from PIL import Image

# Load an image from local file
image = Image.open("images/votaciones2021.jpg")

# Display image with a caption
st.image(image, caption="Elecciones de México 2024", use_container_width=True)

# Center and style the subheader and text
st.markdown("<h2 style='text-align: center; color: dimgray;'>Elecciones</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: left; padding-top: 20px;'>
        <p style='font-size: 1.1em; color: dimgray;'>
            En 2024 México vió las mayores elecciones populares en su historia. La contienda electoral giró alrededor de las elecciones presidenciales y el tema más importante durante esta elección fue la  disputa de la elección entre dos candidatas mujeres, lo cual no había sucedido antes.
        </p>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: center; color: dimgray;'>Resultados</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: left; padding-top: 20px;'>
        <p style='font-size: 1.1em; color: dimgray;'>
            La candidata Claudia Sheinbaum, quien contendió por parte de MORENA, fue la ganadora con un 60% de los votos.
        </p>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: center; color: dimgray;'>Redes Sociales</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: left; padding-top: 20px;'>
        <p style='font-size: 1.1em; color: dimgray;'>
            En las elecciones de México 2024, las redes sociales desempeñaron un papel crucial al influir en la opinión pública y facilitar la comunicación directa entre los candidatos y la ciudadanía. Estas plataformas permitieron una rápida difusión de información y la organización de movimientos políticos, impactando directamente en el nivel de participación y en las estrategias de campaña. Además, ofrecieron un espacio para el debate y la discusión, donde las audiencias pudieron interactuar y expresar sus opiniones de manera inmediata, contribuyendo a una dinámica electoral más participativa y conectada.
        </p>
    </div>
    """, unsafe_allow_html=True
)