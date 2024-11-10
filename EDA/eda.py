# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.header("Exploratory Data Analysis")


# Step 1: Load the dataset
df = pd.read_csv("Merged_data")


def summary(filtered_data):

    # Summary statistics
    st.write("### Summary Statistics")
    st.write(filtered_data.describe())

    # Species distribution
    st.write("### Species Distribution")
    st.bar_chart(filtered_data['species'].value_counts())

def load_data():
    return sns.load_dataset("penguins").dropna()

df = load_data()



# Species selection
species = st.multiselect(
    "Select Species",
    options=df['species'].unique(),
    default=df['species'].unique()
)

# Filter data based on user selection
filtered_data = df[df['species'].isin(species)]
summary(filtered_data)


