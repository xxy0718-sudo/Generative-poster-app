import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# Page setup
st.set_page_config(page_title="Interactive Poster • csv", layout="centered")
st.title("🎨 Interactive Poster • csv")

# -----------------------------
# Helper functions
# -----------------------------
def spiky_shape(center, radius, spikes=30, irregularity=0.5):
    """Generate a spiky, irregular polygon shape."""
    angles = np.linspace(0, 2*np.pi, spikes)
    radii = radius * (1 + np.random.uniform(-irregularity, irregularity, spikes))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# -----------------------------
# Streamlit sidebar controls
# -----------------------------
st.sidebar.header("🎛 Control Panel")

seed = st.sidebar.number_input("Random Seed", min_value=0, value=42)
n_shapes = st.sidebar.slider("Number of Shapes", 5, 50, 20)
min_radius = st.sidebar.slider("Minimum Radius", 20, 100, 40)
max_radius = st.sidebar.slider("Maximum Radius", 100, 300, 150)
alpha_value = st.sidebar.slider("Transparency", 0.1, 1.0, 0.3)
irregularity = st.sidebar.slider("Spikiness", 0.1, 1.0, 0.6)
bg_color = st.sidebar.color_picker("Background Color", "#FFFFFF")

if st.button("Generate Poster 🎨"):
    random.seed(seed)
    np.random.seed(seed)

    # Create figure (portrait orientation)
    fig, ax = plt.subplots(figsize=(5, 7))
    ax.set_xlim(-300, 300)
    ax.set_ylim(-400, 400)
    ax.axis("off")
    ax.set_facecolor(bg_color)

    # Draw multiple spiky shapes
    for _ in range(n_shapes):
        center = (random.uniform(-100, 100), random.uniform(-100, 200))
        radius = random.uniform(min_radius, max_radius)
        x, y = spiky_shape(center, radius, spikes=random.randint(20, 40), irregularity=irregularity)
        color = (random.random(), random.random(), random.random())
        ax.fill(x, y, color=color, alpha=alpha_value)

    # Add title
    ax.text(0, 350, "Interactive Poster • csv", fontsize=14, fontweight="bold",
            ha="center", color="black")

    st.pyplot(fig)
