import streamlit as st
from PIL import Image, ImageDraw
import numpy as np, math, random, io

st.set_page_config(layout="wide", page_title="Unique Poster Generator")

st.title("Unique Poster • vivid")
st.markdown("通过参数调整生成独一无二的艺术海报")

# ======= 参数面板 =======
with st.sidebar:
    st.header("参数设置")
    seed = st.number_input("Seed 随机种子", value=2025, step=1)
    layers = st.slider("Layers 图层数量", 1, 40, 12)
    wobble = st.slider("Wobble 尖刺波动", 0.0, 1.0, 0.25)
    palette_style = st.selectbox("颜色风格", ["vivid", "muted", "cool", "warm", "pastel"])
    outline_width = st.slider("描边粗细", 0, 8, 2)
    alpha = st.slider("透明度 (0-255)", 10, 255, 150)
    size = st.slider("画布大小 (px)", 600, 1600, 1000)
    regenerate = st.button("生成 / 刷新")

# ======= 颜色方案 =======
PALETTES = {
    "vivid": [(39,121,200),(77,183,255),(243,118,97),(186,84,170),(114,221,204),(91,155,173)],
    "muted": [(120,150,170),(140,125,135),(150,160,150),(110,130,120),(130,110,140)],
    "cool": [(33,150,243),(41,121,255),(124,179,195),(88,170,220),(64,128,192)],
    "warm": [(244,143,177),(255,112,67),(255,193,7),(244,67,54),(255,159,128)],
    "pastel": [(198,234,255),(255,220,235),(230,255,240),(250,240,255),(240,255,220)]
}

# ======= 主绘图函数 =======
def generate_spiky_image(seed=2025, layers=12, wobble=0.25, size=1000, palette_name="vivid", outline_w=2, alpha=150):
    random.seed(int(seed))
    np.random.seed(int(seed) % 4294967295)
    palette = PALETTES.get(palette_name, PALETTES["vivid"])
    canvas = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas, "RGBA")
    cx, cy = size // 2, size // 2

    # 控制形状大致排布方向（上下叠）
    centers = []
    angle = -math.pi / 3
    for i in range(layers):
        r = (i / layers) * (size * 0.35)
        dx = int(math.cos(angle + (i * 0.14)) * r * 0.9)
        dy = int(math.sin(angle + (i * 0.14)) * r * 1.05)
        centers.append((cx + dx, cy + dy))

    for i, c in enumerate(centers[::-1]):  # 从下往上绘制
        col = palette[i % len(palette)]
        # 微调颜色
        jitter = tuple(max(0, min(255, int(v + random.randint(-25, 25)))) for v in col)
        fill = (jitter[0], jitter[1], jitter[2], alpha)
        edge = (max(0, jitter[0] - 30), max(0, jitter[1] - 30), max(0, jitter[2] - 30), 255)

        # 当前层的半径
        min_r, max_r = 100, 400
        r = int(min_r + (i / len(centers)) * (max_r - min_r) + random.uniform(-wobble, wobble) * 80)

        spikes = 180
        points = []
        for k in range(spikes):
            theta = 2 * math.pi * (k / spikes)
            spike_strength = 1.0 + (0.25 + random.random() * 0.6) * math.sin(6 * theta + random.random() * 6)
            radial_noise = 1.0 + random.uniform(-wobble, wobble) * 0.6
            rad = r * spike_strength * radial_noise
            x = c[0] + rad * math.cos(theta)
            y = c[1] + rad * math.sin(theta)
            points.append((x, y))

        # 填充
        draw.polygon(points, fill=fill)
        if outline_w > 0:
            for a in range(len(points)):
                draw.line([points[a], points[(a + 1) % len(points)]], fill=edge, width=outline_w)

    return canvas

# ======= 生成图像并展示 =======
img = generate_spiky_image(seed=seed, layers=layers, wobble=wobble, size=size,
                           palette_name=palette_style, outline_w=outline_width, alpha=alpha)

# 转成PNG缓冲
buf = io.BytesIO()
img.save(buf, format="PNG")
buf.seek(0)

# 展示与下载
st.image(buf, use_column_width=True)
st.download_button("下载海报 PNG", data=buf, file_name="unique_poster.png", mime="image/png")

st.markdown("---")
st.markdown("此 Streamlit 应用生成类似实验艺术风格的彩色尖刺海报。可部署至 [Streamlit Cloud](https://streamlit.io/cloud) 或本地运行。")
