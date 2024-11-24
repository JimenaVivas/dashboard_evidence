import streamlit as st
import streamlit as st
import pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image  # Librería para manejar imágenes

st.title("Comparación de Interacciones Promedio por Publicación por Usuario")
st.write("### Temas más recurrentes")
st.write("Se observa a continuación el cambio de temas más recurrentes en la campaña y cómo cambio su frecuencia.")

# Cargar la imagen desde la carpeta 'images'
image = Image.open('images/Topics.png')

# Mostrar la imagen en Streamlit
st.image(image, use_container_width=True)

# Merge interactions and posts data for the entire campaign
user_interactions_all = pd.merge(user_interactions_all, user_posts_all, on='username')

# Calculate average interactions per post for the entire campaign
user_interactions_all['avg_interaction_all'] = user_interactions_all['interaction_count_all'] / user_interactions_all['post_count_all']




####### Interactions by most popular users

with open('interactions_data.pkl', 'rb') as f:
    merged_df = pickle.load(f)    # Mostrar una vista previa del DataFrame

    # Crear la gráfica
    st.write("Gráfica de Interactions per Post by User:")
    
    # Configuración de la gráfica
    X_axis = np.arange(len(merged_df))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(X_axis - 0.2, merged_df['avg_interaction_recent'], 0.4, label='Last 10 Days', color='plum')
    ax.bar(X_axis + 0.2, merged_df['avg_interaction_all'], 0.4, label='Entire Campaign', color='cadetblue')
    ax.set_xticks(X_axis)
    ax.set_xticklabels(merged_df['username'], rotation=45, ha="right")
    ax.set_xlabel("Username")
    ax.set_ylabel("Average Interactions per Post")
    ax.legend()
    
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)
