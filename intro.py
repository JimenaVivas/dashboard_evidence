import streamlit as st
from PIL import Image

# Load an image from local file
image = Image.open("images/votaciones2021.jpg")

# Display image with a caption
st.image(image, caption="Elections", use_column_width=True)

# Display formatted text below the image
st.markdown(
    """
    <div style='text-align: center; padding-top: 20px;'>
        <h2 style='color: #4a4a4a;'>Introduction</h2>
        <p style='font-size: 1.1em; color: #6c757d;'>
            The Instituto Nacional Electoral (INE) oversees federal elections in Mexico. Its responsibilities include organizing election day logistics, producing and distributing electoral materials, counting votes, and certifying the election results.
        </p>
    </div>
    """, unsafe_allow_html=True
)
