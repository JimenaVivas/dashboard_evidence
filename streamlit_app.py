import streamlit as st


intro = st.Page(
    "Background/intro.py",
    title="Introduction",
    icon=":material/help:",
    
)

facts = st.Page(
    "Background/facts.py",
    title="Facts",
    icon=":material/help:",
    
)

visualization = st.Page(
    "Visualization/visualization.py",
    title="Interactive charts",
    icon=":material/help:",
)


ml = st.Page(
    "ml/ml_analysis.py",
    title="Sentiment analysis",
    icon=":material/healing:",
)
eda = st.Page(
    "EDA/eda.py",
    title="Statistics",
    icon=":material/person_add:",
)

about = st.Page(
    "Background/about.py",
    title="About Us",
    icon=":material/person_add:",
)

cr  = st.Page(         
    "Background/example.py",
    title="Copyright",
    icon=":material/person_add:",
)
intro_pages = [intro, facts]
visualization_pages = [visualization]
ml_pages = [ml]
eda_pages = [eda]
about_pages = [about, cr]

#st.title("Data Analytics ")
st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}

page_dict["Introduction"] =  intro_pages
page_dict["Data Analysis"] = eda_pages
page_dict["Visualization"] = visualization_pages
page_dict["Prediction"] = ml_pages
page_dict["About us"] = about_pages




pg = st.navigation(page_dict)
pg.run()