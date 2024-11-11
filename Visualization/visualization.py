import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from eda import filtered_data

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

# Identificar los días de la semana
filtered_data['week_day'] = pd.to_datetime(filtered_data['datetime']).dt.day_name()
week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Multiselect para seleccionar el periodo de tiempo
time_period_selection = st.multiselect(
    "Select the time period:",
    ["Entire campaign", "Last 10 days"]
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

# Crear DataFrame para los últimos 10 días
last_10_days = filtered_platform_data.loc[(filtered_platform_data['datetime'] >= '2024-05-24') & 
                                          (filtered_platform_data['datetime'] <= '2024-06-02')]

# Crear la figura para el gráfico
fig, ax = plt.subplots(figsize=(10, 6))

# Graficar según la selección del usuario
if "Entire campaign" in time_period_selection:
    full_period = filtered_platform_data.groupby(['week_day'])['num_interaction'].mean().reset_index()
    full_period['week_day'] = pd.Categorical(full_period['week_day'], categories=week_order, ordered=True)
    sns.lineplot(x='week_day', y='num_interaction', data=full_period, marker='o',
                 label='Full Period', color='cadetblue', ax=ax)

if "Last 10 days" in time_period_selection:
    last_days = last_10_days.groupby(['week_day'])['num_interaction'].mean().reset_index()
    last_days['week_day'] = pd.Categorical(last_days['week_day'], categories=week_order, ordered=True)
    sns.lineplot(x='week_day', y='num_interaction', data=last_days, marker='o',
                 label='Last 10 Days', color='plum', ax=ax)

# Personalizar el gráfico
ax.set_xlabel('Day of the Week')
ax.set_ylabel('Average Interaction')
ax.tick_params(axis='x', rotation=45)
ax.legend(title='Period')

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

# Agregar el footer
st.write("### About this App")
st.write("This app allows for the visualization of data gathered from social media involving presidential candidates in the 2024 electoral campaign.")
