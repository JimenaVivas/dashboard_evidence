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

# Ruta del archivo ZIP dentro de tu repositorio
zip_file_path = "EDA/csv.zip"

# Ruta temporal donde se extraerá el archivo CSV
extracted_folder = "EDA/extracted/"

# Asegúrate de que la carpeta de extracción existe
os.makedirs(extracted_folder, exist_ok=True)

# Extraer el archivo CSV desde el archivo ZIP
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract('output.csv', extracted_folder)

# Ruta del archivo CSV extraído
csv_file_path = os.path.join(extracted_folder, 'output.csv')

# Cargar el archivo CSV usando pandas
df = pd.read_csv(csv_file_path)

# Convertir columna `datetime` a formato datetime
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')


# Mostrar la imagen
st.image(image, use_column_width=True)

# Mostrar el texto formateado
st.markdown(
    """
    <h2 style='color: #4a4a4a;'>Important Facts</h2>
    <p style='font-size: 1.1em; color: #6c757d;'>
        En este sentido, la revisión de la literatura permite analizar y reflexionar si la teoría y la investigación anterior sugiere una respuesta (aunque sea parcial) a la pregunta o las preguntas de investigación; o bien, si provee una orientación a seguir dentro del planteamiento del estudio (Lawrence y otros, citados por Hernández-Sampieri, 2014). 
    </p>
    """, unsafe_allow_html=True
)


# Crear el multiselect para seleccionar candidatos
candidates = df['candidate_name'].unique()
selected_candidates = st.multiselect('Select Candidates', candidates)

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
        'text': 'Daily Activity on Each Platform',
        'x': 0.5,
        'y': 0.9,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="Date",
    yaxis_title="Number of Posts",
    template="plotly_white",
    legend_title="Platform",
)

# Mostrar gráfico de líneas en Streamlit
st.plotly_chart(fig, use_container_width=True)
