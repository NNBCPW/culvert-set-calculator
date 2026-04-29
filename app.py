import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

st.set_page_config(page_title="Dynamic SET Calculator", layout="wide")

st.markdown("""
<style>
.block-container{max-width:1450px;padding-top:1rem;}
.note-box{
background:#f3f3f3;
border-left:6px solid #7ca982;
padding:12px 16px;
margin-bottom:14px;
font-weight:600;
}
</style>
""", unsafe_allow_html=True)

st.title("Culvert SET Calculator")
st.markdown(
    "<div class='note-box'>Enter Pipe Size, Cover, and Slope Ratio. Note: 9 inches cover minimum may apply by standard, but lower values can be entered for calculation.</div>",
    unsafe_allow_html=True
)

left, right = st.columns([1, 2.6])

with left:
    st.subheader("Input Boxes")

    pipe = st.number_input(
        "PIPE SIZE (inches)",
        min_value=1.0,
        value=18.0,
        step=1.0,
        format="%.0f"
    )

    cover = st.number_input(
        "COVER (inches)",
        min_value=0.0,
        value=9.0,
        step=1.0,
        format="%.0f",
        help='9" may be a design minimum, but calculator allows any value.'
    )

    ratio = st.number_input(
        "SLOPE RATIO",
        min_value=0.1,
        value=4.0,
        step=.25,
        format="%.2f"
    )

size_cover = pipe + cover
set_length = (size_cover * ratio) / 12
pipe_dia_plus_12 = pipe + 12

with right:
    a, b = st.columns([1, 1.45])

    with a:
        st.subheader("Calculation Table")
        st.markdown(f"""
<table style='width:100%;border-collapse:collapse;text-align:center;font-weight:800;font-size:19px;'>
<tr style='background:#ded191;color:#222;'>
<td style='padding:14px;border:1px solid #888'>PIPE</td>
<td style='padding:14px;border:1px solid #888'>COVER</td>
<td style='padding:14px;border:1px solid #888'>SIZE + COVER</td>
</tr>

<tr>
<td style='background:#b7ccb3;color:#263526;padding:24px;border:1px solid #888;font-size:24px'>{pipe:.0f}</td>
<td style='background:#b7ccb3;color:#263526;padding:24px;border:1px solid #888;font-size:24px'>{cover:.0f}</td>
<td style='background:#dddddd;color:#333;padding:24px;border:1px solid #888;font-size:24px'>{size_cover:.0f}</td>
</tr>

<tr style='background:#bad0d6;color:#222;'>
<td style='padding:14px;border:1px solid #888'>RATIO</td>
<td style='padding:14px;border:1px solid #888'>SET LENGTH</td>
<td style='padding:14px;border:1px solid #888'>PIPE DIA +12&quot;</td>
</tr>

<tr>
<td style='background:#b7ccb3;color:#263526;padding:24px;border:1px solid #888;font-size:24px'>{ratio:.2f}:1</td>
<td style='background:#eeeeee;color:#b82121;padding:24px;border:1px solid #888;font-size:24px'>{set_length:.2f}</td>
<td style='background:#eeeeee;color:#b82121;padding:24px;border:1px solid #888;font-size:24px'>{pipe_dia_plus_12:.0f}</td>
</tr>
</table>
""", unsafe_allow_html=True)

    with b:
        st.subheader("Dynamic Illustration")

        fig, ax = plt.subplots(figsize=(12.5, 3.7))
        ax.set_facecolor("white")
        fig.patch.set_facecolor("white")

        x0 = 1
        y0 = 2.25
        x1 = 7.6
        y1 = 1.15
        x2 = x1 + 1.75

        # No grid lines in the illustration.

        ax.plot([x0 - .12, x0 + .12], [1.95, 2.65],
                color="#d71920", linestyle="--", lw=1.4)

        ax.plot([x0, x1], [y0, y1], color="black", lw=3.0)

        ax.add_patch(Rectangle(
            ((x0 + x1) / 2 - .70, y0 - .23),
            1.4, .40,
            facecolor="#dddddd",
            edgecolor="none"
        ))

        ax.text((x0 + x1) / 2, y0 - .035,
                f"{set_length:.2f}",
                color="#d71920",
                fontsize=18,
                fontweight="bold",
                ha="center",
                va="center")

        ax.text((x0 + x1) / 2,
                y1 - .05,
                "SLOPE DISTANCE FEET.",
                fontsize=16,
                ha="center",
                va="top",
                color="black")

        ax.plot([x1, x2], [y1, y1], color="#d71920", lw=3.8)
        ax.plot([x2, x2], [y1, .25], color="#d71920", lw=3.8)

        ax.text((x1 + x2) / 2, y1 - .32,
                f'{pipe_dia_plus_12:.0f}"',
                color="#d71920",
                fontsize=17,
                fontweight="bold",
                ha="center")

        ax.text((x1 + x2) / 2, y1 - .70,
                "Flat Spot",
                fontsize=16,
                ha="center",
                color="black")

        ax.text(x2 + .45, y1 - .03,
                "UPSTREAM TOE DOWN 3 FEET\nDOWNSTREAM TOE DOWN 2 FEET",
                fontsize=16,
                ha="left",
                va="center",
                color="black")

        ax.text(x0 + .12, y0 + .42,
                f"SLOPE {ratio:.2f}:1",
                fontsize=15,
                ha="left",
                color="black")

        ax.set_xlim(.25, 13)
        ax.set_ylim(0, 2.9)
        ax.tick_params(left=False, bottom=False,
                       labelleft=False, labelbottom=False)

        for s in ax.spines.values():
            s.set_visible(False)

        st.pyplot(fig, clear_figure=True)

st.markdown("---")
st.write(f"Size + Cover = {pipe:.0f} + {cover:.0f} = {size_cover:.0f} inches")
st.write(f"SET Length = ({size_cover:.0f} × {ratio:.2f}) ÷ 12 = {set_length:.2f} ft")
st.write(f"Pipe Diameter + 12 inches = {pipe:.0f} + 12 = {pipe_dia_plus_12:.0f} inches")
