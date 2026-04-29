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
""",unsafe_allow_html=True)

st.title("Culvert SET Calculator")
st.markdown(
"<div class='note-box'>Enter Pipe Size, Cover, and Slope Ratio. Note: 9 inches cover minimum may apply by standard, but lower values can be entered for calculation.</div>",
unsafe_allow_html=True
)

left,right=st.columns([1,2.6])

with left:
    pipe=st.number_input(
        "PIPE SIZE (inches)",
        min_value=1.0,
        value=18.0,
        step=1.0,
        format="%.0f"
    )

    cover=st.number_input(
        "COVER (inches)",
        min_value=0.0,
        value=9.0,
        step=1.0,
        format="%.0f",
        help='9" may be a design minimum, but calculator allows any value.'
    )

    ratio=st.number_input(
        "SLOPE RATIO",
        min_value=0.1,
        value=4.0,
        step=.25,
        format="%.2f"
    )

size_cover=pipe+cover
set_length=(size_cover*ratio)/12
pipe_dia_plus_12=pipe+12

with right:
    a,b=st.columns([1,1.45])

    with a:
        st.subheader("Calculation Table")
        st.markdown(f"""
<table style='width:100%;border-collapse:collapse;text-align:center;font-weight:800'>
<tr style='background:#e6d88f'>
<td style='padding:14px;border:1px solid #888'>PIPE</td>
<td style='padding:14px;border:1px solid #888'>COVER</td>
<td style='padding:14px;border:1px solid #888'>SIZE + COVER</td>
</tr>

<tr>
<td style='background:#b8d2b4;padding:24px;border:1px solid #888'>{pipe:.0f}</td>
<td style='background:#b8d2b4;padding:24px;border:1px solid #888'>{cover:.0f}</td>
<td style='background:#d9d9d9;padding:24px;border:1px solid #888'>{size_cover:.0f}</td>
</tr>

<tr style='background:#b8d1d8'>
<td style='padding:14px;border:1px solid #888'>RATIO</td>
<td style='padding:14px;border:1px solid #888'>SET LENGTH</td>
<td style='padding:14px;border:1px solid #888'>PIPE DIA +12"</td>
</tr>

<tr>
<td style='background:#b8d2b4;padding:24px;border:1px solid #888'>{ratio:.2f}:1</td>
<td style='background:#eee;color:red;padding:24px;border:1px solid #888'>{set_length:.2f}</td>
<td style='background:#eee;color:red;padding:24px;border:1px solid #888'>{pipe_dia_plus_12:.0f}</td>
</tr>
</table>
""",unsafe_allow_html=True)

    with b:
        st.subheader("Dynamic Illustration")
        fig,ax=plt.subplots(figsize=(12.5,3.7))
        ax.set_facecolor("white")

        x0=1
        y0=2.25
        x1=7.6
        y1=1.15
        x2=x1+1.75

        ax.set_xticks([i*.75 for i in range(18)])
        ax.set_yticks([i*.35 for i in range(9)])
        ax.grid(True,color="#dedede")

        ax.plot([x0-.12,x0+.12],[1.95,2.65],
                color='red',linestyle='--')

        ax.plot([x0,x1],[y0,y1],color='black',lw=2.6)

        ax.add_patch(Rectangle(
            ((x0+x1)/2-.55,y0-.20),
            1.1,.32,
            facecolor="#d9d9d9"
        ))

        ax.text((x0+x1)/2,y0-.04,
                f"{set_length:.2f}",
                color='red',
                ha='center')

        ax.text((x0+x1)/2,
                y1-.02,
                "SLOPE DISTANCE FEET.",
                ha='center')

        ax.plot([x1,x2],[y1,y1],color='red',lw=3)
        ax.plot([x2,x2],[y1,.25],color='red',lw=3)

        ax.text((x1+x2)/2,y1-.28,
                f'{pipe_dia_plus_12:.0f}"',
                color='red',
                ha='center')

        ax.text((x1+x2)/2,y1-.58,
                "Flat Spot",
                ha='center')

        ax.text(x2+.45,y1-.03,
        "UPSTREAM TOE DOWN 3 FEET\nDOWNSTREAM TOE DOWN 2 FEET",
        ha='left')

        ax.text(x0+.12,y0+.38,
                f"SLOPE {ratio:.2f}:1")

        ax.set_xlim(.25,13)
        ax.set_ylim(0,2.9)
        ax.tick_params(left=False,bottom=False,
                       labelleft=False,labelbottom=False)

        for s in ax.spines.values():
            s.set_visible(False)

        st.pyplot(fig)

st.markdown("---")
st.write(f"SET Length = ({size_cover:.0f} × {ratio:.2f}) ÷ 12 = {set_length:.2f} ft")
