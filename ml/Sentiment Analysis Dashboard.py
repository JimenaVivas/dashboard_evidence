#Start by importing any important library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pickle import dump
from pickle import load
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import plotly.express as px
import

#Let's locate the datset, it is a csv file
complete_data="Sentiment_data.csv"

#It looks good, let's search if there are any missing values in the Sentiment column or otherwise
df = pd.read_csv("complete_data")
df_complete = df.dropna(subset=['lematiz_tweet'])

#Let's visualize the sentiment disribution per candidate
sentiment_per_candidate = df_complete.groupby(['candidate_name', 'Sentiment'])['Sentiment'].count().reset_index(name='count')
# Define a color scale for your sentiments
color_scale = {'negative': 'red', 'neutral': 'gray', 'positive': 'green'}

# Create the bar plot using a custom color scale
fig = px.bar(
    sentiment_per_candidate, 
    x='candidate_name', 
    y='count', 
    color='Sentiment',
    color_discrete_sequence=[color_scale[sentiment] for sentiment in sentiment_per_candidate['Sentiment'].unique()], # Apply custom color scale
    barmode='group',
    title='Distribución de Sentimientos por Candidato'
)

fig.show()

# Create a DataFrame with Sentiment counts
sentiment_per_candidate = df_complete.groupby(['candidate_name', 'Sentiment'])['Sentiment'].count().reset_index(name='count')

# Define custom colors for candidates
custom_colors = {
    "Jorge Álvarez Máynez": "orange",
    "Claudia Sheinbaum": "maroon",  # You can use color names or hex codes
    "Xóchitl Gálvez": "royalblue"
}

# Create the sunburst chart with custom colors
fig_sunburst = px.sunburst(
    sentiment_per_candidate, 
    path=['candidate_name', 'Sentiment'], 
    values='count',
    color='candidate_name',  # Color based on candidate
    color_discrete_map=custom_colors  # Apply custom color map
)
fig_sunburst.show()

#Let's try to create a program able to predict the sentiment expressed on a sentence typed in by a user
#First, we want to load the data used to train the predictive model
training_data_path=("x-senti-labelled_and_lematized.csv")
df_train = pd.read_csv(training_data_path)

#Let's delete the entries from the lematiz_tweet column that have missing values
df_train=df_train.dropna(subset=['lematiz_tweet'])


#Combine all text data to fit the vectorizer
all_text = df_complete['lematiz_tweet'].tolist() + df_train['lematiz_tweet'].tolist()

#Let's fit the Tfidf vectorizer on all data
tfidf = TfidfVectorizer()
tfidf.fit(all_text)

#Let's transform all data into numerical features
num_features=tfidf.transform(df_complete['lematiz_tweet'])

#Let's load an already existing svm model 
svm_model=("svm_model_updated.sav","rb")

#Let's work on the prediction function
def predict_sentiment(phrase,tfidf):
  """Predice el Sentimiento expresado en una oración utilizando el nuevo modelo y el vectorizer
  """
  phrase=phrase.lower()
  phrase_features=tfidf.transform([phrase])
  sentiment=svm_model.predict(phrase_features)[0]
  return sentiment

#Interactive prediction on local environment
user_phrase=input("Introduzca una frase:")
sentiment=predict_sentiment(user_phrase,tfidf)
print("El sentimiento expresado en la frase es:",sentiment)


















# Cargar datos
data = pd.read_csv('ml/x-senti-labelled_and_lematized.csv', encoding='utf-8-sig')
data.rename(columns={'ï»¿datetime': 'datetime'}, inplace=True)

# Asegúrate de que la columna 'datetime' esté en formato datetime
data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')
data = data.dropna(subset=['datetime'])

# Filtrar por el rango de fechas
begin_date = '2024-03-01 00:00:00'
end_date = '2024-06-02 00:00:00'
filtered_data = data[(data['datetime'] >= begin_date) & (data['datetime'] <= end_date)]

# Calcular el inicio de los últimos 10 días en el rango
last_ten_days_start = pd.to_datetime(end_date) - pd.Timedelta(days=10)
last_ten_days_data = filtered_data[filtered_data['datetime'] >= last_ten_days_start]

# Cargar el modelo SVM y el vectorizador
try:
    svm_model = joblib.load('ml/svm_model_updated.sav')
    tfidf = joblib.load('ml/vectorizer.sav')
    st.write("Modelo y vectorizador cargados correctamente.")
except Exception as e:
    st.error(f"Error al cargar el modelo o el vectorizador: {e}")

# Rellenar NaN con cadenas vacías
data['lematiz_tweet'] = data['lematiz_tweet'].fillna('')

# Verificar que el vectorizador y el modelo coinciden con las dimensiones de los datos
tweet_features = tfidf.transform(data['lematiz_tweet'])

# Predecir los sentimientos con el modelo
try:
    predictions = svm_model.predict(tweet_features)
    data['Sentiment'] = predictions
    st.write("Predicciones realizadas exitosamente.")
except Exception as e:
    st.error(f"Error al hacer las predicciones: {e}")

# Gráfico 3D con PCA
def plot_3d_pca():
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(
        data['pca_one'], data['pca_two'], data['pca_three'],
        c=data['cluster_label'], cmap='icefire_r', alpha=0.7
    )
    plt.colorbar(sc, ax=ax, label='Cluster Label')
    ax.set_title('3D PCA of Clusters')
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_zlabel('Principal Component 3')
    st.pyplot(fig)

# Visualización de la distribución de sentimientos por clusters
def plot_sentiment_distribution():
    cluster_labels_mapping = {
        0: "Claudia Sheinbaum",
        1: "Candidatos",
        2: "Elección Presidencial"
    }

    sentiment_distribution = data.groupby(['cluster_label', 'Sentiment']).size().unstack(fill_value=0)
    sentiment_proportions = sentiment_distribution.div(sentiment_distribution.sum(axis=1), axis=0)

    sentiment_labels = ['Negative', 'Neutral', 'Positive']
    sentiment_colors = ['red', 'gray', 'green']

    fig, ax = plt.subplots(figsize=(12, 6))
    sentiment_proportions.rename(index=cluster_labels_mapping).plot(kind='bar', stacked=True, color=sentiment_colors, ax=ax)

    ax.set_title("Sentiment Proportion by Cluster", fontsize=16)
    ax.set_xlabel("Clusters", fontsize=12)
    ax.set_ylabel("Proportion", fontsize=12)
    ax.set_xticklabels(cluster_labels_mapping.values(), rotation=0)
    ax.legend(sentiment_labels, title="Sentiment")
    st.pyplot(fig)

# Visualización para los últimos 10 días
def plot_last_ten_days_sentiment_distribution():
    cluster_labels_mapping = {
        0: "Claudia Sheinbaum",
        1: "Candidatos",
        2: "Elección Presidencial"
    }

    sentiment_distribution = last_ten_days_data.groupby(['cluster_label', 'Sentiment']).size().unstack(fill_value=0)
    sentiment_proportions = sentiment_distribution.div(sentiment_distribution.sum(axis=1), axis=0)

    sentiment_labels = ['Negative', 'Neutral', 'Positive']
    sentiment_colors = ['red', 'gray', 'green']

    fig, ax = plt.subplots(figsize=(12, 6))
    sentiment_proportions.rename(index=cluster_labels_mapping).plot(kind='bar', stacked=True, color=sentiment_colors, ax=ax)

    ax.set_title("Sentiment Proportion by Cluster in the last 10 days", fontsize=16)
    ax.set_xlabel("Clusters", fontsize=12)
    ax.set_ylabel("Proportion", fontsize=12)
    ax.set_xticklabels(cluster_labels_mapping.values(), rotation=0)
    ax.legend(sentiment_labels, title="Sentiment")
    st.pyplot(fig)

# Crear la interfaz de usuario con Streamlit
st.title('Análisis de Sentimientos y Clústeres en Redes Sociales')

st.header('Visualización de Clústeres en 3D')
plot_3d_pca()

st.header('Distribución de Sentimientos por Clúster')
plot_sentiment_distribution()

st.header('Distribución de Sentimientos por Clúster en los Últimos 10 Días')
plot_last_ten_days_sentiment_distribution()