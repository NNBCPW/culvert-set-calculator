import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

st.set_page_config(page_title='Dynamic SET Calculator',layout='wide')

st.markdown('''
<style>
.block-container{max-width:1400px;padding-top:1rem;}
.metric{
background:#f3f3f3;
padding:18px;
border-radius:12px;
border:1px solid #c8c8c8;
}
</style>
''',unsafe_allow_html=True)

st.title('Culvert SET Calculator')

left,right=st.columns([1,2.3])

with left:
    pipe=st.number_input('Pipe Size (in)',12.0,120.0,15.0)
    ratio=st.selectbox('Slope Ratio',[4.0,6.0],index=1)

cover=6
size_cover=pipe+cover
set_length=(size_cover*ratio)/12
flat_spot=pipe+12

with right:
    a,b=st.columns([1.05,1.35])

    with a:
        st.subheader('Calculation Table')

        st.markdown(f'''
<table style="width:100%;border-collapse:collapse;text-align:center;font-weight:700;">
<tr style="background:#e6d88f;color:#1f1f1f;">
<td style="padding:14px;border:1px solid #999">PIPE</td>
<td style="padding:14px;border:1px solid #999">COVER</td>
<td style="padding:14px;border:1px solid #999">SIZE+COVER</td>
</tr>
<tr>
<td style="background:#b8d2b4;color:#111;padding:24px;border:1px solid #999">{pipe:.0f}</td>
<td style="background:#d7d7d7;color:#111;padding:24px;border:1px solid #999">{cover}</td>
<td style="background:#d7d7d7;color:#111;padding:24px;border:1px solid #999">{size_cover:.0f}</td>
</tr>
<tr style="background:#b8d1d8;color:#111;">
<td style="padding:14px;border:1px solid #999">{ratio:.0f}:1</td>
<td style="padding:14px;border:1px solid #999">SET LENGTH</td>
<td style="padding:14px;border:1px solid #999">DIA+12"</td>
</tr>
<tr>
<td style="background:#b8d2b4;color:#111;padding:24px;border:1px solid #999">{ratio:.2f}</td>
<td style="background:#ececec;color:#d51919;padding:24px;border:1px solid #999">{set_length:.2f}</td>
<td style="background:#ececec;color:#d51919;padding:24px;border:1px solid #999">{flat_spot:.0f}</td>
</tr>
</table>
st.write('Flat Spot = Pipe + 12")
