# Import necessary libraries 
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.header("Exploratory Data Analysis")

# Plot template functions
def plot_template(suptitle=None, title=None, suptitle_dict={}, title_dict={}, logo=None, logo_size=(100, 100)):
    if suptitle:
        plt.suptitle(suptitle, fontsize=14, fontweight='bold', color='darkblue', **suptitle_dict if suptitle_dict else {})
    if title:
        plt.title(title, fontsize=12, **title_dict if title_dict else {})

    if logo:
        logo_img = logo
        if logo_img.mode != 'RGBA':
            logo_img = logo_img.convert('RGBA')

        logo_img = logo_img.resize(logo_size, Image.LANCZOS)
        fig = plt.gcf()
        fig_width, fig_height = fig.get_size_inches()
        dpi = fig.dpi
        x_pos = 90
        y_pos = fig_height * dpi - logo_size[1] - 2.3
        plt.figimage(logo_img, x_pos, y_pos, alpha=1.0, origin='upper', zorder=1)
    plt.tight_layout()

def plot_template_plotly(fig, suptitle="This is the superior title",
                         title="This is a general description of plot",
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

# Step 1: Load the dataset
df = pd.read_csv(r"C:/Users/jvh26/Downloads/cosofinal/dashboard_evidence/EDA/output.csv")
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Seleccionar candidatos
candidates = st.multiselect(
    "Select Candidate Name",
    options=df['candidate_name'].unique(),
    default=df['candidate_name'].unique()
)
filtered_data = df[df['candidate_name'].isin(candidates)]

# Mostrar resumen estadístico
def summary(filtered_data):

    # Se modifican los nombres para que sean más claros al visualizar en la app
    filtered_data.rename(columns={ 
    'comment_count': 'Comments',
    'view_count': 'Views',
    'like_count': 'Likes',
    'num_interaction': 'Total interactions'
    }, inplace=True)

    filtered_data['num_interaction'] = filtered_data['Total interactions'].copy()

    # Seleccionar solo el promedio y el conteo de cada columna numérica
    summary_stats = filtered_data.describe().loc[['mean', 'count']]
    summary_stats.rename(index={'mean': 'Mean', 'count': 'Count'}, inplace=True)


    # Mostrar estadísticos seleccionados
    st.write("### Summary Statistics")
    st.write(summary_stats)

    # Distribución de candidatos
    st.write("### Candidate Distribution")
    # Distribución de candidatos con colores personalizados
    candidate_counts = filtered_data['candidate_name'].value_counts()
    
    # Crear gráfico de barras con colores personalizados
    fig_bar = go.Figure(
        data=[go.Bar(
            x=candidate_counts.index,
            y=candidate_counts.values,
            marker_color=[candidate_colors[candidate] for candidate in candidate_counts.index]
        )]
    )
    fig_bar.update_layout(
        xaxis_title="Candidate Name",
        yaxis_title="Count"
    )
    plot_template_plotly(
    fig_bar,
    suptitle='Distribution of Candidates',
    title='Distribution of candidates throughout the entire campaign.',
    suptitle_x=0.45, suptitle_y=.9,
    title_x=0.04, title_y=1.1
    )
    st.plotly_chart(fig_bar)

summary(filtered_data)

# Crear la figura interactiva con Plotly
fig = go.Figure()
st.write('### Distribution by platform')
# Crear interacciones por fecha y plataforma en datos filtrados
interactions_by_date = filtered_data.groupby([filtered_data['datetime'].dt.date, 'platform'])['text'].count().reset_index()

# Colores de las plataformas
platform_colors = {
    'youtube': 'red',
    'instagram': 'purple',
    'facebook': 'blue',
    'twitter': 'lightblue'
}

for platform in ['youtube', 'instagram', 'facebook', 'twitter']:
    platform_data = interactions_by_date[interactions_by_date['platform'] == platform]
    fig.add_trace(go.Scatter(
        x=platform_data['datetime'],
        y=platform_data['text'],
        mode='lines+markers',
        name=platform,
        line=dict(color=platform_colors.get(platform))
    ))

# Configurar la plantilla personalizada de Plotly
plot_template_plotly(
    fig,
    suptitle='Daily Activity on Each Platform',
    title='Number of posts per day for each platform',
    suptitle_x=0.5, suptitle_y=.9,
    title_x=0.09, title_y=1.1    
)
# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

# Crear función para mostrar estadísticas y gráfico en base a datos filtrados
def summary_statistics_and_plot(filtered_data):
    platform_counts = filtered_data['platform'].value_counts()

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plot_template(
        suptitle='Number of posts per platform',
        title='Distribution of posts across different social media platforms.',
        suptitle_dict={'x': 0.3, 'y': 0.95},
        title_dict={'x': 0.37, 'y': 1.07},
    )
    sns.barplot(x=platform_counts.index, y=platform_counts.values, palette=platform_colors)
    plt.xlabel('Platform')
    plt.ylabel('Number of Posts')
    
    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

# Llamada a la función para mostrar estadísticas y gráfico usando los datos filtrados
summary_statistics_and_plot(filtered_data)
