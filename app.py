import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random

# ---------------------------
# Pastel color generator
# ---------------------------
def random_pastel_color(palette_type='minimal'):
    palettes = {
        'minimal': [(255, 179, 186), (255, 223, 186), (255, 255, 186),
                    (186, 255, 201), (186, 225, 255)],
        'vivid': [(255, 153, 153), (255, 204, 153), (255, 255, 153),
                  (153, 255, 204), (153, 204, 255)],
        'noisetouch': [(230, 180, 180), (230, 210, 180), (230, 230, 180),
                       (180, 230, 210), (180, 210, 230)]
    }
    base_colors = palettes.get(palette_type, [(200, 200, 200)])
    r, g, b = random.choice(base_colors)
    return (r / 255, g / 255, b / 255, 0.6)

# ---------------------------
# Draw a circular blob with small irregular waves
# ---------------------------
def draw_irregular_wavy_circle(ax, x, y, radius=1, num_points=100, max_offset=0.08, color=(0.5, 0.5, 0.5, 0.6)):
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    xs, ys = [], []
    for angle in angles:
        offset = random.uniform(-max_offset, max_offset)
        r = radius + offset
        xs.append(x + r * np.cos(angle))
        ys.append(y + r * np.sin(angle))
    polygon = Polygon(np.column_stack([xs, ys]), closed=True, color=color)
    ax.add_patch(polygon)

# ---------------------------
# Poster generator
# ---------------------------
def generate_layered_wavy_poster(width=8, height=10, n_blobs=10, style='minimal', seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    for _ in range(n_blobs):
        x, y = random.uniform(0, width), random.uniform(0, height)
        radius = random.uniform(0.5, 2)
        color = random_pastel_color(style)
        max_offset = random.uniform(0.03, 0.12)
        draw_irregular_wavy_circle(ax, x, y, radius, num_points=120, max_offset=max_offset, color=color)

    ax.text(0.2, height - 0.5, "Generative Poster", fontsize=16, fontweight='bold', ha='left', va='top')
    ax.text(0.2, height - 1.0, "Week 2 Arts & Advanced Big Data", fontsize=12, ha='left', va='top')
    ax.set_aspect('equal')

    return fig


# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🎨 Generative Poster Creator")
st.write("파스텔 톤의 물결형 원을 겹겹이 쌓아 만드는 생성형 포스터")

style = st.selectbox("🎨 Color Style 선택", ["minimal", "vivid", "noisetouch"])
n_blobs = st.slider("원 개수", 5, 30, 10)
seed = st.number_input("Seed (재현 가능성)", min_value=0, value=42)

if st.button("포스터 생성하기 🎨"):
    fig = generate_layered_wavy_poster(width=8, height=10, n_blobs=n_blobs, style=style, seed=seed)
    st.pyplot(fig)
