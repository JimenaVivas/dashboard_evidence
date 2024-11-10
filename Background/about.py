import streamlit as st
from PIL import Image

# Title and description
st.markdown(
    """
    <div style='text-align: center; padding: 2em; background-color: #f8f9fa;'>
        <h2 style='font-size: 2em; color: #4a4a4a;'>About Us</h2>
        <p style='font-size: 1.2em; color: #6c757d; line-height: 1.5;'>
            We are a team of dedicated professionals passionate about creating innovative solutions that help people.
            Our goal is to make the world a better place through technology.
        </p>
    </div>
    """, unsafe_allow_html=True
)

# Define images and team member details
team_members = [
    {"name": "Jane Smith", "role": "Project Manager", "image": "images/rosa.jpeg"},
    {"name": "John Doe", "role": "Lead Developer", "image": "images/blue.webp"},
    {"name": "Emma Brown", "role": "UI/UX Designer", "image": "images/gray.jpg"},
]

# Create columns for each team member
cols = st.columns(len(team_members))
for col, member in zip(cols, team_members):
    with col:
        # Display each member's image
        image = Image.open(member["image"])
        st.image(image, use_column_width=True, caption=member["name"])
        # Display member name and role
        st.markdown(
            f"<h3 style='text-align: center; color: #4a4a4a;'>{member['name']}</h3>", unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='text-align: center; color: #6c757d;'>{member['role']}</p>", unsafe_allow_html=True
        )
