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
from EDA.eda import filtered_data, plot_template, candidate_colors, plot_template_plotly

st.header("Graphs of the hypothesis")
st.write("The 10 days leading up to the elections, including debate days and key announcements, provide a representative sample of user behavior on social media.")

# Función para clasificar la hora del día
def classify_time_of_day(dt):
    if 0 <= dt.hour < 3:
        return 'Early Dawn'
    elif 3 <= dt.hour < 6:
        return 'Late Dawn'
    elif 6 <= dt.hour < 9:
        return 'Early Morning'
    elif 9 <= dt.hour < 12:
        return 'Morning'
    elif 12 <= dt.hour < 14:
        return 'Noon'
    elif 14 <= dt.hour < 17:
        return 'Afternoon'
    elif 17 <= dt.hour < 21:
        return 'Early Evening'
    else:
        return 'Night'

time_of_day_colors = {
    'Early Dawn': 'dimgray',
    'Late Dawn': 'lightsalmon',
    'Early Morning': 'gold',
    'Morning': 'orange',
    'Noon': 'lightcoral',
    'Afternoon': 'indianred',
    'Early Evening': 'maroon',
    'Night': 'darkblue'
}

# Identificar los días de la semana
filtered_data['week_day'] = pd.to_datetime(filtered_data['datetime']).dt.day_name()
week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
filtered_data['week_day'] = pd.Categorical(filtered_data['week_day'], categories=week_order, ordered=True)
st.write("###  User behavior according to day and time of the day ")

# Multiselect para seleccionar el periodo de tiempo
time_option = st.multiselect(
    "Select the time period:",
    options=["Entire campaign", "Last 10 days", "Select other dates"]
)

# Diccionario de los nombres de plataformas (mostrado en la lista y los nombres en la base de datos)
platform_mapping = {
    "Facebook": "facebook",
    "Twitter": "twitter",
    "Instagram": "instagram",
    "YouTube": "youtube"
}

# Multiselect para seleccionar la plataforma
db_selection = st.multiselect(
    "Select the platform:",
    list(platform_mapping.keys())
)

# Convertir la selección del usuario en nombres de columnas del DataFrame
selected_platforms = [platform_mapping[platform] for platform in db_selection if platform in platform_mapping]

# Filtrar los datos según la selección de la plataforma
if selected_platforms:
    filtered_platform_data = filtered_data[filtered_data['platform'].isin(selected_platforms)].copy()
else:
    st.warning("Please select at least one platform.")
    st.stop()

filtered_platform_data['datetime'] = pd.to_datetime(filtered_platform_data['datetime'])
filtered_platform_data['time_of_day'] = filtered_platform_data['datetime'].apply(classify_time_of_day)

# Crear DataFrame para los últimos 10 días
last_10_days = filtered_platform_data.loc[(filtered_platform_data['datetime'] >= '2024-05-24') & 
                                          (filtered_platform_data['datetime'] <= '2024-06-02')]

# Función para manejar el slider de fechas (ajustado para multiselect con un rango)
def get_custom_date_range():
    # Selección de rango de fechas con las fechas más antiguas y más recientes del dataset
    start_date = st.date_input("Start Date", min_value=filtered_platform_data['datetime'].min().date(), 
                               max_value=filtered_platform_data['datetime'].max().date())
    end_date = st.date_input("End Date", min_value=start_date, 
                             max_value=filtered_platform_data['datetime'].max().date())
    return start_date, end_date


########################## Gráfico 1 y 2 
# Crear la figura para el gráfico
fig = go.Figure()
fig2 = go.Figure()

# Manejo de las opciones de fecha seleccionadas (tiempo)
if "Select other dates" in time_option:
    start_date, end_date = get_custom_date_range()

    # Convertir start_date y end_date a datetime con la zona horaria correcta
    start_date = pd.to_datetime(start_date).tz_localize('America/Mexico_City')
    end_date = pd.to_datetime(end_date).tz_localize('America/Mexico_City')

    # Filtrar los datos según el rango de fechas seleccionado
    filtered_by_date = filtered_platform_data[(filtered_platform_data['datetime'] >= start_date) & 
                                              (filtered_platform_data['datetime'] <= end_date)]

    # Calcular el promedio de interacciones por día de la semana
    avg_interactions_by_day = filtered_by_date.groupby('week_day')['num_interaction'].mean().reset_index()
    avg_interactions_by_day['week_day'] = pd.Categorical(avg_interactions_by_day['week_day'], categories=week_order, ordered=True)

    fig.add_trace(go.Scatter(x=avg_interactions_by_day['week_day'], y=avg_interactions_by_day['num_interaction'], mode='markers+lines',
                             name='Selected dates', line=dict(color='#4c72b0')))
    
    # Calcular el promedio de interacciones por hora del día (time of day)
    filtered_by_date['time_of_day'] = filtered_by_date['datetime'].apply(classify_time_of_day)
    filtered_by_date['time_of_day'] = pd.Categorical(filtered_by_date['time_of_day'], categories=time_of_day_colors, ordered=True)
    avg_interactions_df2 = filtered_by_date.groupby('time_of_day')['num_interaction'].mean().reset_index()

    fig2.add_trace(go.Scatter(x=avg_interactions_df2['time_of_day'], y=avg_interactions_df2['num_interaction'], mode='markers+lines',
                             name='Selected dates', line=dict(color='#4c72b0')))

# Graficar según la selección del usuario
if "Entire campaign" in time_option:
    full_period = filtered_platform_data.groupby(['week_day'])['num_interaction'].mean().reset_index()
    full_period['week_day'] = pd.Categorical(full_period['week_day'], categories=week_order, ordered=True)
    fig.add_trace(go.Scatter(x=full_period['week_day'], y=full_period['num_interaction'], mode='markers+lines',
                             name='Full Period', line=dict(color='lightsteelblue')))
    
    filtered_platform_data['time_of_day'] = filtered_platform_data['datetime'].apply(classify_time_of_day)
    filtered_platform_data['time_of_day'] = pd.Categorical(filtered_platform_data['time_of_day'], categories=time_of_day_colors, ordered=True)
    avg_interactions_df2 = filtered_platform_data.groupby('time_of_day')['num_interaction'].mean().reset_index()
    fig2.add_trace(go.Scatter(x=avg_interactions_df2['time_of_day'], y=avg_interactions_df2['num_interaction'], mode='markers+lines',
                             name='Full Period', line=dict(color='lightsteelblue')))

if "Last 10 days" in time_option:
    last_days = last_10_days.groupby(['week_day'])['num_interaction'].mean().reset_index()
    last_days['week_day'] = pd.Categorical(last_days['week_day'], categories=week_order, ordered=True)
    fig.add_trace(go.Scatter(x=last_days['week_day'], y=last_days['num_interaction'], mode='markers+lines',
                             name='Last 10 Days', line=dict(color='#1b9e77')))
    
    last_10_days['time_of_day'] = last_10_days['datetime'].apply(classify_time_of_day)
    last_10_days['time_of_day'] = pd.Categorical(last_10_days['time_of_day'], categories=time_of_day_colors, ordered=True)
    avg_interactions_df2 = last_10_days.groupby('time_of_day')['num_interaction'].mean().reset_index()
    fig2.add_trace(go.Scatter(x=avg_interactions_df2['time_of_day'], y=avg_interactions_df2['num_interaction'], mode='markers+lines',
                             name='Last 10 Days', line=dict(color='#1b9e77')))

# Aplicar el formato con plot_template_plotly
plot_template_plotly(
    fig,
    suptitle='Average Interaction',
    title='Comparison of Average Interactions over Days of the Week.',
    suptitle_x=0.312, suptitle_y=0.9,
    title_x=0.04, title_y=1.1
)

plot_template_plotly(
    fig2,
    suptitle='Average Interactions by Time of Day',
    title='Comparison of Average Interactions over Time of Day',
    suptitle_x=0.519, suptitle_y=0.9,
    title_x=0.04, title_y=1.1
)

# Mostrar los gráficos en Streamlit
st.plotly_chart(fig)
st.plotly_chart(fig2)


st.write("## Comparison between full period and last 10 days or selected week")

time_option = st.selectbox("Select Time Period for Comparison:", ["Last 10 days", "Select a week"])
if time_option == "Last 10 days":
    df= last_10_days
    comparison_title = "Last 10 days"
else:
    comparison_title = "Selected Week"
    min_date = filtered_platform_data['datetime'].min().date()
    max_date = filtered_platform_data['datetime'].max().date()
    # Si se selecciona "Otra semana", permitir al usuario elegir una fecha desde min_date
    selected_date = st.date_input("Select a start date for the week", min_value=min_date, max_value=max_date)
    selected_date = pd.to_datetime(selected_date).tz_localize('America/Mexico_City')  # Convertir a datetime con zona horaria
    df = filtered_platform_data[
        (filtered_platform_data['datetime'] >= selected_date) &
        (filtered_platform_data['datetime'] < selected_date + timedelta(days=7))
    ]



####################### GRÁFICO CANDIDATOS
# Gráficos de preferencias de candidatos según el día de la semana
st.write("### Difference in candidate preference according to the day of the week (selected platforms)")

# Filtrar y preparar los datos
full_period = filtered_platform_data.groupby(['week_day', 'candidate_name'])['num_interaction'].mean().reset_index()
full_period['week_day'] = pd.Categorical(full_period['week_day'], categories=week_order, ordered=True)
second_candidate_graph = df.groupby(['week_day', 'candidate_name'])['num_interaction'].mean().reset_index()
second_candidate_graph['week_day'] = pd.Categorical(second_candidate_graph['week_day'], categories=week_order, ordered=True)

# Pivotar las tablas para tener los candidatos como columnas
full_period_pivot = full_period.pivot(index='week_day', columns='candidate_name', values='num_interaction').fillna(0)
second_candidate_graph_pivot = second_candidate_graph.pivot(index='week_day', columns='candidate_name', values='num_interaction').fillna(0)

# Convertir las tablas pivotadas a formato largo para Plotly
full_period_long = full_period_pivot.reset_index().melt(id_vars='week_day', var_name='candidate_name', value_name='num_interaction')
second_candidate_graph_long = second_candidate_graph_pivot.reset_index().melt(id_vars='week_day', var_name='candidate_name', value_name='num_interaction')

# Crear una figura con dos subgráficos (en una fila)
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=['Full Period', comparison_title],
    shared_yaxes=True,
    vertical_spacing=0.1
)

# Agregar gráfico apilado para el periodo completo
for candidate in full_period_pivot.columns:
    fig.add_trace(
        go.Bar(
            x=full_period_long['week_day'],
            y=full_period_long[full_period_long['candidate_name'] == candidate]['num_interaction'],
            name=candidate,
            hoverinfo='x+y+name',
            marker=dict(color=candidate_colors.get(candidate, 'gray')),  # Usar los colores de la paleta candidate_colors
            orientation='v'
        ),
        row=1, col=1
    )

# Agregar gráfico apilado para el periodo seleccionado
for candidate in second_candidate_graph_pivot.columns:
    fig.add_trace(
        go.Bar(
            x=second_candidate_graph_long['week_day'],
            y=second_candidate_graph_long[second_candidate_graph_long['candidate_name'] == candidate]['num_interaction'],
            name=candidate,
            hoverinfo='x+y+name',
            marker=dict(color=candidate_colors.get(candidate, 'gray')),  # Usar los colores de la paleta candidate_colors
            orientation='v'
        ),
        row=1, col=2
    )

# Actualizar el layout para mejorar la visualización
fig.update_layout(
    title_text="Average Interaction per Candidate",
    barmode='stack',
    xaxis_title="Day of the Week",
    yaxis_title="Average Interaction",
    xaxis=dict(tickmode='array', tickvals=week_order),  # Asegura el orden de los días de la semana
    showlegend=True,
    height=600,
    width=1200,
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)


####################### Heatmap
st.write("### Interactions depending the day and time of the day")
# Crear la tabla pivotada para los datos completos de la campaña
filtered_platform_data['datetime'] = pd.to_datetime(filtered_platform_data['datetime']).dt.tz_convert('America/Mexico_City')
heatmap_data_df2 = filtered_platform_data.pivot_table(
    index='week_day', 
    columns='time_of_day', 
    values='num_interaction', 
    aggfunc='mean'
)
heatmap_data_df2 = heatmap_data_df2.reindex(week_order)  # Ordenar días de la semana
heatmap_data_df2 = heatmap_data_df2[list(time_of_day_colors.keys())]  # Ordenar horas del día

second_heatmap = df.pivot_table(
    index='week_day', 
    columns='time_of_day', 
    values='num_interaction', 
    aggfunc='mean'
)
second_heatmap = second_heatmap.reindex(week_order)  # Ordenar días de la semana
second_heatmap = second_heatmap[list(time_of_day_colors.keys())]  # Ordenar horas del día

# Crear los heatmaps
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 6))

# Heatmap para la campaña completa
sns.heatmap(heatmap_data_df2, annot=False, cmap="YlGnBu", ax=axes2[0])
axes2[0].set_title('Full Campaign')
axes2[0].set_xlabel('Time of Day')
axes2[0].set_ylabel('Day of the Week')
axes2[0].set_xticklabels(axes2[0].get_xticklabels(), rotation=45)

# Heatmap para el periodo seleccionado (Últimos 10 días u otra semana)
sns.heatmap(second_heatmap, annot=False, cmap="YlGnBu", ax=axes2[1], cbar_kws={'label': 'Average Interactions'})
axes2[1].set_title(comparison_title)
axes2[1].set_xlabel('Time of Day')
axes2[1].set_xticklabels(axes2[1].get_xticklabels(), rotation=45)

# Personalizar la apariencia de los heatmaps
plot_template(
    suptitle='Average Interactions Heatmap Comparison',
    suptitle_dict={'x': 0.465, 'y': 0.97},
    title_dict={'x': 0.38, 'y': 1.095},
)

plt.tight_layout()
st.pyplot(fig2)

############## Cambios en los topics
st.write("### Most discussed topics")

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
wordcloud_campaign = generate_wordcloud(filtered_platform_data)
wordcloud_df = generate_wordcloud(df)

# Crear una figura con dos subgráficas para mostrar las nubes de palabras
fig, axes = plt.subplots(1, 2, figsize=(15, 7))

# Mostrar nubes de palabras
axes[0].imshow(wordcloud_campaign, interpolation='bilinear')
axes[0].set_title("Entire campaign")
axes[0].axis('off')  # Quitar los ejes

axes[1].imshow(wordcloud_df, interpolation='bilinear')
axes[1].set_title(comparison_title)
axes[1].axis('off')  # Quitar los ejes

# Mostrar la figura en Streamlit
st.pyplot(fig)


############### Users más activos y sus diferencias en actividad
st.write("### Most Relevant User")
# Contar interacciones por usuario
user_interactions_recent = df.groupby('username')['num_interaction'].sum().reset_index()

# Contar publicaciones por usuario en los últimos 10 días (last_10_days)
user_posts_recent = df.groupby('username').size().reset_index(name='post_count_recent')

# Unir las interacciones y las publicaciones para los últimos 10 días
user_interactions_recent = pd.merge(user_interactions_recent, user_posts_recent, on='username')

# Calcular el promedio de interacciones por publicación en los últimos 10 días
user_interactions_recent['avg_interaction_recent'] = user_interactions_recent['num_interaction'] / user_interactions_recent['post_count_recent']

# Ordenar por promedio de interacciones (de mayor a menor)
user_interactions_recent = user_interactions_recent.sort_values(by='avg_interaction_recent', ascending=False)

# Obtener los 10 usuarios principales basados en el promedio de interacciones en los últimos 10 días
top_10_users = user_interactions_recent.head(10)

# Contar interacciones por usuario para toda la campaña (df2)
user_interactions_all = filtered_platform_data.groupby('username')['num_interaction'].sum().reset_index(name='interaction_count_all')

# Contar publicaciones por usuario para toda la campaña
user_posts_all = filtered_platform_data.groupby('username').size().reset_index(name='post_count_all')

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
    name=comparison_title,
    marker=dict(color='#4c72b0'),
    hoverinfo='x+y+name'
))

# Agregar las barras para toda la campaña
fig.add_trace(go.Bar(
    x=merged_df['username'],
    y=merged_df['avg_interaction_all'],
    name='Entire Campaign',
    marker=dict(color='lightsteelblue'),
    hoverinfo='x+y+name'
))

# Configurar el diseño del gráfico
fig.update_layout(
    title="Comparison of Average Interactions per Post by User: Last 10 Days vs. Entire Campaign",
    xaxis_title="Username",
    yaxis_title="Average Interactions per Post",
    barmode='group',  # Barra agrupada (no apilada)
    xaxis=dict(tickangle=45),  # Rotar etiquetas del eje x
    legend=dict(title="Period"),
    height=600
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)




