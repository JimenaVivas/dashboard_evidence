from Background.facts import filtered_data
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pytz
st.title("Interacciones de acuerdo al momento de interacción")

def plot_template_plotly(fig, suptitle="Este es el título principal",
                         title="Esta es una descripción general del gráfico",
                         logo=None,
                         suptitle_x=0.665, suptitle_y=1,
                         title_x=0.5, title_y=1.06):
    fig.update_layout(
        title={
            'text': suptitle,
            'x': suptitle_x, 'y': suptitle_y,
            'xanchor': 'right',
            'font': {'size': 18, 'color': '#0047AB', 'family': 'Arial', 'weight': 'bold'}
        },
        plot_bgcolor='rgba(255, 255, 255, 0)',
        paper_bgcolor='rgba(255, 255, 255, 0)',
    )

    fig.add_annotation(
        text=title,
        xref="paper", yref="paper",
        x=title_x, y=title_y,
        showarrow=False,
        font=dict(size=14, color='#4A4A4A', family='Arial')
    )

# Diccionario de colores de los candidatos
candidate_colors = {
    'Claudia Sheinbaum': 'darkred',
    'Xóchitl Gálvez': 'blue',
    'Jorge Álvarez Máynez': 'darkorange'
}
time_of_day_colors = {
    'Amanecer Temprano': 'dimgray',
    'Amanecer Tardío': 'lightsalmon',
    'Mañana Temprana': 'gold',
    'Mañana': 'orange',
    'Mediodía': 'lightcoral',
    'Tarde': 'indianred',
    'Tarde Noche': 'maroon',
    'Noche': 'darkblue'
}
# Función para clasificar la hora del día
def classify_time_of_day(dt):
    if 0 <= dt.hour < 3:
        return 'Amanecer Temprano'
    elif 3 <= dt.hour < 6:
        return 'Amanecer Tardío'
    elif 6 <= dt.hour < 9:
        return 'Mañana Temprana'
    elif 9 <= dt.hour < 12:
        return 'Mañana'
    elif 12 <= dt.hour < 14:
        return 'Mediodía'
    elif 14 <= dt.hour < 17:
        return 'Tarde'
    elif 17 <= dt.hour < 21:
        return 'Tarde Noche'
    else:
        return 'Noche'

time_of_day_colors = {
    'Amanecer Temprano': 'dimgray',
    'Amanecer Tardío': 'lightsalmon',
    'Mañana Temprana': 'gold',
    'Mañana': 'orange',
    'Mediodía': 'lightcoral',
    'Tarde': 'indianred',
    'Tarde Noche': 'maroon',
    'Noche': 'darkblue'
}

def get_custom_date_range():
    # Selección de rango de fechas con las fechas más antiguas y más recientes del dataset
    start_date = st.date_input("Fecha de inicio", min_value=filtered_platform_data['datetime'].min().date(), 
                               max_value=filtered_platform_data['datetime'].max().date())
    end_date = st.date_input("Fecha de fin", min_value=start_date, 
                             max_value=filtered_platform_data['datetime'].max().date())
    return start_date, end_date

# Multiselect para seleccionar el periodo de tiempo
time_option = st.multiselect(
    "Selecciona el periodo de tiempo:",
    options=["Toda la campaña", "Últimos 10 días", "Seleccionar otras fechas"]
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
    "Selecciona la plataforma:",
    list(platform_mapping.keys())
)

# Convertir la selección del usuario en nombres de columnas del DataFrame
selected_platforms = [platform_mapping[platform] for platform in db_selection if platform in platform_mapping]
filtered_platform_data = filtered_data[filtered_data['platform'].isin(selected_platforms)].copy()
# Asumiendo que 'filtered_platform_data' es tu DataFrame y tiene una columna 'datetime'
filtered_platform_data['datetime'] = pd.to_datetime(filtered_platform_data['datetime'])

# Crear una nueva columna 'week_day' que representa el día de la semana (0=Lunes, 6=Domingo)
week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

# Asegurarte de crear la columna 'week_day' en filtered_data
filtered_data['week_day'] = filtered_data['datetime'].dt.day_name()
filtered_data['time_of_day'] = filtered_data['datetime'].apply(classify_time_of_day)
# Asegurarte de crear la columna 'week_day' en filtered_platform_data
filtered_platform_data['week_day'] = filtered_platform_data['datetime'].dt.day_name()
last_10_days_df = filtered_data.loc[(filtered_data['datetime'] >= '2024-05-24') & 
                                 (filtered_data['datetime'] <= '2024-06-02')]

# Crear DataFrame para los últimos 10 días
last_10_days = filtered_platform_data.loc[(filtered_platform_data['datetime'] >= '2024-05-24') & 
                                 (filtered_platform_data['datetime'] <= '2024-06-02')]
last_10_days['week_day'] = last_10_days['datetime'].dt.day_name()
filtered_platform_data['week_day'] = filtered_platform_data['datetime'].dt.day_name()

#### Primer gráfico
fig = go.Figure()
if "Seleccionar otras fechas" in time_option:
    start_date, end_date = get_custom_date_range()
    start_date = pd.to_datetime(start_date).tz_localize('America/Mexico_City')
    end_date = pd.to_datetime(end_date).tz_localize('America/Mexico_City')

    filtered_by_date = filtered_platform_data[(filtered_platform_data['datetime'] >= start_date) & 
                                              (filtered_platform_data['datetime'] <= end_date)]
    avg_interactions_by_day = filtered_by_date.groupby('week_day')['num_interaction'].mean().reset_index()
    
    # Order the week days
    avg_interactions_by_day['week_day'] = pd.Categorical(avg_interactions_by_day['week_day'], categories=week_order, ordered=True)
    avg_interactions_by_day = avg_interactions_by_day.sort_values('week_day')

    fig.add_trace(go.Scatter(x=avg_interactions_by_day['week_day'], y=avg_interactions_by_day['num_interaction'], mode='markers+lines',
                             name='Fechas seleccionadas', line=dict(color='#4c72b0')))
    
if "Toda la campaña" in time_option:
    full_period = filtered_platform_data.groupby(['week_day'])['num_interaction'].mean().reset_index()
    
    # Order the week days
    full_period['week_day'] = pd.Categorical(full_period['week_day'], categories=week_order, ordered=True)
    full_period = full_period.sort_values('week_day')
    
    fig.add_trace(go.Scatter(x=full_period['week_day'], y=full_period['num_interaction'], mode='markers+lines',
                             name='Período completo', line=dict(color='lightsteelblue')))
    
if "Últimos 10 días" in time_option:
    last_days = last_10_days.groupby(['week_day'])['num_interaction'].mean().reset_index()
    
    # Order the week days
    last_days['week_day'] = pd.Categorical(last_days['week_day'], categories=week_order, ordered=True)
    last_days = last_days.sort_values('week_day')
    
    fig.add_trace(go.Scatter(x=last_days['week_day'], y=last_days['num_interaction'], mode='markers+lines',
                             name='Últimos 10 días', line=dict(color='#1b9e77')))

plot_template_plotly(
    fig,
    suptitle='Promedio de Interacciones',
    title='Comparación de las Interacciones Promedio a lo largo de los Días de la Semana.',
    suptitle_x=0.41, suptitle_y=0.9,
    title_x=0.04, title_y=1.1
)

st.plotly_chart(fig)



########### Segundo gráfico
fig2 = go.Figure()

if "Seleccionar otras fechas" in time_option:
    filtered_by_date['time_of_day'] = filtered_by_date['datetime'].apply(classify_time_of_day)
    filtered_by_date['time_of_day'] = pd.Categorical(filtered_by_date['time_of_day'], categories=time_of_day_colors, ordered=True)
    avg_interactions_df2 = filtered_by_date.groupby('time_of_day')['num_interaction'].mean().reset_index()
    fig2.add_trace(go.Scatter(x=avg_interactions_df2['time_of_day'], y=avg_interactions_df2['num_interaction'], mode='markers+lines',
                             name='Fechas seleccionadas', line=dict(color='#4c72b0')))

if "Toda la campaña" in time_option:
    filtered_platform_data['time_of_day'] = filtered_platform_data['datetime'].apply(classify_time_of_day)
    filtered_platform_data['time_of_day'] = pd.Categorical(filtered_platform_data['time_of_day'], categories=time_of_day_colors, ordered=True)
    avg_interactions_df2 = filtered_platform_data.groupby('time_of_day')['num_interaction'].mean().reset_index()
    fig2.add_trace(go.Scatter(x=avg_interactions_df2['time_of_day'], y=avg_interactions_df2['num_interaction'], mode='markers+lines',
                             name='Período completo', line=dict(color='lightsteelblue')))

if "Últimos 10 días" in time_option:
    last_10_days['time_of_day'] = last_10_days['datetime'].apply(classify_time_of_day)
    last_10_days['time_of_day'] = pd.Categorical(last_10_days['time_of_day'], categories=time_of_day_colors, ordered=True)
    avg_interactions_df2 = last_10_days.groupby('time_of_day')['num_interaction'].mean().reset_index()
    fig2.add_trace(go.Scatter(x=avg_interactions_df2['time_of_day'], y=avg_interactions_df2['num_interaction'], mode='markers+lines',
                             name='Últimos 10 días', line=dict(color='#1b9e77')))

plot_template_plotly(
    fig2,
    suptitle='Promedio de Interacciones',
    title='Promedio de Interacciones por Periodo del Día',
    suptitle_x=0.42, suptitle_y=0.9,
    title_x=0.053, title_y=1.1
)

st.plotly_chart(fig2)





######## Heatmaps
filtered_data['time_of_day'] = filtered_data['datetime'].apply(classify_time_of_day)
last_10_days_df['time_of_day'] = last_10_days_df['datetime'].apply(classify_time_of_day)



heatmap_data_df2 = filtered_data.pivot_table(index='week_day', columns='time_of_day', values='num_interaction', aggfunc='mean')
heatmap_data_df2 = heatmap_data_df2.reindex(week_order)  # Ordenar los días de la semana
heatmap_data_df2 = heatmap_data_df2[list(time_of_day_colors.keys())]  # Ordenar las horas del día

heatmap_data_last_10_days = last_10_days_df.pivot_table(index='week_day', columns='time_of_day', values='num_interaction', aggfunc='mean')
heatmap_data_last_10_days = heatmap_data_last_10_days.reindex(week_order)  # Ordenar los días de la semana
heatmap_data_last_10_days = heatmap_data_last_10_days[list(time_of_day_colors.keys())]  # Ordenar las horas del día

# Crear las gráficas de calor con Plotly
# Heatmap para la campaña completa
fig1 = px.imshow(heatmap_data_df2,
                 labels=dict(x="Time of Day", y="Day of the Week", color="Average Interactions"),
                 color_continuous_scale='YlGnBu',
                 title="Campaña Completa"
                )
fig1.update_layout(
    xaxis_title="Time of Day",
    yaxis_title="Day of the Week",
    xaxis_tickangle=45
)

# Heatmap para los últimos 10 días
fig2 = px.imshow(heatmap_data_last_10_days,
                 labels=dict(x="Momento del día", y="Day of the Week", color="Average Interactions"),
                 color_continuous_scale='YlGnBu',
                 title="Últimos 10 días"
                )
fig2.update_layout(
    xaxis_title="Time of Day",
    yaxis_title="",
    xaxis_tickangle=45
)

# Mostrar las gráficas en Streamlit
st.title("Interacciones promedio dependiendo el horario y el día de publicación")

# Mostrar las dos gráficas de calor en Streamlit en secciones separadas
st.plotly_chart(fig1)
st.plotly_chart(fig2)

