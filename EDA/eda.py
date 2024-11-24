# Importación de librerías
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import pickle
from plotly.subplots import make_subplots
import plotly.express as px
from Background.facts import filtered_data  # Asegúrate de que esta importación sea válida

# Configuración inicial de la aplicación
st.title("Interacciones de acuerdo al momento de interacción")

# Función para aplicar plantilla a gráficos Plotly
def plot_template_plotly(fig, suptitle, title, suptitle_x=0.665, suptitle_y=1, title_x=0.5, title_y=1.06):
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

# Configuración de colores
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

# Función para obtener un rango de fechas personalizado
def get_custom_date_range(dataframe):
    start_date = st.date_input(
        "Fecha de inicio",
        min_value=dataframe['datetime'].min().date(),
        max_value=dataframe['datetime'].max().date()
    )
    end_date = st.date_input(
        "Fecha de fin",
        min_value=start_date,
        max_value=dataframe['datetime'].max().date()
    )
    return start_date, end_date

# Mapeo de plataformas
platform_mapping = {
    "Facebook": "facebook",
    "Twitter": "twitter",
    "Instagram": "instagram",
    "YouTube": "youtube"
}

# Traducción de días de la semana
english_to_spanish_days = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}
week_order_spanish = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Filtros interactivos
time_option = st.multiselect(
    "Selecciona el periodo de tiempo:",
    options=["Toda la campaña", "Últimos 10 días", "Seleccionar otras fechas"]
)
db_selection = st.multiselect(
    "Selecciona la plataforma:",
    list(platform_mapping.keys())
)
selected_platforms = [platform_mapping[platform] for platform in db_selection]
filtered_platform_data = filtered_data[filtered_data['platform'].isin(selected_platforms)].copy()
filtered_platform_data['datetime'] = pd.to_datetime(filtered_platform_data['datetime'])

# Clasificar horas y días en los datos
filtered_platform_data['time_of_day'] = filtered_platform_data['datetime'].apply(classify_time_of_day)
filtered_platform_data['week_day'] = filtered_platform_data['datetime'].dt.day_name().replace(english_to_spanish_days)

# Función para crear gráficos
def create_line_chart(data, group_column, value_column, name, color):
    grouped_data = data.groupby(group_column)[value_column].mean().reset_index()
    grouped_data[group_column] = pd.Categorical(grouped_data[group_column], categories=week_order_spanish, ordered=True)
    grouped_data = grouped_data.sort_values(group_column)
    return go.Scatter(
        x=grouped_data[group_column],
        y=grouped_data[value_column],
        mode='markers+lines',
        name=name,
        line=dict(color=color)
    )

# Crear y mostrar el primer gráfico
fig = go.Figure()

if "Seleccionar otras fechas" in time_option:
    start_date, end_date = get_custom_date_range()
    start_date = pd.to_datetime(start_date).tz_localize('America/Mexico_City')
    end_date = pd.to_datetime(end_date).tz_localize('America/Mexico_City')

    filtered_by_date = filtered_platform_data[
        (filtered_platform_data['datetime'] >= start_date) & 
        (filtered_platform_data['datetime'] <= end_date)
    ]
    
    avg_interactions_by_day = filtered_by_date.groupby('week_day')['num_interaction'].mean().reset_index()
    
    # Traducir días al español
    avg_interactions_by_day['week_day'] = avg_interactions_by_day['week_day'].replace(english_to_spanish_days)
    
    # Ordenar los días de la semana en español
    week_order_spanish = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    avg_interactions_by_day['week_day'] = pd.Categorical(avg_interactions_by_day['week_day'], categories=week_order_spanish, ordered=True)
    avg_interactions_by_day = avg_interactions_by_day.sort_values('week_day')

    fig.add_trace(go.Scatter(
        x=avg_interactions_by_day['week_day'], 
        y=avg_interactions_by_day['num_interaction'], 
        mode='markers+lines',
        name='Fechas seleccionadas', 
        line=dict(color='#4c72b0')
    ))

if "Toda la campaña" in time_option:
    full_period = filtered_platform_data.groupby(['week_day'])['num_interaction'].mean().reset_index()
    
    # Traducir días al español
    full_period['week_day'] = full_period['week_day'].replace(english_to_spanish_days)
    
    # Ordenar los días de la semana en español
    full_period['week_day'] = pd.Categorical(full_period['week_day'], categories=week_order_spanish, ordered=True)
    full_period = full_period.sort_values('week_day')
    
    fig.add_trace(go.Scatter(
        x=full_period['week_day'], 
        y=full_period['num_interaction'], 
        mode='markers+lines',
        name='Período completo', 
        line=dict(color='lightsteelblue')
    ))

if "Últimos 10 días" in time_option:
    last_10_days = filtered_platform_data[
        filtered_platform_data['datetime'] >= (filtered_platform_data['datetime'].max() - pd.Timedelta(days=10))
    ]
    last_days = last_10_days.groupby(['week_day'])['num_interaction'].mean().reset_index()
    
    # Traducir días al español
    last_days['week_day'] = last_days['week_day'].replace(english_to_spanish_days)
    
    # Ordenar los días de la semana en español
    last_days['week_day'] = pd.Categorical(last_days['week_day'], categories=week_order_spanish, ordered=True)
    last_days = last_days.sort_values('week_day')
    
    fig.add_trace(go.Scatter(
        x=last_days['week_day'], 
        y=last_days['num_interaction'], 
        mode='markers+lines',
        name='Últimos 10 días', 
        line=dict(color='#1b9e77')
    ))

# Aplicar plantilla y formato
plot_template_plotly(
    fig,
    suptitle='Promedio de Interacciones Según Día',
    title='Comparación de las Interacciones Promedio a lo largo de los Días de la Semana.',
    suptitle_x=0.385, suptitle_y=0.9,
    title_x=0.008, title_y=1.1
)

fig.update_layout(
    yaxis=dict(
        title='Interacciones',  # Etiqueta del eje vertical
        title_font=dict(size=15, color='black'),  # Título más grande y oscuro
        tickfont=dict(size=14, color='black')  # Etiquetas del eje vertical en negro
    ),
    xaxis=dict(
        tickfont=dict(size=14, color='black')  # Etiquetas del eje horizontal en negro
    )
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
    suptitle='Promedio de Interacciones Según Momento del Día',
    title='Promedio de Interacciones por Periodo del Día',
    suptitle_x=0.5, suptitle_y=0.9,
    title_x=0.012, title_y=1.1
)

fig2.update_layout(
    yaxis=dict(
        title='Interacciones',  # Etiqueta del eje vertical
        title_font=dict(size=15, color='black'),
        tickfont=dict(size=14, color='black')  # Nombres de los periodos más grandes y oscuros
    ),
    xaxis=dict(
        tickfont=dict(size=14, color='black')  # Etiquetas del eje horizontal en negro
    )
)

st.plotly_chart(fig2)
st.markdown("<br>", unsafe_allow_html=True)  # Salto de línea


##
# Datos filtrados
filtered_platform_data = filtered_data.copy()  # Asegúrate de usar los datos correctos
filtered_platform_data['week_day'] = filtered_platform_data['datetime'].dt.day_name().map(english_to_spanish_days)

# Últimos 10 días de la campaña
last_10_days = filtered_platform_data[filtered_platform_data['datetime'] >= filtered_platform_data['datetime'].max() - pd.Timedelta(days=10)]

# Título de la sección
st.write("### Interacciones Promedio por Candidato por Día de la Semana")

# Preparar los datos agrupados y ordenados
full_period = filtered_platform_data.groupby(['week_day', 'candidate_name'])['num_interaction'].mean().reset_index()
full_period['week_day'] = pd.Categorical(full_period['week_day'], categories=week_order_spanish, ordered=True)

last_days = last_10_days.groupby(['week_day', 'candidate_name'])['num_interaction'].mean().reset_index()
last_days['week_day'] = pd.Categorical(last_days['week_day'], categories=week_order_spanish, ordered=True)

# Pivot tables para las gráficas
full_period_pivot = full_period.pivot(index='week_day', columns='candidate_name', values='num_interaction').fillna(0)
last_days_pivot = last_days.pivot(index='week_day', columns='candidate_name', values='num_interaction').fillna(0)

# Crear subplot
fig = make_subplots(
    rows=1, cols=2,  # 1 fila, 2 columnas
    shared_yaxes=True,
    subplot_titles=("Campaña Completa", "10 Días Previos a la Elección"),
)

# Gráfica para todo el periodo
for candidate in full_period_pivot.columns:
    fig.add_trace(go.Bar(
        x=full_period_pivot.index,
        y=full_period_pivot[candidate],
        name=f"Campaña Completa - {candidate}",
        hoverinfo='y+name',
        marker=dict(color=candidate_colors.get(candidate, '#1f77b4')),  # Color asignado al candidato
    ), row=1, col=1)

# Gráfica para los últimos 10 días
for candidate in last_days_pivot.columns:
    fig.add_trace(go.Bar(
        x=last_days_pivot.index,
        y=last_days_pivot[candidate],
        name=f"10 Últimos Días - {candidate}",
        hoverinfo='y+name',
        marker=dict(color=candidate_colors.get(candidate, '#ff7f0e')),  # Color asignado al candidato
    ), row=1, col=2)

# Ajustes de diseño
fig.update_layout(
    barmode='stack',
    yaxis_title="Interacciones Promedio",
    plot_bgcolor="white",
    showlegend=True,
    legend_title="Candidatos",
    legend=dict(
        x=1, y=1,
        traceorder="normal",
        orientation="v",
        xanchor="left"
    )
)
# Mostrar la gráfica
st.plotly_chart(fig, use_container_width=True)

### Heatmaps
# Puedes crear un diccionario similar para los momentos del día si es necesario, por ejemplo:
time_of_day_translation = {
    'Early Dawn': 'Amanecer temprano',
    'Late Dawn': 'Amanecer tardío',
    'Early Morning': 'Mañana temprana',
    'Morning': 'Mañana',
    'Noon': 'Mediodía',
    'Afternoon': 'Tarde',
    'Early Evening': 'Tarde Noche',
    'Night': 'Noche'
}

# Cargar los datos de los heatmaps
with open('EDA/heatmap_data_full_campaign.pkl', 'rb') as f:
    heatmap_data_df2 = pickle.load(f)

with open('EDA/heatmap_data_last_10_days.pkl', 'rb') as f:
    heatmap_data_last_10_days = pickle.load(f)

# Asumir que las filas contienen los días de la semana y las columnas los momentos del día
heatmap_data_df2.index = heatmap_data_df2.index.map(english_to_spanish_days)
heatmap_data_last_10_days.index = heatmap_data_last_10_days.index.map(english_to_spanish_days)

# Si las columnas son los momentos del día, puedes hacer lo mismo para ellas:
heatmap_data_df2.columns = heatmap_data_df2.columns.map(time_of_day_translation)
heatmap_data_last_10_days.columns = heatmap_data_last_10_days.columns.map(time_of_day_translation)

# Crear la figura con subgráficos (subplots)
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Campaña Completa", "Últimos 10 Días"),
    shared_yaxes=True,  # Para compartir el eje y
    vertical_spacing=0.1  # Espacio entre los subgráficos
)

# Añadir el primer heatmap a la primera columna (con colorbar)
fig.add_trace(
    go.Heatmap(
        z=heatmap_data_df2.values,
        x=heatmap_data_df2.columns,
        y=heatmap_data_df2.index,
        colorscale='YlGnBu',
        colorbar=dict(x=1.05)  # Definir colorbar solo aquí
    ),
    row=1, col=1
)

# Añadir el segundo heatmap a la segunda columna (sin colorbar)
fig.add_trace(
    go.Heatmap(
        z=heatmap_data_last_10_days.values,
        x=heatmap_data_last_10_days.columns,
        y=heatmap_data_last_10_days.index,
        colorscale='YlGnBu',
        showscale=False  # Desactivar el colorbar en este heatmap
    ),
    row=1, col=2
)

# Actualizar la configuración de los ejes y diseño
fig.update_layout(
    height=500,  # Ajustar la altura total del gráfico
    width=1400  # Ajustar el ancho total del gráfico
)
# Título y descripción
st.write("Los momentos con mayor cantidad de interacciones fueron:")

# Mostrar las gráficas en columnas
col1, col2 = st.columns(2)
with col1:
    st.markdown(""" 
        <div style="background-color: #00274D; padding: 25px; border-radius: 10px; border: 3px solid #001F3F; width: 90%; margin: auto;">
            <h2 style="color: #FFFFFF; text-align: center; font-size: 20px;">Domingo en la noche</h2>
            <p style="color: #D3D3D3; font-size: 14px; text-align: center;">Campaña Completa.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(""" 
        <div style="background-color: #00274D; padding: 25px; border-radius: 10px; border: 3px solid #001F3F; width: 90%; margin: auto;">
            <h2 style="color: #FFFFFF; text-align: center; font-size: 20px;">Miércoles en la campaña</h2>
            <p style="color: #D3D3D3; font-size: 14px; text-align: center;">Últimos 10 Días.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)  # Salto de línea
st.markdown(
    """
    ### 📅 Miércoles 29 de mayo de 2024. Cierre de campaña. 
    """, 
    unsafe_allow_html=True,
)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)
