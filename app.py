import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Points → Score Calculator", page_icon="🧮", layout="centered")

st.title("🧠 Neurbiology Small Tests Points → Score Calculator")
st.write(
    "Add or edit rows below. Each row is a **got / max** pair. "
    "We'll compute the normalized ratios, their average, and a 0–10 score."
)

# Sidebar options
with st.sidebar:
    st.header("⚙️ Options")
    round_digits = st.slider("Rounding digits", 0, 6, 2, help="How many decimals to show.")
    drop_invalid = st.checkbox("Ignore rows with invalid or missing values", True)
    st.markdown("---")
    st.caption("Tip: You can paste data from Excel (two columns: got, max) into the table.")

# Default example data
default_data = pd.DataFrame({
    "got": [11, 11.5, 12, 6, 16.5, 12],
    "max": [14, 13, 13, 16, 18, 12],
})

st.subheader("Input points")
st.write("Click the **＋** icon at the bottom to add more rows. Double‑click cells to edit.")
edited = st.data_editor(
    default_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "got": st.column_config.NumberColumn("Got", help="Points obtained (numerator)", step=0.5),
        "max": st.column_config.NumberColumn("Max", help="Maximum points (denominator)", step=0.5, min_value=0.0),
    },
    key="points_editor"
)

# Validate and compute
df = edited.copy()

# Coerce to numeric
for c in ["got", "max"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# Determine valid rows
valid_mask = df["got"].notna() & df["max"].notna() & (df["max"] != 0)

if not valid_mask.any():
    st.info("Add valid rows (both numbers, and Max ≠ 0) to get results.")
    st.stop()

if not drop_invalid and (~valid_mask).any():
    st.warning("There are invalid rows (missing values or Max=0). They will be shown as NaN in the results.")

# Compute per-row normalized scores
df["normalized"] = df["got"] / df["max"]
if drop_invalid:
    df_display = df[valid_mask].copy()
else:
    df_display = df.copy()

# Clip normalized values to [0, 1] only for display if desired? Usually not necessary; keep original.
avg_norm = df_display["normalized"].mean(skipna=True)
score_0_10 = avg_norm * 10.0

# Rounding for display
def r(x):
    if pd.isna(x):
        return np.nan
    # round for display only
    return round(float(x), round_digits)

df_out = df_display.copy()
df_out["normalized"] = df_out["normalized"].apply(r)

st.subheader("Results")
c1, c2 = st.columns(2)
with c1:
    st.metric("Average normalized", f"{round(avg_norm, round_digits)}")
with c2:
    st.metric("Score (0–10)", f"{round(score_0_10, round_digits)}")

with st.expander("Show per-row details"):
    st.dataframe(df_out, use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit. Duplicate 'got' values are allowed; each row counts once.")

