import streamlit as st
from PIL import Image



# Read the CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply the CSS
local_css("css/main.css")

# Display formatted text below the image
st.markdown(
    """
        <!DOCTYPE html><html><head><link href="https://fonts.googleapis.com/css?family=Julius+Sans+One&display=swap" rel="stylesheet" /><link href="https://fonts.googleapis.com/css?family=Khula&display=swap" rel="stylesheet" /><link href="./css/main.css" rel="stylesheet" /><title>Document</title></head><body><div class="v1_2"><div class="v3_7"></div><span class="v1_4">Copyright</span><span class="v1_5">description</span><span class="v1_6">Copyright is a type of intellectual property that protects original works of authorship as soon as an author fixes the work in a tangible form of expression. In copyright law, there are a lot of different types of works, including paintings, photographs, illustrations, musical compositions, sound recordings, computer programs, books, poems, blog posts, movies, architectural works, plays, and so much more!</span></div></body></html>
    """, unsafe_allow_html=True
)
