import math
import streamlit as st

st.set_page_config(page_title="Culvert SET Calculator", page_icon="📐", layout="wide")

st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; max-width: 1200px;}
    .title {font-size: 2.1rem; font-weight: 800; margin-bottom: .15rem;}
    .subtitle {font-size: 1rem; color: #4b5563; margin-bottom: 1.25rem;}
    .metric-card {border: 1px solid #d1d5db; border-radius: 14px; padding: 14px; background: #ffffff;}
    .metric-label {font-size: .85rem; color: #374151; font-weight: 700;}
    .metric-value {font-size: 1.8rem; font-weight: 900; color: #dc2626; line-height: 1.15;}
    .input-note {font-size: .85rem; color: #6b7280; margin-top: -.4rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Culvert SET Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Only type in the green boxes. The grey values calculate automatically from the spreadsheet logic.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Green Input Boxes")
    pipe_size = st.number_input('PIPE SIZE in inches', min_value=1.0, max_value=144.0, value=18.0, step=1.0)
    slope_ratio = st.number_input('SLOPE RATIO, 4:1 or 6:1', min_value=1.0, max_value=20.0, value=4.0, step=1.0)
    st.caption('Cover is fixed at 6 inches, matching the spreadsheet example.')

cover = 6.0
size_plus_cover = pipe_size + cover
set_length = size_plus_cover * slope_ratio / 12
flat_spot = pipe_size + 12
upstream = 3
downstream = 2

def fmt_number(value, decimals=2):
    if abs(value - round(value)) < 0.000001:
        return str(int(round(value))) if decimals == 0 else f"{value:.2f}"
    return f"{value:.{decimals}f}"

col1, col2 = st.columns([1.05, 1.6], gap="large")

with col1:
    st.subheader("Spreadsheet-style calculation")
    st.markdown("""
<table style="border-collapse:collapse;width:100%;font-size:16px;text-align:center;">
<tr>
<th style="background:#ffff00;border:1px solid #111;padding:10px;">PIPE&quot;</th>
<th style="background:#ffff00;border:1px solid #111;padding:10px;">COVER</th>
<th style="background:#ffff00;border:1px solid #111;padding:10px;">SIZE + Cover</th>
</tr>
<tr>
<td style="background:#39ff14;border:1px solid #111;padding:12px;font-weight:900;font-size:22px;">{pipe}</td>
<td style="background:#d9d9d9;border:1px solid #111;padding:12px;color:red;font-weight:800;">{cover}</td>
<td style="background:#d9d9d9;border:1px solid #111;padding:12px;color:red;font-weight:800;">{size_plus_cover}</td>
</tr>
<tr>
<th style="background:#00e5ee;border:1px solid #111;padding:10px;">4:1 or 6:1</th>
<th style="background:#00e5ee;border:1px solid #111;padding:10px;">SET Length</th>
<th style="background:#00e5ee;border:1px solid #111;padding:10px;">DIA + 12&quot;</th>
</tr>
<tr>
<td style="background:#39ff14;border:1px solid #111;padding:12px;font-weight:900;font-size:22px;">{ratio}</td>
<td style="background:#d9d9d9;border:1px solid #111;padding:12px;color:red;font-weight:800;">{set_length}</td>
<td style="background:#d9d9d9;border:1px solid #111;padding:12px;color:red;font-weight:800;">{flat_spot}</td>
</tr>
</table>
""".format(
        pipe=fmt_number(pipe_size, 0),
        cover=fmt_number(cover, 0),
        size_plus_cover=fmt_number(size_plus_cover, 0),
        ratio=fmt_number(slope_ratio, 2),
        set_length=fmt_number(set_length, 2),
        flat_spot=fmt_number(flat_spot, 0),
    ), unsafe_allow_html=True)

    st.write("")
    a, b = st.columns(2)
    with a:
        st.markdown(f'<div class="metric-card"><div class="metric-label">E30 SET Length</div><div class="metric-value">{fmt_number(set_length, 2)}</div><div>feet</div></div>', unsafe_allow_html=True)
    with b:
        st.markdown(f'<div class="metric-card"><div class="metric-label">H31 / P33 Flat Spot</div><div class="metric-value">{fmt_number(flat_spot, 0)}</div><div>inches</div></div>', unsafe_allow_html=True)

with col2:
    st.subheader("Dynamic illustration")
    svg = f"""
<svg viewBox="0 0 920 560" width="100%" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowRed" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#dc2626"/></marker>
    <marker id="arrowBlack" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#111"/></marker>
    <pattern id="pipeLines" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="#9ca3af" stroke-width="1"/></pattern>
  </defs>

  <text x="20" y="38" fill="#dc2626" font-size="22" font-weight="800">DO NOT TYPE IN GREY BOXES</text>
  <rect x="15" y="48" width="850" height="18" fill="#d9d9d9"/>

  <line x1="150" y1="230" x2="540" y2="285" stroke="#111" stroke-width="5"/>
  <line x1="150" y1="285" x2="540" y2="285" stroke="#111" stroke-width="5"/>
  <line x1="150" y1="215" x2="150" y2="285" stroke="#ef4444" stroke-dasharray="6 5" stroke-width="2"/>
  <line x1="540" y1="240" x2="540" y2="315" stroke="#ef4444" stroke-dasharray="6 5" stroke-width="2"/>

  <line x1="70" y1="235" x2="140" y2="245" stroke="#111" stroke-width="2.5" marker-end="url(#arrowBlack)"/>
  <text x="28" y="215" font-size="22" fill="#111" font-weight="700">6:1 - 4:1</text>
  <text x="62" y="248" font-size="24" fill="#111">{fmt_number(slope_ratio, 2)}</text>

  <line x1="152" y1="258" x2="530" y2="310" stroke="#ef4444" stroke-width="3" marker-end="url(#arrowRed)"/>
  <text x="310" y="280" font-size="24" fill="#ef4444" font-weight="800">{fmt_number(set_length, 2)}</text>
  <text x="310" y="306" font-size="18" fill="#111">FEET</text>

  <rect x="540" y="285" width="190" height="36" fill="none" stroke="#ef4444" stroke-width="5"/>
  <line x1="552" y1="312" x2="718" y2="312" stroke="#ef4444" stroke-width="3" marker-start="url(#arrowRed)" marker-end="url(#arrowRed)"/>
  <text x="620" y="300" font-size="22" fill="#ef4444" font-weight="900">{fmt_number(flat_spot, 0)}</text>
  <text x="585" y="338" font-size="18" fill="#111">INCHES</text>
  <rect x="735" y="285" width="135" height="62" fill="#ffff00" stroke="#ef4444" stroke-dasharray="6 4" stroke-width="2"/>
  <text x="745" y="306" font-size="20" fill="#111">UPSTREAM 3'</text>
  <text x="745" y="332" font-size="20" fill="#111">DOWNSTREAM 2'</text>

  <g transform="translate(470,70) rotate(30)">
    <rect x="0" y="0" width="360" height="95" fill="white" stroke="#222" stroke-width="2"/>
    <ellipse cx="180" cy="47" rx="105" ry="32" fill="url(#pipeLines)" stroke="#222" stroke-width="2"/>
    <ellipse cx="5" cy="47" rx="43" ry="47" fill="url(#pipeLines)" stroke="#222" stroke-width="2"/>
  </g>
  <g transform="translate(710,300)">
    <polygon points="0,0 105,0 145,35 40,35" fill="white" stroke="#dc2626" stroke-width="3"/>
    <polygon points="105,0 145,35 145,90 105,55" fill="white" stroke="#dc2626" stroke-width="3"/>
    <polygon points="0,0 40,35 40,90 0,55" fill="white" stroke="#dc2626" stroke-width="3"/>
    <line x1="40" y1="35" x2="145" y2="35" stroke="#dc2626" stroke-width="3"/>
  </g>

  <line x1="535" y1="285" x2="710" y2="300" stroke="#dc2626" stroke-width="2" marker-end="url(#arrowRed)"/>
  <line x1="790" y1="335" x2="875" y2="335" stroke="#dc2626" stroke-width="3" marker-start="url(#arrowRed)" marker-end="url(#arrowRed)"/>
  <text x="735" y="395" font-size="21" fill="#dc2626" font-weight="900">FLAT</text>
  <text x="735" y="421" font-size="21" fill="#dc2626" font-weight="900">SPOT</text>
  <text x="817" y="397" font-size="22" fill="#dc2626" font-weight="900">{fmt_number(flat_spot, 0)}</text>
  <text x="800" y="424" font-size="22" fill="#dc2626" font-weight="900">INCHES</text>

  <rect x="20" y="460" width="880" height="78" rx="12" fill="#f9fafb" stroke="#d1d5db"/>
  <text x="40" y="492" font-size="18" fill="#111" font-weight="800">Formulas</text>
  <text x="40" y="522" font-size="17" fill="#111">Size + Cover = Pipe Size + 6   •   SET Length = (Size + Cover × Ratio) ÷ 12   •   DIA + 12 = Pipe Size + 12</text>
</svg>
"""
    st.markdown(svg, unsafe_allow_html=True)

st.divider()
st.caption("Created by Nick Nabholz spreadsheet logic. Converted to a no-hosted-assets Streamlit web app.")
