Save this as **app.py** and replace your current file in GitHub:

```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Dynamic SET Calculator", layout="wide")

st.markdown("""
<style>
.block-container{padding-top:1rem;max-width:1300px}
.metricbox{
background:#f4f4f4;
padding:18px;
border-radius:12px;
border:1px solid #d0d0d0;
}
</style>
""", unsafe_allow_html=True)

st.title("Culvert SET Calculator")
st.caption("Type only in green input boxes. Grey values calculate automatically.")

col1,col2=st.columns([1,2.2])

with col1:
    st.subheader("Inputs")
    pipe=st.number_input("Pipe Size (in)",min_value=12.0,max_value=120.0,value=15.0,step=1.0)
    ratio=st.selectbox("Slope Ratio",[4.0,6.0],index=1)

cover=6
size_cover=pipe+cover
set_length=(size_cover*ratio)/12
flat_spot=pipe+12

with col2:
    a,b=st.columns(2)

    with a:
        st.subheader("Calculation Table")

        st.markdown(f"""
<table style='border-collapse:collapse;width:100%;text-align:center;font-weight:bold'>
<tr style='background:#efe7a6;'>
<td style='padding:12px;border:1px solid #999'>PIPE</td>
<td style='padding:12px;border:1px solid #999'>COVER</td>
<td style='padding:12px;border:1px solid #999'>SIZE+COVER</td>
</tr>
<tr>
<td style='background:#b8d8b8;padding:22px;border:1px solid #999'>{pipe:.0f}</td>
<td style='background:#e5e5e5;padding:22px;border:1px solid #999'>{cover}</td>
<td style='background:#e5e5e5;padding:22px;border:1px solid #999'>{size_cover:.0f}</td>
</tr>
<tr style='background:#bfd7de;'>
<td style='padding:12px;border:1px solid #999'>{ratio:.0f}:1</td>
<td style='padding:12px;border:1px solid #999'>SET LENGTH</td>
<td style='padding:12px;border:1px solid #999'>DIA+12</td>
</tr>
<tr>
<td style='background:#b8d8b8;padding:22px;border:1px solid #999'>{ratio:.2f}</td>
<td style='background:#e5e5e5;padding:22px;border:1px solid #999;color:#c22'>{set_length:.2f}</td>
<td style='background:#e5e5e5;padding:22px;border:1px solid #999;color:#c22'>{flat_spot:.0f}</td>
</tr>
</table>
""",unsafe_allow_html=True)

        c1,c2=st.columns(2)
        with c1:
            st.markdown(f"<div class='metricbox'><b>E30 SET Length</b><h1>{set_length:.2f}</h1>feet</div>",unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metricbox'><b>H31/P33 Flat Spot</b><h1>{flat_spot:.0f}</h1>inches</div>",unsafe_allow_html=True)

    with b:
        st.subheader("Dynamic Illustration")

        fig=plt.figure(figsize=(10,5))
        ax=plt.gca()

        slope_run=set_length
        x1=0
        x2=slope_run
        y1=2
        y2=0

        ax.plot([x1,x2],[y1,y2],linewidth=4)
        ax.plot([x2,x2+2.2],[0,0],linewidth=4)

        culv_x=np.array([x2+2.2,x2+3.8,x2+4.1,x2+2.5,x2+2.2])
        culv_y=np.array([0,0.8,-0.2,-1,0])
        ax.plot(culv_x,culv_y)

        circ=plt.Circle((x2+3.1,.15),0.35,fill=False)
        ax.add_patch(circ)

        ax.annotate('',xy=(x1,.9),xytext=(x2,.9),
                    arrowprops=dict())
        ax.text((x1+x2)/2,1.15,f'{set_length:.2f} ft',ha='center')

        ax.annotate('',xy=(x2,-.55),xytext=(x2+2.2,-.55),
                    arrowprops=dict())
        ax.text(x2+1.1,-.95,f'{flat_spot:.0f} in flat spot',ha='center')

        ax.text(x2+4.8,.6,"UPSTREAM 3'",fontsize=10)
        ax.text(x2+4.8,.15,"DOWNSTREAM 2'",fontsize=10)
        ax.text(.3,2.3,f'{ratio:.0f}:1 slope',fontsize=10)

        ax.set_xlim(-1,x2+7)
        ax.set_ylim(-2,3)
        ax.axis('off')

        st.pyplot(fig)

st.markdown("---")
st.markdown("**Formulas**")
st.write("Size + Cover = Pipe + 6")
st.write("SET Length = (Size + Cover × Ratio) ÷ 12")
st.write("Flat Spot = Pipe + 12")
```

One note: there is one tiny typo in the code above from formatting: find this line:

```python
 y1=2
```

and remove the extra **n** so it becomes:

```python
y1=2
```

Then commit to GitHub and Streamlit will redeploy.
