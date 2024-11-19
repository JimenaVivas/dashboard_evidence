from EDA.eda import filtered_data,  plot_template_plotly, last_10_days_df
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pytz
import re
from wordcloud import WordCloud, STOPWORDS
from datetime import timedelta



st.title('Cambios en el comportamiento de los usuarios')
st.write("### Temas más recurrentes")
st.write("Se observa a continuación el cambio de temas más recurrentes en la campaña y cómo cambio su frecuencia.")

# Diccionario de sinónimos (para evitar palabras repetitivas)
dictionary = {
    'ClaudiaSheinbaum': ['Claudia', 'Sheinbaum', 'claudia','claudiapresidenta', 'sheinbaum', 'dra', 'doctora', 'Claudiashein','claudiashein','claudiasheinbaum'],
    'XóchitlGálvez': ['Xóchitl', 'gálvez','Gálvez', 'xóchitl', 'galvez', 'glvez', 'xchitl', 'xochitl', 'XochitlGalvez','xochitlgalvez','xochitl2024','xóchitlgálvez'],
    'CDMX': ['cdmx', 'ciudad'],
    'metro': ['lnea', 'metro', '12'],
    '4t': ['4t', 'cuarta', 'transformacin', 'transformacion','transformación','t'],
    'marea_rosa': ['marcha', 'marea', 'rosa', 'mayo19', '19', 'bandera', 'bandera10am','marea_rosa'],
    'PRIAN': ['pri', 'pan', 'prian'],
    'voto': ['vota','voto','votar','VOTO'],
    'AMLO':['amlo','lopezobrador','AMLO','lopezobrador_'],
    'ÁlvarezMáynez': ['jorge', 'alvarez', 'alvarezmaynez','máynez','maynez','alvarez','alvarez_maynez']
}

# Función para reemplazar palabras por sus sinónimos usando el diccionario proporcionado
def replace_dictionary(text):
    text = text.lower()  # Convertir a minúsculas para insensibilidad a mayúsculas
    for key, values in dictionary.items():
        # Crear un patrón regex que incluya todos los sinónimos
        pattern = r'\b(' + '|'.join(map(re.escape, values)) + r')\b'
        text = re.sub(pattern, key.lower(), text)  # Reemplazar sinónimos por la clave en minúsculas
    return text

# Lista de palabras irrelevantes
irrelevant_words = set(STOPWORDS)
irrelevant_words.update([
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por",
    "un", "para", "con", "no", "una", "su", "al", "es", "lo", "como", "más",
    "pero", "sus", "le", "ya", "o", "fue", "este", "ha", "sí", "porque", "esta",
    "son", "entre", "cuando", "muy", "sin", "sobre", "también", "me", "hasta",
    "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno",
    "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto",
    "mí", "antes", "algunos", "qué", "unos", "yo", "otro", "otras", "otra",
    "él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual",
    "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis",
    "tú", "te", "ti", "tu", "tus", "ellas", "https", "co", "sí", "si", "usted",
    "así", "ustedes", "dice", "después", "cómo", "pues"
])

# Generación de la nube de palabras para el conjunto de datos de la campaña completa
def generate_wordcloud(data):
    all_words = ' '.join([str(text) for text in data['text'] if isinstance(text, str)])
    all_words_with_synonyms = replace_dictionary(all_words)  # Reemplazar sinónimos
    wordcloud = WordCloud(
        width=800,
        height=400,
        stopwords=irrelevant_words,
        background_color=None,
        mode="RGBA",
        collocations=False
    ).generate(all_words_with_synonyms)
    return wordcloud

# Generar nubes de palabras
wordcloud_campaign = generate_wordcloud(filtered_data)
wordcloud_df = generate_wordcloud(last_10_days_df)

# Crear una figura con dos subgráficas para mostrar las nubes de palabras
fig, axes = plt.subplots(1, 2, figsize=(15, 7))

# Mostrar nubes de palabras
axes[0].imshow(wordcloud_campaign, interpolation='bilinear')
axes[0].set_title("Campaña Entera")
axes[0].axis('off')  # Quitar los ejes

axes[1].imshow(wordcloud_df, interpolation='bilinear')
axes[1].set_title("Últimos 10 Días")
axes[1].axis('off')  # Quitar los ejes

# Mostrar la figura en Streamlit
st.pyplot(fig)

############### Users más activos y sus diferencias en actividad
st.write("### Usuarios más relevantes")
st.write("En las siguientes gráficas se puede comparar el cambio en número de interacciones los usuarios más relevantes en los últimos 10 dás. esto nos permite conocer si su actividad fue constante o si cambio en la última fase de la campaña.")

# Contar interacciones por usuario
user_interactions_recent = last_10_days_df.groupby('username')['num_interaction'].sum().reset_index()

# Contar publicaciones por usuario en los últimos 10 días (last_10_days)
user_posts_recent = last_10_days_df.groupby('username').size().reset_index(name='post_count_recent')

# Unir las interacciones y las publicaciones para los últimos 10 días
user_interactions_recent = pd.merge(user_interactions_recent, user_posts_recent, on='username')

# Calcular el promedio de interacciones por publicación en los últimos 10 días
user_interactions_recent['avg_interaction_recent'] = user_interactions_recent['num_interaction'] / user_interactions_recent['post_count_recent']

# Ordenar por promedio de interacciones (de mayor a menor)
user_interactions_recent = user_interactions_recent.sort_values(by='avg_interaction_recent', ascending=False)

# Obtener los 10 usuarios principales basados en el promedio de interacciones en los últimos 10 días
top_10_users = user_interactions_recent.head(10)

# Contar interacciones por usuario para toda la campaña (df2)
user_interactions_all = filtered_data.groupby('username')['num_interaction'].sum().reset_index(name='interaction_count_all')

# Contar publicaciones por usuario para toda la campaña
user_posts_all = filtered_data.groupby('username').size().reset_index(name='post_count_all')

# Unir las interacciones y las publicaciones para toda la campaña
user_interactions_all = pd.merge(user_interactions_all, user_posts_all, on='username')

# Calcular el promedio de interacciones por publicación para toda la campaña
user_interactions_all['avg_interaction_all'] = user_interactions_all['interaction_count_all'] / user_interactions_all['post_count_all']

# Unir los dataframes
merged_df = pd.merge(top_10_users, user_interactions_all[['username', 'avg_interaction_all']], on='username', how='left')

# Crear un gráfico de barras con Plotly
import plotly.graph_objects as go

# Crear el gráfico de barras
fig = go.Figure()

# Agregar las barras para los últimos 10 días
fig.add_trace(go.Bar(
    x=merged_df['username'],
    y=merged_df['avg_interaction_recent'],
    name='Últimos 10 Días',
    marker=dict(color='#4c72b0'),
    hoverinfo='x+y+name'
))

# Agregar las barras para toda la campaña
fig.add_trace(go.Bar(
    x=merged_df['username'],
    y=merged_df['avg_interaction_all'],
    name='Campaña Entera',
    marker=dict(color='lightsteelblue'),
    hoverinfo='x+y+name'
))

# Configurar el diseño del gráfico
fig.update_layout(
    title="Comparación de Interacciones Promedio por Publicación por Usuario: Últimos 10 Días vs. Toda la Campaña",
    xaxis_title="Username",
    yaxis_title="Interacciones Promedio por Publicación",
    barmode='group',  # Barra agrupada (no apilada)
    xaxis=dict(tickangle=45),  # Rotar etiquetas del eje x
    legend=dict(title="Period"),
    height=600
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)





