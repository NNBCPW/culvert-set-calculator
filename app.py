import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

st.set_page_config(page_title="Dynamic SET Calculator", layout="wide")

st.markdown("""
<style>
.block-container {max-width:1450px;padding-top:1rem;}
.note-box {
  background:#f3f3f3;
  border-left:6px solid #7ca982;
  padding:12px 16px;
  margin-bottom:14px;
  color:#1f1f1f;
  font-weight:600;
}
</style>
""", unsafe_allow_html=True)

st.title("Culvert SET Calculator")
st.markdown(
    "<div class='note-box'>Only type in the green boxes. Grey values calculate automatically.</div>",
    unsafe_allow_html=True
)

left, right = st.columns([1, 2.6])

with left:
    st.subheader("Green Input Boxes")
    pipe = st.number_input("PIPE SIZE in inches", min_value=12.0, max_value=120.0, value=20.0, step=1.0, format="%.0f")
    ratio = st.selectbox("SLOPE RATIO", options=[4.0, 6.0], index=0, format_func=lambda x: f"{int(x)}:1")
    st.caption("Cover is fixed at 6 inches.")

cover = 6.0
size_cover = pipe + cover
set_length = (size_cover * ratio) / 12.0
pipe_dia_plus_12 = pipe + 12.0

with right:
    table_col, drawing_col = st.columns([1.0, 1.45])

    with table_col:
        st.subheader("Calculation Table")
        st.markdown(f"""
<table style="width:100%;border-collapse:collapse;text-align:center;font-weight:800;font-size:18px;">
<tr style="background:#e6d88f;color:#111;">
<td style="padding:14px;border:1px solid #888;">PIPE</td>
<td style="padding:14px;border:1px solid #888;">COVER</td>
<td style="padding:14px;border:1px solid #888;">SIZE + COVER</td>
</tr>
<tr>
<td style="background:#b8d2b4;color:#111;padding:24px;border:1px solid #888;font-size:24px;">{pipe:.0f}</td>
<td style="background:#d9d9d9;color:#111;padding:24px;border:1px solid #888;font-size:24px;">{cover:.0f}</td>
<td style="background:#d9d9d9;color:#111;padding:24px;border:1px solid #888;font-size:24px;">{size_cover:.0f}</td>
</tr>
<tr style="background:#b8d1d8;color:#111;">
<td style="padding:14px;border:1px solid #888;">{ratio:.0f}:1</td>
<td style="padding:14px;border:1px solid #888;">SET LENGTH</td>
<td style="padding:14px;border:1px solid #888;">PIPE DIA + 12&quot;</td>
</tr>
<tr>
<td style="background:#b8d2b4;color:#111;padding:24px;border:1px solid #888;font-size:24px;">{ratio:.2f}</td>
<td style="background:#eeeeee;color:#d71920;padding:24px;border:1px solid #888;font-size:24px;">{set_length:.2f}</td>
<td style="background:#eeeeee;color:#d71920;padding:24px;border:1px solid #888;font-size:24px;">{pipe_dia_plus_12:.0f}</td>
</tr>
</table>
""", unsafe_allow_html=True)

    with drawing_col:
        st.subheader("Dynamic Illustration")

        fig, ax = plt.subplots(figsize=(12.8, 4.7))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        # Layout coordinates.  The set length is shown as text, while the
        # geometry remains readable for all pipe sizes.
        x0 = 1.5
        y0 = 2.15
        x_end = 8.0
        y_end = 0.45
        x_flat_end = 9.85
        box_x = 9.95
        box_y = 0.15
        box_w = 3.0
        box_h = 0.9

        # Left slope label and arrow, matching the spreadsheet style.
        ax.text(0.15, 2.65, "SLOPE", fontsize=12, fontweight="bold", ha="left")
        ax.text(0.52, 2.36, f"{ratio:.2f}", fontsize=11, ha="left")
        ax.annotate("", xy=(x0 - 0.12, y0 - 0.04), xytext=(0.95, 2.38),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5))

        # Red dashed end guides.
        ax.plot([x0 - 0.1, x0 + 0.25], [1.65, 2.75], color="#d71920", lw=1.1, linestyle="--")
        ax.plot([x_end - 0.06, x_end + 0.2], [-0.05, 0.95], color="#d71920", lw=1.1, linestyle="--")

        # Slope lines: black top and red construction line under it.
        ax.plot([x0, x_end], [y0, y_end], color="black", lw=2.8)
        ax.plot([x0 + 0.06, x_end], [y0 - 0.18, y_end - 0.18], color="#d71920", lw=1.7)

        # Main horizontal baseline.
        ax.plot([x0, x_end], [0.20, 0.20], color="black", lw=2.5)

        # Slope distance label below the baseline.
        ax.text((x0 + x_end) / 2, -0.05, "SLOPE DISTANCE FEET.", fontsize=11, ha="center")

        # Red dimension arrow parallel to the slope.
        ax.annotate("", xy=(x_end - 0.08, y_end + 0.02), xytext=(x0 + 0.1, y0 - 0.12),
                    arrowprops=dict(arrowstyle="<->", color="#d71920", lw=1.5))
        ax.text((x0 + x_end) / 2, 0.52, f"{set_length:.2f}", color="#d71920",
                fontsize=12, fontweight="bold", ha="center")

        # Pipe diameter plus 12 inch section.
        ax.add_patch(Rectangle((x_end, 0.2), x_flat_end - x_end, 0.48,
                               facecolor="#d9d9d9", edgecolor="none"))
        ax.plot([x_end, x_flat_end], [0.68, 0.68], color="#d71920", lw=3)
        ax.plot([x_end, x_end], [0.10, 0.96], color="#d71920", lw=2)
        ax.plot([x_flat_end, x_flat_end], [0.10, 0.96], color="#d71920", lw=2)
        ax.annotate("", xy=(x_end + 0.05, 0.05), xytext=(x_flat_end - 0.05, 0.05),
                    arrowprops=dict(arrowstyle="<->", color="#d71920", lw=1.4))
        ax.text((x_end + x_flat_end) / 2, 0.82, f"{pipe_dia_plus_12:.0f}",
                color="#d71920", fontsize=12, fontweight="bold", ha="center")
        ax.text((x_end + x_flat_end) / 2, 0.30, "INCHES",
                color="black", fontsize=10, ha="center")
        ax.text(x_end + 0.05, -0.38, "FLAT\nSPOT",
                color="#d71920", fontsize=11, fontweight="bold", ha="left")

        # Upstream/downstream yellow callout.
        ax.add_patch(Rectangle((box_x, box_y), box_w, box_h,
                               facecolor="#fff27a", edgecolor="#d71920",
                               linewidth=1.7, linestyle="--"))
        ax.text(box_x + box_w/2, box_y + box_h/2, "UPSTREAM 3'\nDOWNSTREAM 2'",
                fontsize=11, fontweight="bold", ha="center", va="center", color="black")

        # Right vertical dimension by callout.
        ax.plot([box_x + box_w + 0.25, box_x + box_w + 0.25], [box_y, box_y + box_h],
                color="#d71920", lw=1.5)
        ax.annotate("", xy=(box_x + box_w + 0.25, box_y + 0.03),
                    xytext=(box_x + box_w + 0.25, box_y + box_h - 0.03),
                    arrowprops=dict(arrowstyle="<->", color="#d71920", lw=1.2))

        # Toe down block / headwall sketch, closer to the spreadsheet reference.
        toe_x = box_x + box_w + 1.15
        toe_y = 0.28
        block = Polygon([
            (toe_x, toe_y + 0.45),
            (toe_x + 0.65, toe_y + 0.15),
            (toe_x + 0.65, toe_y - 0.75),
            (toe_x, toe_y - 0.45)
        ], closed=True, fill=False, edgecolor="#c44", linewidth=2.2)
        ax.add_patch(block)
        ax.plot([toe_x - 1.2, toe_x], [toe_y + 0.75, toe_y + 0.45], color="#c44", lw=2.2)
        ax.plot([toe_x - 1.2, toe_x], [toe_y + 0.55, toe_y + 0.25], color="#c44", lw=2.2)
        ax.plot([toe_x + 0.65, toe_x + 1.35], [toe_y + 0.10, toe_y + 0.45], color="#c44", lw=2.2)
        ax.plot([toe_x + 0.25, toe_x + 0.65], [toe_y - 0.10, toe_y + 0.10], color="#c44", lw=2.0)

        ax.text(toe_x + 1.65, toe_y + 0.55, "TOE DOWN\nUPSTREAM 3'\nDOWNSTREAM 2'",
                color="#d71920", fontsize=11, fontweight="bold", ha="left", va="center")

        ax.set_xlim(-0.2, toe_x + 5.4)
        ax.set_ylim(-1.15, 3.1)
        ax.axis("off")
        st.pyplot(fig, clear_figure=True)

st.markdown("---")
st.write("Size + Cover = Pipe Diameter + 6 inches")
st.write("SET Length = (Size + Cover × Slope Ratio) ÷ 12")
st.write("Pipe Diameter + 12 inches = Pipe Diameter + 12 inches")
