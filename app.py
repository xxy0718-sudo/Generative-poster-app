import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random, os

# ---------------------------
# Pastel color palette
# ---------------------------
def random_pastel_color(palette_type='pastel'):
    palettes = {
        'pastel': [(255, 179, 186), (255, 223, 186), (255, 255, 186),
                   (186, 255, 201), (186, 225, 255), (204, 204, 255)],
        'minimal': [(240, 240, 240), (220, 220, 220), (200, 200, 200)],
    }
    rgb = random.choice(palettes.get(palette_type, palettes['pastel']))
    return np.array(rgb) / 255

# ---------------------------
# Generate blob shape
# ---------------------------
def random_blob(center, radius, n_points=100, wobble=0.3):
    angles = np.linspace(0, 2*np.pi, n_points)
    r = radius * (1 + wobble * np.random.uniform(-1, 1, n_points))
    x = center[0] + r * np.cos(angles)
    y = center[1] + r * np.sin(angles)
    return np.column_stack([x, y])

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🎨 Generative Poster (Streamlit)")

layers = st.sidebar.slider("Layers", 3, 15, 8)
wobble = st.sidebar.slider("Wobble", 0.0, 0.5, 0.18)
palette_type = st.sidebar.selectbox("Palette", ["pastel", "minimal"])
mono_hue = st.sidebar.slider("Mono Hue (0–1)", 0.0, 1.0, 0.6)
save = st.sidebar.checkbox("Save poster", True)
save_dir = st.sidebar.text_input("Save dir", "posters")
width = st.sidebar.slider("Preview width (px)", 600, 2000, 1200)

if st.button("🔄 Regenerate"):
    st.experimental_rerun()

# ---------------------------
# Generate poster
# ---------------------------
fig, ax = plt.subplots(figsize=(width/100, width/100))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

for i in range(layers):
    center = np.random.uniform(2, 8, 2)
    radius = np.random.uniform(1.5, 3)
    blob = random_blob(center, radius, wobble=wobble)
    color = random_pastel_color(palette_type)
    ax.add_patch(Polygon(blob, closed=True, facecolor=color, alpha=0.6, edgecolor='gray', linewidth=0.5))

plt.text(3, 9.5, "Poster • pastel", fontsize=20, fontweight='bold')

# Show in Streamlit
st.pyplot(fig)

# Save file
if save:
    os.makedirs(save_dir, exist_ok=True)
    fname = os.path.join(save_dir, f"poster_{random.randint(1000,9999)}.png")
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    st.success(f"Saved: {fname}")
