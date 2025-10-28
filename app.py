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
    base_colors = palettes.get(palette_type, [(200,200,200)])
    r, g, b = random.choice(base_colors)
    return (r/255, g/255, b/255, 0.6)

# ---------------------------
# Draw a circular blob with small irregular waves
# ---------------------------
def draw_irregular_wavy_circle(ax, x, y, radius=1, num_points=100, max_offset=0.08, color=(0.5,0.5,0.5,0.6)):
    angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
    xs, ys = [], []
    for angle in angles:
        # 每个点随机偏移一点半径，产生不规则细小波纹
        offset = random.uniform(-max_offset, max_offset)
        r = radius + offset
        xs.append(x + r * np.cos(angle))
        ys.append(y + r * np.sin(angle))
    polygon = Polygon(np.column_stack([xs, ys]), closed=True, color=color)
    ax.add_patch(polygon)

# ---------------------------
# Poster generator
# ---------------------------
def generate_irregular_wavy_poster(width=8, height=10, n_blobs=25, style='minimal', seed=None, save_path=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    for _ in range(n_blobs):
        x, y = random.uniform(0, width), random.uniform(0, height)
        radius = random.uniform(0.5, 1.5)
        color = random_pastel_color(style)
        draw_irregular_wavy_circle(ax, x, y, radius, num_points=100, max_offset=0.08, color=color)

    # Add top-left text
    ax.text(0.2, height-0.5, "Generative Poster", fontsize=16, fontweight='bold', ha='left', va='top')
    ax.text(0.2, height-1.0, "Week 2 Arts & Advanced Big Data", fontsize=12, ha='left', va='top')

    ax.set_aspect('equal')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=False)
    plt.show()

# ---------------------------
# Example usage
# ---------------------------
generate_irregular_wavy_poster(width=8, height=10, n_blobs=25, style='vivid', seed=42, save_path='irregular_wavy_poster.png')  위 코드를 github를 통해서 streamlit cloud 상에서 실행(배포)하고 싶어
