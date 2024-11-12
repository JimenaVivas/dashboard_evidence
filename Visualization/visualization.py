import streamlit as st 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pytz
from EDA.eda import filtered_data, plot_template

st.header("Graphs of the hypothesis")

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
st.write("###  User behaviour according to day and time of the day ")
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

if filtered_platform_data.empty:
    st.warning("No data available for the selected platforms.")
    st.stop()

filtered_platform_data['datetime'] = pd.to_datetime(filtered_platform_data['datetime'])

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

# Crear la figura para el gráfico
fig, ax = plt.subplots(figsize=(10, 6))
fig2, ax2 = plt.subplots(figsize=(10, 6))

# Manejo del multiselect si se elige la opción "Select other dates"
if "Select other dates" in time_option:
    start_date, end_date = get_custom_date_range()

    # Convertir start_date y end_date a datetime con la zona horaria correcta
    start_date = pd.to_datetime(start_date).tz_localize('America/Mexico_City')
    end_date = pd.to_datetime(end_date).tz_localize('America/Mexico_City')

    # Filtrar los datos según el rango de fechas seleccionado
    filtered_by_date = filtered_platform_data[(filtered_platform_data['datetime'] >= start_date) & 
                                              (filtered_platform_data['datetime'] <= end_date)]
    sns.lineplot(x='week_day', y='num_interaction', data=filtered_by_date, marker='o',
                 label='Selected dates', color='lightcoral', ax=ax)
    filtered_by_date['time_of_day'] = filtered_by_date['datetime'].apply(classify_time_of_day)

else:
    filtered_by_date = filtered_platform_data

# Verificar si el DataFrame tiene datos después del filtro de fechas
if filtered_by_date.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

#  Graficar según la selección del usuario
if "Entire campaign" in time_option:
    full_period = filtered_by_date.groupby(['week_day'])['num_interaction'].mean().reset_index()
    full_period['week_day'] = pd.Categorical(full_period['week_day'], categories=week_order, ordered=True)
    sns.lineplot(x='week_day', y='num_interaction', data=full_period, marker='o',
                 label='Full Period', color='cadetblue', ax=ax)  # Plot on ax
    filtered_by_date['time_of_day'] = filtered_by_date['datetime'].apply(classify_time_of_day)
    filtered_by_date['time_of_day'] = pd.Categorical(filtered_by_date['time_of_day'], categories=time_of_day_colors, ordered=True)
    avg_interactions_df2 = filtered_by_date.groupby('time_of_day')['num_interaction'].mean().reset_index()
    sns.lineplot(x='time_of_day', y='num_interaction', data=avg_interactions_df2, marker='o', 
                 label='Full Period', color='cadetblue', ax=ax2)  # Plot on ax2

if "Last 10 days" in time_option:
    last_days = last_10_days.groupby(['week_day'])['num_interaction'].mean().reset_index()
    last_days['week_day'] = pd.Categorical(last_days['week_day'], categories=week_order, ordered=True)
    sns.lineplot(x='week_day', y='num_interaction', data=last_days, marker='o',
                 label='Last 10 Days', color='plum', ax=ax)  # Plot on ax
    last_10_days['time_of_day'] = last_10_days['datetime'].apply(classify_time_of_day)
    last_10_days['time_of_day'] = pd.Categorical(last_10_days['time_of_day'], categories=time_of_day_colors, ordered=True)
    avg_interactions_df2 = last_10_days.groupby('time_of_day')['num_interaction'].mean().reset_index()
    sns.lineplot(x='time_of_day', y='num_interaction', data=avg_interactions_df2, marker='o', 
                 label='Last 10 Days', color='plum', ax=ax2)  # Plot on ax2
    

# Personalizar el gráfico para el primer plot
plot_template(
    suptitle='Average Interaction',
    title='Comparison of Average Interactions over Days of the Week',  # This title will appear only on the first plot
    suptitle_dict={'x': 0.05, 'y': 0.97},
    title_dict={'x': 0.127, 'y': 1.095},
)

ax.set_xlabel('Day of the Week')
ax.set_ylabel('Average Interaction')
ax.tick_params(axis='x', rotation=45)
ax.legend(title='Period')

# Personalizar el gráfico para el segundo plot
plot_template(
    suptitle='Average Interactions by Time of Day',
    title='Comparison of Average Interactions over Time of Day',  # Title for the second plot
    suptitle_dict={'x': 0.285, 'y': 0.97},
    title_dict={'x': 0.257, 'y': 1.095},
)

ax2.set_xlabel('Time of Day')
ax2.set_ylabel('Average Number of Interactions')
ax2.tick_params(axis='x', rotation=45)
ax2.legend(title='Period')

# Mostrar el gráfico en Streamlit
st.pyplot(fig)
st.pyplot(fig2)

# Agregar el footer
st.write("### About this App")
st.write("This app allows for the visualization of data gathered from social media involving presidential candidates in the 2024 electoral campaign.")