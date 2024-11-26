from EDA.eda import plot_template_plotly
import streamlit as st
import pickle
import numpy as np
import plotly.graph_objects as go
from PIL import Image  
from wordcloud import WordCloud

st.title("Comparación de Interacciones Promedio por Publicación por Usuario")
st.write("### Temas más recurrentes")
st.write("Se observa a continuación el cambio de temas más recurrentes en la campaña y cómo cambio su frecuencia.")

# Cargar la imagen desde la carpeta 'images'
# En este caso se utiliza la imagen en lugar de un archivo csv o el dataframe en pickle debido a que no es interactivo y resulta más sencillo así, 
# además de mantener la página rápida evitando que se realicen procesos para llevar a cabo la gráfica
image = Image.open('images/Topics.png')
# Mostrar la imagen en Streamlit
st.image(image, use_container_width=True)

##################### Posts por usuario
st.write("### Diferencia en la actividad de los diez usuarios más populares")
st.write("* En este caso los usuarios que se muestran son aquellos que fueron más constantes y con mayor número de publicaciones los últimos 10 días del proceso electoral.")

# Cargar el archivo pickle directamente
with open('EDA/merged_posts_data.pkl', 'rb') as f:
    data = pickle.load(f)

# Crear la gráfica con Plotly
    fig = go.Figure()

    # Agregar barras para los últimos 10 días
    fig.add_trace(go.Bar(
        x=data['username'],
        y=data['avg_posts_per_day_recent'],
        name='Últimos 10 días',
        marker_color='#1b9e77'
    ))

    # Agregar barras para toda la campaña
    fig.add_trace(go.Bar(
        x=data['username'],
        y=data['avg_posts_per_day_all'],
        name='Campaña Completa',
        marker_color='lightsteelblue'
    ))

    # Configuración del diseño
    fig.update_layout(
        title={
            'text': "Average Posts per Day by User",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Nombre de Usuario",
        yaxis_title="Promedio de Publicaciones por Día",
        barmode='group',  # Agrupar barras
        legend_title="Periodo de Tiempo",
        template="plotly_white"  # Tema de la gráfica
    )
    plot_template_plotly(
    fig,
    suptitle='Promedio de Publicaciones',
    title='Por Publicación de los 10 Usuarios Más Populares',
    suptitle_x=0.58, suptitle_y=0.9,
    title_x=0.52, title_y=1.1,
    )
    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig)