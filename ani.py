import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline
import time

st.set_page_config(page_title="Lerp Animator", layout="wide")
st.title("🎞️ Lerp Animator with Custom Animation Curve")

# --- Sidebar controls ---
st.sidebar.header("Animation Settings")
frames = st.sidebar.slider("Frames", 10, 200, 80)
delay = st.sidebar.slider("Delay (seconds)", 0.01, 0.2, 0.03)
start_pos = np.array(st.sidebar.slider("Start Position (x, y)", -5.0, 5.0, (0.0, 0.0)))
end_pos = np.array(st.sidebar.slider("End Position (x, y)", -5.0, 5.0, (5.0, 5.0)))

# --- Initialize curve points ---
if "curve_points" not in st.session_state:
    st.session_state.curve_points = [(0.0, 0.0), (1.0, 1.0)]

st.write("### Define your custom Animation Curve")
st.caption("Add (x,y) points to shape your easing. The curve maps time (0→1) → progress (0→1 or beyond).")

# --- Add / remove points ---
col1, col2, col3 = st.columns(3)
with col1:
    x_val = st.number_input("Key X (0→1)", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
with col2:
    y_val = st.number_input("Key Y (-1→2)", min_value=-1.0, max_value=2.0, value=0.5, step=0.05)
with col3:
    if st.button("➕ Add Key"):
        st.session_state.curve_points.append((float(x_val), float(y_val)))
        st.session_state.curve_points = sorted(st.session_state.curve_points)

if st.button("🗑️ Reset Keys"):
    st.session_state.curve_points = [(0.0, 0.0), (1.0, 1.0)]

points = np.array(st.session_state.curve_points)
x, y = points[:, 0], points[:, 1]

# --- Build spline curve ---
try:
    spline = make_interp_spline(x, y, k=3)
except Exception:
    spline = make_interp_spline([0, 1], [0, 1], k=1)

x_smooth = np.linspace(0, 1, 300)
y_smooth = spline(x_smooth)

# --- Plot curve ---
curve_fig = go.Figure()
curve_fig.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode="lines", name="Curve", line=dict(color="lime")))
curve_fig.add_trace(go.Scatter(x=x, y=y, mode="markers+text", text=[f"{i}" for i in range(len(x))],
                               textposition="top center", name="Keys", marker=dict(size=8, color="orange")))
curve_fig.update_layout(height=300, title="Animation Curve Editor",
                        xaxis_title="Time (0→1)", yaxis_title="Progress", template="plotly_dark")
st.plotly_chart(curve_fig, use_container_width=True)

# --- Animate lerp using curve ---
if st.button("▶️ Play Animation"):
    stframe = st.empty()
    for i in range(frames + 1):
        t = i / frames
        curve_t = float(spline(t))
        pos = start_pos + (end_pos - start_pos) * curve_t

        anim_fig = go.Figure()
        anim_fig.add_trace(go.Scatter(x=[start_pos[0], end_pos[0]], y=[start_pos[1], end_pos[1]],
                                      mode="markers", marker=dict(color="red", size=10), name="Start/End"))
        anim_fig.add_trace(go.Scatter(x=[pos[0]], y=[pos[1]],
                                      mode="markers", marker=dict(color="cyan", size=14), name="Moving Point"))
        anim_fig.update_layout(title=f"Lerping... t={t:.2f}, curve={curve_t:.2f}",
                               xaxis=dict(range=[-6, 6]), yaxis=dict(range=[-6, 6]), template="plotly_dark",
                               height=400)
        stframe.plotly_chart(anim_fig, use_container_width=True)
        time.sleep(delay)
