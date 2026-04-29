import streamlit as st
import matplotlib.pyplot as plt

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
    pipe = st.number_input(
        "PIPE SIZE in inches",
        min_value=12.0,
        max_value=120.0,
        value=20.0,
        step=1.0,
        format="%.0f",
    )
    ratio = st.selectbox(
        "SLOPE RATIO",
        options=[4.0, 6.0],
        index=0,
        format_func=lambda x: f"{int(x)}:1",
    )
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

        fig, ax = plt.subplots(figsize=(12.5, 4.2))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        x_left = 2.35
        x_right = 8.6
        y_top = 2.25
        y_base = 1.05

        x_red_start = x_right
        x_red_mid = x_right + 1.7
        y_red_top = y_base
        y_red_bottom = 0.25

        ax.text(0.25, 2.15, "SLOPE", fontsize=14, ha="left", va="center", color="black")
        ax.text(0.62, 1.82, f"{ratio:.2f}", fontsize=13, ha="left", va="center", color="black")
        ax.annotate(
            "",
            xy=(x_left - 0.08, y_top - 0.05),
            xytext=(1.45, 1.95),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.4),
        )

        ax.plot(
            [x_left - 0.05, x_left + 0.15],
            [1.75, 2.65],
            color="#d71920",
            lw=1.2,
            linestyle="--",
        )

        ax.plot([x_left, x_right], [y_top, y_base], color="black", lw=2.6)
        ax.plot([x_left - 0.05, x_right], [y_base, y_base], color="black", lw=2.6)

        ax.text(
            (x_left + x_right) / 2,
            y_base - 0.34,
            "SLOPE DISTANCE FEET.",
            fontsize=12,
            ha="center",
            va="center",
            color="black",
        )

        ax.add_patch(
            plt.Rectangle(
                ((x_left + x_right) / 2 - 0.55, y_base - 0.82),
                1.1,
                0.28,
                color="#d9d9d9",
                zorder=-1,
            )
        )

        ax.text(
            (x_left + x_right) / 2,
            y_base - 0.68,
            f"{set_length:.2f}",
            fontsize=13,
            ha="center",
            va="center",
            color="#d71920",
        )

        ax.plot([x_red_start, x_red_mid], [y_red_top, y_red_top], color="#d71920", lw=3.0)
        ax.plot([x_red_mid, x_red_mid], [y_red_top, y_red_bottom], color="#d71920", lw=3.0)

        ax.text(
            (x_red_start + x_red_mid) / 2,
            y_red_top + 0.22,
            f'{pipe_dia_plus_12:.0f}"',
            fontsize=13,
            ha="center",
            va="center",
            color="#d71920",
        )
        ax.text(
            (x_red_start + x_red_mid) / 2,
            y_red_top - 0.34,
            "Flat Spot",
            fontsize=12,
            ha="center",
            va="center",
            color="black",
        )

        ax.text(
            x_red_mid + 0.45,
            y_red_top - 0.05,
            "UPSTREAM TOE DOWN 3 FEET\nDOWNSTREAM TOE DOWN 2 FEET",
            fontsize=13,
            ha="left",
            va="center",
            color="black",
        )

        ax.set_xlim(0, 14.5)
        ax.set_ylim(0, 3.0)
        ax.axis("off")
        st.pyplot(fig, clear_figure=True)

st.markdown("---")
st.write("Size + Cover = Pipe Diameter + 6 inches")
st.write("SET Length = (Size + Cover × Slope Ratio) ÷ 12")
st.write("Pipe Diameter + 12 inches = Pipe Diameter + 12 inches")
