import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

st.set_page_config(page_title="3D-Like Generative Poster", layout="centered")
st.title("🎨 3D-Like Generative Poster")
st.write("Portrait-oriented layered blobs with depth cues, shadows, and warm/cool colors.")

# -----------------------------
# Functions
# -----------------------------
def generate_blob(ax, x, y, r, wobble=0.1, color=(0.5,0.5,0.5), shadow=False):
    """Draw a wobbly blob with optional shadow."""
    points = 100
    angles = np.linspace(0, 2*np.pi, points)
    radii = r + np.random.uniform(-wobble*r, wobble*r, size=points)
    x_points = x + radii * np.cos(angles)
    y_points = y + radii * np.sin(angles)

    if shadow:
        shadow_offset = r * 0.1
        ax.fill(x_points + shadow_offset, y_points - shadow_offset, color=(0,0,0,0.3), zorder=0)

    ax.fill(x_points, y_points, color=color, alpha=0.8, zorder=1)

def random_palette(n_colors=5, warm=True):
    """Generate a list of warm or cool colors for depth."""
    colors = []
    for _ in range(n_colors):
        if warm:
            colors.append((random.uniform(0.7,1), random.uniform(0.3,0.7), random.uniform(0,0.3)))
        else:
            colors.append((random.uniform(0,0.3), random.uniform(0.3,0.7), random.uniform(0.7,1)))
    return colors

# -----------------------------
# Streamlit controls
# -----------------------------
seed = st.number_input("Random Seed", min_value=0, value=42)
n_layers = st.slider("Number of Layers", 5, 20, 12)
max_radius = st.slider("Max Radius", 50, 200, 120)
portrait_width = st.slider("Canvas Width", 6, 10, 6)
portrait_height = st.slider("Canvas Height", 8, 15, 9)

if st.button("Generate Poster 🎨"):
    random.seed(seed)
    np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(portrait_width, portrait_height))
    ax.set_xlim(-200, 200)
    ax.set_ylim(-300, 450)
    ax.axis('off')
    ax.set_facecolor('white')

    for i in range(n_layers):
        r = max_radius - i*7
        x = random.randint(-150, 150)
        y = random.randint(-250, 400)
        color = random.choice(random_palette(warm=(i < n_layers//2)))
        shadow = i > n_layers // 3
        generate_blob(ax, x, y, r, wobble=0.15, color=color, shadow=shadow)

    ax.text(-180, 400, "3D-Like Generative Poster", fontsize=14, fontweight='bold', color='black')

    st.pyplot(fig)
