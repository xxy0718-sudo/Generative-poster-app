import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

st.set_page_config(page_title="Generative Poster", layout="centered")

st.title("🎨 Generative Poster - Wave Blobs")
st.write("This version generates the **'more blobs'** style poster (the one with many overlapping circles).")

# ========== Parameters ==========
n_layers = st.slider("Number of layers (shapes)", 15, 40, 25)
max_radius = st.slider("Max blob radius", 0.1, 0.5, 0.3)
seed = st.number_input("Random seed", value=42)
random.seed(seed)
np.random.seed(seed)

# ========== Color palette generator ==========
def random_palette(n=5):
    return [
        (
            random.random() * 0.6 + 0.2,
            random.random() * 0.6 + 0.2,
            random.random() * 0.6 + 0.2,
        )
        for _ in range(n)
    ]

palette = random_palette(5)

# ========== Generate one wavy blob ==========
def blob(center_x, center_y, radius, waviness=0.1, points=100):
    theta = np.linspace(0, 2 * np.pi, points)
    r = radius * (1 + np.random.uniform(-waviness, waviness, size=points))
    x = center_x + r * np.cos(theta)
    y = center_y + r * np.sin(theta)
    return x, y

# ========== Plot the poster ==========
fig, ax = plt.subplots(figsize=(6, 9))  # vertical poster
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

for i in range(n_layers):
    color = random.choice(palette)
    cx, cy = np.random.rand(2)
    r = np.random.uniform(0.1, max_radius)
    x, y = blob(cx, cy, r, waviness=0.15)
    ax.fill(x, y, color=color, alpha=0.4)

plt.text(
    0.05,
    0.95,
    "Generative Poster\nWeek 2 Arts & Advanced Big Data",
    fontsize=12,
    fontweight="bold",
    va="top",
)

st.pyplot(fig)

