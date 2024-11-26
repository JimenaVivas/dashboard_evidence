import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


# Configurar título de la aplicación
st.title("Análisis de Sentimientos por Candidato")
st.write("Visualiza la distribución de sentimientos y predice el sentimiento de una frase.")

# Cargar los datos directamente desde los archivos especificados
complete_data = "ml/Sentiment_data.csv"
training_data_path = "ml/x-senti-labelled_and_lematized.csv"
svm_model_path = "ml/svm_model_updated.sav"

# Cargar datos completos
df = pd.read_csv(complete_data)
df_complete = df.dropna(subset=['lematiz_tweet'])

# Visualizar la distribución de sentimientos por candidato
sentiment_per_candidate = df_complete.groupby(['candidate_name', 'Sentiment'])['Sentiment'].count().reset_index(name='count')
color_scale = {'negative': 'red', 'neutral': 'gray', 'positive': 'green'}

st.subheader("Distribución de Sentimientos por Candidato (Campaña Completa)")
fig_bar = px.bar(
    sentiment_per_candidate, 
    x='candidate_name', 
    y='count', 
    color='Sentiment',
    color_discrete_sequence=[color_scale[sentiment] for sentiment in sentiment_per_candidate['Sentiment'].unique()],
    barmode='group',
    title='Distribución de Sentimientos por Candidato'
)
st.plotly_chart(fig_bar)

# Gráfico de Sunburst
custom_colors = {
    "Jorge Álvarez Máynez": "orange",
    "Claudia Sheinbaum": "maroon",
    "Xóchitl Gálvez": "royalblue"
}

st.subheader("Diagrama de Sunburst de Sentimientos")
fig_sunburst = px.sunburst(
    sentiment_per_candidate, 
    path=['candidate_name', 'Sentiment'], 
    values='count',
    color='candidate_name',
    color_discrete_map=custom_colors
)
st.plotly_chart(fig_sunburst)

# Cargar datos de entrenamiento
df_train = pd.read_csv(training_data_path)
df_train = df_train.dropna(subset=['lematiz_tweet'])

# Combinar texto para ajustar el vectorizador
all_text = df_complete['lematiz_tweet'].tolist() + df_train['lematiz_tweet'].tolist()
tfidf = TfidfVectorizer()
tfidf.fit(all_text)

# Cargar el modelo SVM
with open(svm_model_path, "rb") as model_file:
    svm_model = pickle.load(model_file)

# Función para predecir sentimiento
def predict_sentiment(phrase, tfidf, svm_model):
    """Predice el sentimiento de una frase."""
    phrase = phrase.lower()
    phrase_features = tfidf.transform([phrase])
    sentiment = svm_model.predict(phrase_features)[0]
    return sentiment

# Entrada del usuario para la predicción
st.subheader("Predicción de Sentimientos")
user_phrase = st.text_input("Introduce una frase para predecir el sentimiento:")

if user_phrase:
    sentiment = predict_sentiment(user_phrase, tfidf, svm_model)
    st.write("El sentimiento expresado en la frase es:", sentiment)

