import streamlit as st
import pandas as pd
import altair as alt
import time

# === Data ===
data = """score,group
68.2,A
70.5,A
65.3,A
75.1,A
54.2,B
59.8,B
63.1,B
50.9,B
62.3,C
64.7,C
67.2,C
70.4,C
71.9,A
73.3,A
57.1,B
55.6,B
68.9,C
66.8,C
63.5,B
61.2,A
"""
df = pd.read_csv(pd.io.common.StringIO(data))

# === Setup UI ===
st.title("📊 Click-to-Switch Animated Histogram (Single Group)")

groups = sorted(df["group"].unique())

# Use Streamlit buttons for click-based selection
cols = st.columns(len(groups))
clicked_group = None
for i, g in enumerate(groups):
    if cols[i].button(f"Show Group {g}"):
        clicked_group = g

# Session state to track previous group (for animation)
if "prev_group" not in st.session_state:
    st.session_state.prev_group = groups[0]

if clicked_group is None:
    clicked_group = st.session_state.prev_group

# === Chart building ===
placeholder = st.empty()

def plot_hist(group, opacity=1.0):
    sub = df[df["group"] == group]
    chart = alt.Chart(sub).mark_bar(opacity=opacity).encode(
        x=alt.X("score:Q", bin=alt.Bin(maxbins=10), title="Score"),
        y=alt.Y("count()", title="Count"),
        tooltip=["score"]
    ).properties(width=600, height=400, title=f"Group {group}")
    return chart

# === Animation when switching ===
if clicked_group != st.session_state.prev_group:
    old_group = st.session_state.prev_group
    new_group = clicked_group

    # Fade out old histogram
    for alpha in [1.0, 0.7, 0.4, 0.1]:
        placeholder.altair_chart(plot_hist(old_group, opacity=alpha), use_container_width=True)
        time.sleep(0.1)

    # Fade in new histogram
    for alpha in [0.1, 0.4, 0.7, 1.0]:
        placeholder.altair_chart(plot_hist(new_group, opacity=alpha), use_container_width=True)
        time.sleep(0.1)

    st.session_state.prev_group = new_group
else:
    placeholder.altair_chart(plot_hist(clicked_group), use_container_width=True)
