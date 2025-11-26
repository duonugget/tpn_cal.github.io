import streamlit as st
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Scatterplot Animate", layout="centered")

st.title("Scatterplot_animate")

# --- User parameters ---
st.sidebar.header("Animation Parameters")
x1 = st.sidebar.slider("xDim1 (start x)", 0.0, 1.0, 0.2)
y1 = st.sidebar.slider("yDim1 (start y)", 0.0, 1.0, 0.2)
r1 = st.sidebar.slider("rDim1 (start radius)", 0.01, 0.2, 0.05)
x2 = st.sidebar.slider("xDim2 (end x)", 0.0, 1.0, 0.8)
y2 = st.sidebar.slider("yDim2 (end y)", 0.0, 1.0, 0.8)
r2 = st.sidebar.slider("rDim2 (end radius)", 0.01, 0.2, 0.1)

color = st.sidebar.color_picker("Circle Color", "#1f77b4")
numFrames = st.sidebar.slider("Number of Frames", 5, 60, 60)
delay = st.sidebar.slider("Delay (seconds per frame)", 0.01, 0.2, 0.05)

# --- Animation logic ---
placeholder = st.empty()

for f in range(numFrames + 1):
    p = f / numFrames
    x = x1 + (x2 - x1) * p
    y = y1 + (y2 - y1) * p
    r = r1 + (r2 - r1) * p

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Circle + center point
    circle = plt.Circle((x, y), r, color=color, alpha=0.4, edgecolor='black')
    ax.add_artist(circle)
    ax.plot(x, y, 'ko', markersize=5)  # center point (black dot)

    # Start & End markers
    ax.plot(x1, y1, 'ro', markersize=6, label="Start")
    ax.plot(x2, y2, 'r^', markersize=6, label="End")

    # Add legend only once
    if f == 0:
        ax.legend(loc='upper right')

    placeholder.pyplot(fig)
    plt.close(fig)

    time.sleep(delay)
