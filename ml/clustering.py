from ml.ml_analysis import tfidf, svm_model
import streamlit as st
import pandas as pd
import zipfile
import numpy as np
import matplotlib.pyplot as plt
# Sklearn libraries for feature extraction, dimensionality reduction, and SVM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.svm import SVC
import os
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from PIL import Image
# Ignore warnings (optional)
import warnings
warnings.filterwarnings('ignore')

st.header("Clustering")
merged_df = pd.read_csv('ml/Complete_Data.csv')

# Ensure datetime column is in datetime format
merged_df['datetime'] = pd.to_datetime(merged_df['datetime'], errors='coerce')

# Ensure there are no rows with NaT values in the 'datetime' column
merged_df = merged_df.dropna(subset=['datetime'])

# Define the date range
begin_date = '2024-03-01 00:00:00'
end_date = '2024-06-02 00:00:00'
merged_df = merged_df.loc[(merged_df['datetime'] >= begin_date) & (merged_df['datetime'] <= end_date)]

# Calculate the start date of the last 10-day period in the range
last_ten_days_start = pd.to_datetime(end_date) - pd.Timedelta(days=10)

# Filter to only include data from the last 10 days
merged_df2= merged_df.loc[merged_df['datetime'] >= last_ten_days_start]

# Ruta del archivo
file_path = "ml/merged_df.pkl"
with open(file_path, "rb") as file:
    merged_df = pd.read_pickle(file)

# Gráfica 3D PCA
st.subheader("Representación de los clusters")
fig = plt.figure(figsize=(7.5, 5.25))  
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(
    merged_df['pca_one'], merged_df['pca_two'], merged_df['pca_three'],
    c=merged_df['cluster_label'], cmap='viridis', alpha=0.7
)
plt.colorbar(sc, ax=ax, label='Cluster Label')
ax.set_title('3D PCA of Clusters')
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_zlabel('Principal Component 3')
# Mostrar la gráfica en Streamlit
st.write("Nuestro objetivo con procesos de clustering era dividir el texto en grupos bien definidos para analizar diferentes temas de interés y el sentimiento atribuido en las campañas y en los últimos 10 días. Utilizamos TF-IDF y Word2Vec para crear los vectores numéricos y K Means para hacer el clustering (manteniendo 3 grupos), nos quedamos con los clusters obtenidos con los vectores de Word2Vec pero como se puede ver no estaban bien definidos. Procedimos a sacar una muestra de los 1,500 puntos más cercanos a los centroides con lo cual conseguimos clusters bien definidos para analizar.")
st.pyplot(fig)

# Cargar y mostrar la imagen
image = Image.open('images/clusters.jpg')
# Mostrar la imagen en Streamlit
st.image(image, use_container_width=True)

st.write("## Sentiment Analysis y Key Topics")
st.write("En esta sección mostramos nuestros insights del proceso de clustering. Medimos la proporción de sentimiento en todos los datos de las campañas presidenciales, en la muestra de los puntos más cercanos a los centroides y de los 10 días antes de la campaña. Además también medimos las palabras más utilizadas en cada dataset para ver si los temas más relevantes tuvieron un cambio significativo. Como se puede observar, las proporciones de sentimiento y los temas clave se mantuvieron muy similares. ")
st.write("Cluster 1: Claudia Sheinbaum - Tendencia positiva")
st.write("Cluster 2: Votación - Tendencia negativa")
st.write("Cluster 3: Elección presidencial - Tendencia negativa")

# Verificar columnas necesarias en merged_df2
if 'cluster_label' not in merged_df2.columns or 'Sentiment' not in merged_df2.columns:
    st.error("Las columnas 'cluster_label' y 'Sentiment' deben estar en merged_df2.")
else:
    # Mapear los nombres de los clusters
    cluster_labels_mapping = {
        0: "Claudia Sheinbaum",
        1: "Candidatos",
        2: "Elección Presidencial"
    }

    # Distribución de sentimientos por cluster
    sentiment_distribution = merged_df2.groupby(['cluster_label', 'Sentiment']).size().unstack(fill_value=0)
    sentiment_proportions = sentiment_distribution.div(sentiment_distribution.sum(axis=1), axis=0)

    # Etiquetas y colores
    sentiment_labels = ['Negative', 'Neutral', 'Positive']
    sentiment_colors = ['red', 'gray', 'green']

    # Gráfica de barras apiladas
    fig, ax = plt.subplots(figsize=(9, 4.5))  # Reducción al 75% del tamaño original
    sentiment_proportions.rename(index=cluster_labels_mapping).plot(kind='bar', stacked=True, color=sentiment_colors, ax=ax)

    ax.set_title("Proporción de Sentimientos por Cluster en los Últimos 10 Días", fontsize=16)
    ax.set_xlabel("Clusters", fontsize=12)
    ax.set_ylabel("Proporción", fontsize=12)
    ax.set_xticklabels(cluster_labels_mapping.values(), rotation=0)
    ax.legend(sentiment_labels, title="Sentiment")
    plt.tight_layout()

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)


############### Segundo Sentiment Proportion
# Verificar columnas requeridas
if 'cluster_label' not in merged_df.columns or 'Sentiment' not in merged_df.columns:
    st.error("Las columnas 'cluster_label' y 'Sentiment' deben estar en el DataFrame.")
else:
    # Mapear nombres de los clusters
    cluster_labels_mapping = {
        0: "Claudia Sheinbaum",
        1: "Candidatos",
        2: "Elección Presidencial"
    }
st.markdown("<br>", unsafe_allow_html=True)  

    # Distribución de sentimientos por cluster
sentiment_distribution = merged_df.groupby(['cluster_label', 'Sentiment']).size().unstack(fill_value=0)
sentiment_proportions = sentiment_distribution.div(sentiment_distribution.sum(axis=1), axis=0)

    # Etiquetas y colores
sentiment_labels = ['Negative', 'Neutral', 'Positive']
sentiment_colors = ['red', 'gray', 'green']

    # Gráfica de barras apiladas
fig, ax = plt.subplots(figsize=(9, 4.5))  # Reducción al 75% del tamaño original
sentiment_proportions.rename(index=cluster_labels_mapping).plot(kind='bar', stacked=True, color=sentiment_colors, ax=ax)

ax.set_title("Proporción de Sentimientos por Cluster (Campaña Completa)", fontsize=16)
ax.set_xlabel("Clusters", fontsize=12)
ax.set_ylabel("Proportion", fontsize=12)
ax.set_xticklabels(cluster_labels_mapping.values(), rotation=0)
ax.legend(sentiment_labels, title="Sentiment")
plt.tight_layout()

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

############### Tercer Sentiment Proportion (Se anexa como imagen porque su cálculo ralentizaba mucho la página)
st.header("Proporción de Sentimientos por Cluster (Sample Testing)")
# Cargar y mostrar la imagen
image = Image.open('images/sentpro.jpg')
# Mostrar la imagen en Streamlit
st.image(image, use_container_width=True)


#################################### Keywords
# Título de la aplicación
st.title("Análisis de Palabras Clave en el Periodo Completo")

# Subtítulo para Claudia Sheinbaum
st.subheader("Claudia Sheinbaum")

# Lista con las palabras más mencionadas para Claudia Sheinbaum
claudia_keywords = {
    "mexico": 7856,
    "presidenta": 5186,
    "ClaudiaSheinbaum": 4690,
    "junio": 2221,
    "transformacion": 1898,
    "proxima": 1820,
    "mujer": 1815,
    "mejor": 1776,
    "futuro": 1738,
    "pais": 1693
}

# Mostrar en lista visualmente atractiva
for keyword, count in claudia_keywords.items():
    st.markdown(f"* **{keyword}**: {count}")

# Agregar un espacio vacío
st.markdown("<br>", unsafe_allow_html=True)

# Subtítulo para Candidatos
st.subheader("Candidatos")

# Lista con las palabras más mencionadas para Candidatos
candidates_keywords = {
    "bien": 1876,
    "hijo": 1574,
    "corrupto": 1494,
    "madre": 1358,
    "creer": 1345,
    "esquirol": 1287,
    "JorgeMaynez": 1272,
    "XóchitlGálvez": 1231,
    "ClaudiaSheinbaum": 1100,
    "pendejo": 969
}

# Mostrar en lista visualmente atractiva
for keyword, count in candidates_keywords.items():
    st.markdown(f"* **{keyword}**: {count}")

# Agregar un espacio vacío
st.markdown("<br>", unsafe_allow_html=True)

# Subtítulo para Votación / Elección
st.subheader("Votación / Elección")

# Lista con las palabras más mencionadas para Votación / Elección
voting_keywords = {
    "XóchitlGálvez": 6829,
    "ClaudiaSheinbaum": 6158,
    "voto": 4911,
    "candidata": 4517,
    "Morena": 4301,
    "votar": 4257,
    "mexico": 4140,
    "candidato": 3974,
    "JorgeMaynez": 3564,
    "campán": 3552
}

# Mostrar en lista visualmente atractiva
for keyword, count in voting_keywords.items():
    st.markdown(f"* **{keyword}**: {count}")



# Título de la aplicación
st.title("Análisis de Palabras Clave en Sample Testing")

# Subtítulo para Claudia Sheinbaum
st.subheader("Claudia Sheinbaum")

# Lista con las palabras más mencionadas para Claudia Sheinbaum en Sample Testing
claudia_keywords_sample_testing = {
    "mexico": 823,
    "presidenta": 654,
    "ClaudiaSheinbaum": 500,
    "proxima": 238,
    "proximo": 215,
    "transformacion": 173,
    "junio": 161,
    "pais": 160,
    "futuro": 157,
    "junto": 156
}

# Mostrar en lista visualmente atractiva
for keyword, count in claudia_keywords_sample_testing.items():
    st.markdown(f"* **{keyword}**: {count}")

# Agregar un espacio vacío
st.markdown("<br>", unsafe_allow_html=True)

# Subtítulo para Candidatos
st.subheader("Candidatos")

# Lista con las palabras más mencionadas para Candidatos en Sample Testing
candidates_keywords_sample_testing = {
    "XóchitlGálvez": 28,
    "ClaudiaSheinbaum": 25,
    "bien": 23,
    "vez": 21,
    "creer": 21,
    "mejor": 21,
    "ahi": 18,
    "siempre": 18,
    "pasar": 17,
    "tal": 15
}

# Mostrar en lista visualmente atractiva
for keyword, count in candidates_keywords_sample_testing.items():
    st.markdown(f"* **{keyword}**: {count}")

# Agregar un espacio vacío
st.markdown("<br>", unsafe_allow_html=True)

# Subtítulo para Votación / Elección
st.subheader("Votación / Elección")

# Lista con las palabras más mencionadas para Votación / Elección en Sample Testing
voting_keywords_sample_testing = {
    "ClaudiaSheinbaum": 283,
    "XóchitlGálvez": 216,
    "mexico": 187,
    "candidata": 159,
    "Morena": 107,
    "candidato": 105,
    "voto": 94,
    "campán": 92,
    "AMLO": 83,
    "ganar": 77
}

# Mostrar en lista visualmente atractiva
for keyword, count in voting_keywords_sample_testing.items():
    st.markdown(f"* **{keyword}**: {count}")



# Título de la aplicación
st.title("Análisis de Palabras Clave en los Últimos 10 Días")

# Subtítulo para Claudia Sheinbaum
st.subheader("Claudia Sheinbaum")

# Lista con las palabras más mencionadas para Claudia Sheinbaum en los últimos 10 días
claudia_keywords_last_10_days = {
    "mexico": 56,
    "presidenta": 42,
    "ClaudiaSheinbaum": 37,
    "junio": 27,
    "votar": 22,
    "campán": 20,
    "junto": 18,
    "gran": 16,
    "distrito": 14,
    "cierre": 13
}

# Mostrar en lista visualmente atractiva
for keyword, count in claudia_keywords_last_10_days.items():
    st.markdown(f"* **{keyword}**: {count}")

# Agregar un espacio vacío
st.markdown("<br>", unsafe_allow_html=True)

# Subtítulo para Candidatos
st.subheader("Candidatos")

# Lista con las palabras más mencionadas para Candidatos en los últimos 10 días
candidates_keywords_last_10_days = {
    "JorgeMaynez": 22,
    "cobarde": 19,
    "esquirol": 15,
    "nadie": 13,
    "corrupto": 13,
    "tragedia": 12,
    "pinche": 10,
    "votar": 9,
    "ahi": 9,
    "muerto": 9
}

# Mostrar en lista visualmente atractiva
for keyword, count in candidates_keywords_last_10_days.items():
    st.markdown(f"* **{keyword}**: {count}")

# Agregar un espacio vacío
st.markdown("<br>", unsafe_allow_html=True)

# Subtítulo para Votación / Elección
st.subheader("Votación / Elección")

# Lista con las palabras más mencionadas para Votación / Elección en los últimos 10 días
voting_keywords_last_10_days = {
    "voto": 44,
    "ClaudiaSheinbaum": 41,
    "votar": 39,
    "mexico": 38,
    "XóchitlGálvez": 33,
    "campán": 30,
    "JorgeMaynez": 29,
    "Morena": 29,
    "ganar": 26,
    "gobierno": 23
}

# Mostrar en lista visualmente atractiva
for keyword, count in voting_keywords_last_10_days.items():
    st.markdown(f"* **{keyword}**: {count}")