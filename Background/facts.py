import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import zipfile
import os

# Cargar la imagen
image = Image.open("images/mapa.webp")

# Ruta al archivo ZIP
zip_file_path = "EDA/csv.zip"

# Nombre del archivo CSV dentro del ZIP
csv_file_name = "output.csv"

# Leer el archivo CSV directamente desde el ZIP sin extraerlo
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Leer el archivo CSV dentro del ZIP en memoria
    with zip_ref.open(csv_file_name) as file:
        # Cargar el archivo CSV en un DataFrame
        df = pd.read_csv(file)


# Convertir columna `datetime` a formato datetime
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
if df['datetime'].dt.tz is None:
    # Si no tiene zona horaria, asignar UTC
    df['datetime'] = df['datetime'].dt.tz_localize('UTC')
# Ahora, convertir a la zona horaria de Ciudad de México (CDMX)
df['datetime'] = df['datetime'].dt.tz_convert('America/Mexico_City')

# Mostrar la imagen
st.image(image, use_column_width=True)

# Mostrar el texto formateado
st.markdown(
    """
    <h2 style='text-align: left; color: #c0c0c0;'>Explicación de hipótesis</h2>
    <p style='font-size: 1.1em; color: #b0b0b0;'>
        La revisión de la literatura permite analizar y reflexionar si la teoría y la investigación previa ofrecen una respuesta, aunque sea parcial, a las preguntas de investigación o, en su defecto, proporcionan una guía clara para el planteamiento del estudio (Lawrence et al., citado por Hernández-Sampieri, 2014).  
        El análisis de datos recuperados de diversas redes sociales brinda una comprensión más profunda del comportamiento de los usuarios y de la dinámica de la opinión pública. Este conocimiento puede ser invaluable para los candidatos y sus campañas políticas, permitiéndoles ajustar sus estrategias de manera más efectiva y maximizar sus beneficios en el proceso electoral.  
        En esta página web se examinará el comportamiento de los usuarios para identificar posibles cambios significativos en la campaña. La hipótesis sugiere que los 10 días previos a las elecciones, incluyendo los días de debates y anuncios clave, representan una muestra confiable del comportamiento de los usuarios en redes sociales.  
        Para evaluar esta hipótesis, se observarán los cambios en los patrones de publicación, como los horarios de actividad y su relación con el volumen de interacciones. Además, se analizarán las interacciones generadas por los usuarios más influyentes y las variaciones en los temas más discutidos. Este enfoque permitirá identificar tendencias clave y medir el impacto de los eventos de la campaña en el comportamiento digital de los usuarios. 
    </p>
    """, unsafe_allow_html=True
)



# Crear el multiselect para seleccionar candidatos
candidates = df['candidate_name'].unique()
selected_candidates = st.multiselect('Selecciona Candidatos', candidates)

# Filtrar los datos según los candidatos seleccionados
if selected_candidates:
    filtered_data = df[df['candidate_name'].isin(selected_candidates)]
else:
    filtered_data = df

# Crear interacciones por fecha y plataforma
interactions_by_date = (
    filtered_data.groupby([filtered_data['datetime'].dt.date, 'platform'])['text']
    .count()
    .reset_index()
)
interactions_by_date.columns = ['datetime', 'platform', 'text']



# Crear gráfico de líneas con Plotly
fig = go.Figure()

# Colores personalizados para las plataformas
platform_colors = {
    'youtube': 'red',
    'instagram': 'purple',
    'facebook': 'blue',
    'twitter': 'lightblue'
}

for platform in platform_colors.keys():
    platform_data = interactions_by_date[interactions_by_date['platform'] == platform]
    fig.add_trace(go.Scatter(
        x=platform_data['datetime'],
        y=platform_data['text'],
        mode='lines+markers',
        name=platform,
        line=dict(color=platform_colors[platform])
    ))

# Configuración adicional del gráfico
fig.update_layout(
    title={
        'text': 'Actividad Diaria en Cada Plataforma',
        'x': 0.5,
        'y': 0.9,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="Plataforma",
    yaxis_title="Número de Publicaciones",
    template="plotly_white",
    legend_title="Plataforma",
)

# Mostrar gráfico de líneas en Streamlit
st.plotly_chart(fig, use_container_width=True)


# Mostrar el texto formateado
st.markdown(
    """
    <h2 style='text-align: left; color: #c0c0c0;'>Explicación de hipótesis</h2>
    <p style='font-size: 1.1em; color: #b0b0b0;'>
        La revisión de la literatura permite analizar y reflexionar si la teoría y la investigación previa ofrecen una respuesta, aunque sea parcial, a las preguntas de investigación o, en su defecto, proporcionan una guía clara para el planteamiento del estudio (Lawrence et al., citado por Hernández-Sampieri, 2014).  
        El análisis de datos recuperados de diversas redes sociales brinda una comprensión más profunda del comportamiento de los usuarios y de la dinámica de la opinión pública. Este conocimiento puede ser invaluable para los candidatos y sus campañas políticas, permitiéndoles ajustar sus estrategias de manera más efectiva y maximizar sus beneficios en el proceso electoral.  
        En esta página web se examinará el comportamiento de los usuarios para identificar posibles cambios significativos en la campaña. La hipótesis sugiere que los 10 días previos a las elecciones, incluyendo los días de debates y anuncios clave, representan una muestra confiable del comportamiento de los usuarios en redes sociales.  
        Para evaluar esta hipótesis, se observarán los cambios en los patrones de publicación, como los horarios de actividad y su relación con el volumen de interacciones. Además, se analizarán las interacciones generadas por los usuarios más influyentes y las variaciones en los temas más discutidos. Este enfoque permitirá identificar tendencias clave y medir el impacto de los eventos de la campaña en el comportamiento digital de los usuarios. 
    </p>
    """, unsafe_allow_html=True
)
