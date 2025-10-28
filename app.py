import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# ---------------------------
# Generate random palette
# ---------------------------
def random_palette(n_colors, palette_type="pastel"):
    colors = []
    for _ in range(n_colors):
        if palette_type == "pastel":
            color = (random.uniform(0.6,1.0), random.uniform(0.6,1.0), random.uniform(0.6,1.0))
        elif palette_type == "vivid":
            color = (random.random(), random.random(), random.random())
        elif palette_type == "muted":
            color = (random.uniform(0.2,0.6), random.uniform(0.2,0.6), random.uniform(0.2,0.6))
        else:
            color = (random.random(), random.random(), random.random())
        colors.append(color)
    return colors

# ---------------------------
# Generate wobbly circular blob
# ---------------------------
def blob(center, size, wobble_factor=0.2, n_points=100):
    angles = np.linspace(0, 2*np.pi, n_points)
    radius = size + np.random.normal(0, size * wobble_factor, n_points)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return x, y

# ---------------------------
# Generate poster (returns fig)
# ---------------------------
def generate_poster(style="Pastel", seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis('off')

    if style.lower() == "minimal":
        n_layers, wobble_factor, min_size, max_size, palette_type = 4, 0.05, 0.07, 0.15, "muted"
    elif style.lower() == "vivid":
        n_layers, wobble_factor, min_size, max_size, palette_type = 15, 0.2, 0.05, 0.25, "vivid"
    elif style.lower() == "noisetouch":
        n_layers, wobble_factor, min_size, max_size, palette_type = 12, 0.4, 0.04, 0.2, "pastel"
    else:
        n_layers, wobble_factor, min_size, max_size, palette_type = 8, 0.2, 0.05, 0.2, "pastel"

    colors = random_palette(5, palette_type)

    for _ in range(n_layers):
        center_x, center_y = random.uniform(0, 1), random.uniform(0, 1)
        size = random.uniform(min_size, max_size)
        x, y = blob((center_x, center_y), size, wobble_factor)
        ax.fill(x, y, color=random.choice(colors), alpha=0.6)

    ax.text(0.02, 0.95, "Generative Poster\nWeek 2 Arts & Advanced Big Data",
            fontsize=12, fontweight='bold', color='black', transform=ax.transAxes,
            verticalalignment='top', horizontalalignment='left')

    return fig

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🎨 Generative Poster Generator")
st.write("랜덤한 색과 블롭 형태를 이용해 생성형 포스터를 만들어 보세요!")

style = st.selectbox("🎨 Style 선택", ["Minimal", "Vivid", "Noisetouch", "Pastel"])
seed = st.number_input("Seed (재현용)", min_value=0, value=42)

if st.button("포스터 생성하기 🎨"):
    fig = generate_poster(style=style, seed=seed)
    st.pyplot(fig)
