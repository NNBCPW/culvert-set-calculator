import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

st.set_page_config(page_title="Dynamic SET Calculator", layout="wide")

st.markdown("""
<style>
.block-container {max-width:1450px;padding-top:1rem;}
.note-box {
background:#f3f3f3;border-left:6px solid #7ca982;padding:12px 16px;
margin-bottom:14px;color:#1f1f1f;font-weight:600;}
.formula-box {
background:#f6f6f6;border:1px solid #cfcfcf;border-radius:10px;
padding:14px 18px;color:#1f1f1f;}
</style>
""", unsafe_allow_html=True)

st.title("Culvert SET Calculator")
st.markdown("<div class='note-box'>Only type in the green input boxes. Grey values calculate automatically.</div>", unsafe_allow_html=True)

left, right = st.columns([1, 2.5])

with left:
    st.subheader("Green Input Boxes")
    pipe = st.number_input("PIPE SIZE in inches", min_value=12.0, max_value=120.0, value=15.0, step=1.0, format="%.0f")
    ratio = st.selectbox("SLOPE RATIO, 4:1 or 6:1", options=[4.0, 6.0], index=1, format_func=lambda x: f"{int(x)}:1")
    st.caption("Cover is fixed at 6 inches, matching the spreadsheet example.")

cover = 6.0
size_cover = pipe + cover
set_length = (size_cover * ratio) / 12.0
pipe_dia_plus_12 = pipe + 12.0

with right:
    table_col, drawing_col = st.columns([1.05, 1.45])

    with table_col:
        st.subheader("Calculation Table")
        st.markdown(f"""
<table style="width:100%;border-collapse:collapse;text-align:center;font-weight:800;font-size:18px;">
<tr style="background:#e6d88f;color:#111;">
<td style="padding:15px;border:1px solid #888;">PIPE</td>
<td style="padding:15px;border:1px solid #888;">COVER</td>
<td style="padding:15px;border:1px solid #888;">SIZE + COVER</td>
</tr>
<tr>
<td style="background:#b8d2b4;color:#111;padding:26px;border:1px solid #888;font-size:24px;">{pipe:.0f}</td>
<td style="background:#d9d9d9;color:#111;padding:26px;border:1px solid #888;font-size:24px;">{cover:.0f}</td>
<td style="background:#d9d9d9;color:#111;padding:26px;border:1px solid #888;font-size:24px;">{size_cover:.0f}</td>
</tr>
<tr style="background:#b8d1d8;color:#111;">
<td style="padding:15px;border:1px solid #888;">{ratio:.0f}:1</td>
<td style="padding:15px;border:1px solid #888;">SET LENGTH</td>
<td style="padding:15px;border:1px solid #888;">PIPE DIA + 12&quot;</td>
</tr>
<tr>
<td style="background:#b8d2b4;color:#111;padding:26px;border:1px solid #888;font-size:24px;">{ratio:.2f}</td>
<td style="background:#eeeeee;color:#d51919;padding:26px;border:1px solid #888;font-size:24px;">{set_length:.2f}</td>
<td style="background:#eeeeee;color:#d51919;padding:26px;border:1px solid #888;font-size:24px;">{pipe_dia_plus_12:.0f}</td>
</tr>
</table>
""", unsafe_allow_html=True)

    with drawing_col:
        st.subheader("Dynamic Illustration")
        fig, ax = plt.subplots(figsize=(12, 4.7))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        x_start = 0.0
        x_set_end = max(set_length, 4.0)
        x_flat_start = x_set_end + 0.25
        x_flat_end = x_flat_start + 2.45
        x_callout = x_flat_end + 0.25
        x_culvert = x_callout + 4.25

        y_top = 2.05
        y_bottom = 0.10

        ax.plot([x_start, x_set_end], [y_top, y_bottom], color="black", linewidth=2.5)
        ax.plot([x_start, x_set_end], [y_top - 0.18, y_bottom - 0.18], color="#d71920", linewidth=1.6)
        ax.plot([1.4, x_flat_start], [0, 0], color="black", linewidth=2.5)

        ax.plot([x_start - 0.35, x_start - 0.05], [y_top - 0.65, y_top + 0.38], color="#d71920", linewidth=1.2, linestyle="--")
        ax.plot([x_set_end - 0.05, x_set_end + 0.25], [y_bottom - 0.55, y_bottom + 0.45], color="#d71920", linewidth=1.2, linestyle="--")

        ax.annotate("", xy=(x_start + 0.05, y_top + 0.35), xytext=(x_set_end - 0.05, y_bottom + 0.35), arrowprops=dict(arrowstyle="<->", color="#d71920", lw=1.5))
        ax.text(x_set_end / 2, 0.38, f"{set_length:.2f}", ha="center", va="bottom", color="#d71920", fontsize=12, fontweight="bold")
        ax.text(x_set_end / 2, -0.05, "FEET", ha="center", va="top", color="black", fontsize=10)

        ax.plot([x_flat_start, x_flat_end], [0, 0], color="#d71920", linewidth=3)
        ax.plot([x_flat_start, x_flat_start], [-0.45, 0.45], color="#d71920", linewidth=2)
        ax.plot([x_flat_end, x_flat_end], [-0.45, 0.45], color="#d71920", linewidth=2)
        ax.annotate("", xy=(x_flat_start + 0.05, -0.55), xytext=(x_flat_end - 0.05, -0.55), arrowprops=dict(arrowstyle="<->", color="#d71920", lw=1.5))
        ax.text((x_flat_start + x_flat_end) / 2, -0.98, f"{pipe_dia_plus_12:.0f}\nINCHES", ha="center", va="top", color="#d71920", fontsize=11, fontweight="bold")

        callout = Rectangle((x_callout, -0.15), 3.25, 0.95, facecolor="#fff27a", edgecolor="#d71920", linewidth=1.6, linestyle="--")
        ax.add_patch(callout)
        ax.text(x_callout + 1.62, 0.32, "UPSTREAM 3'\nDOWNSTREAM 2'", ha="center", va="center", color="#111", fontsize=11, fontweight="bold")

        ax.annotate("", xy=(x_culvert - 0.45, 0.18), xytext=(x_callout + 3.25, 0.18), arrowprops=dict(arrowstyle="->", color="#c44", lw=1.3))

        culvert_body = Polygon([(x_culvert, -0.55), (x_culvert + 1.15, -0.95), (x_culvert + 1.15, -0.05), (x_culvert, 0.35)], closed=True, fill=False, edgecolor="#c44", linewidth=2.2)
        ax.add_patch(culvert_body)
        ax.plot([x_culvert - 0.9, x_culvert], [0.35, 0.05], color="#c44", linewidth=2.2)
        ax.plot([x_culvert - 0.9, x_culvert], [0.70, 0.40], color="#c44", linewidth=2.2)
        ax.plot([x_culvert + 1.15, x_culvert + 1.9], [0.15, 0.43], color="#c44", linewidth=2.2)
        ax.plot([x_culvert + 0.38, x_culvert + 1.05], [-0.15, 0.10], color="#c44", linewidth=2.0)

        ax.text(x_culvert + 2.15, 0.62, "TOE DOWN\nUPSTREAM 3'\nDOWNSTREAM 2'", ha="left", va="center", color="#d71920", fontsize=11, fontweight="bold")
        ax.text(x_start - 0.1, y_top + 0.42, "6:1 - 4:1", ha="left", va="bottom", color="black", fontsize=11, fontweight="bold")
        ax.text(x_start + 0.35, y_top + 0.1, f"{ratio:.2f}", ha="left", va="bottom", color="black", fontsize=11)
        ax.text(x_culvert - 2.25, -1.25, "PIPE DIA\n+ 12", ha="center", va="top", color="#d71920", fontsize=11, fontweight="bold")

        ax.set_xlim(-0.8, x_culvert + 5.0)
        ax.set_ylim(-2.0, 3.0)
        ax.axis("off")
        st.pyplot(fig, clear_figure=True)

st.markdown("---")
st.markdown(f"""
<div class='formula-box'>
<b>Formulas</b><br>
Size + Cover = Pipe Diameter + 6 inches<br>
SET Length = (Size + Cover × Slope Ratio) ÷ 12<br>
Pipe Diameter + 12 inches = Pipe Diameter + 12 inches<br><br>
Current result: <b>{pipe:.0f}</b> inch pipe + <b>12</b> inches = <b>{pipe_dia_plus_12:.0f}</b> inches
</div>
""", unsafe_allow_html=True)
