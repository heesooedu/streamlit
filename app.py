import streamlit as st

st.set_page_config(page_title="VPython in Streamlit", layout="wide")
st.title("GlowScript VPython × Streamlit Demo")

# ---- 위젯 (3열) ----
col1, col2, col3 = st.columns(3)

with col1:
    rot_speed = st.slider("회전 속도 (rad/s)", min_value=0.0, max_value=0.2, value=0.03, step=0.005)

with col2:
    box_size = st.slider("박스 크기", min_value=0.1, max_value=3.0, value=1.0, step=0.1)

with col3:
    bg_white = st.toggle("배경: 흰색", value=True)

bg_color = "color.white" if bg_white else "vec(0.1,0.1,0.12)"

# ---- GlowScript + VPython 임베드 ----
html = f"""
<div id="glowscript" class="glowscript"></div>
<!-- 필수 라이브러리 -->
<script src="https://www.glowscript.org/lib/glow.3.2.min.js"></script>
<script src="https://www.glowscript.org/lib/RSrun.3.2.min.js"></script>
<script src="https://www.glowscript.org/lib/RScompile.3.2.min.js"></script>

<!-- VPython 코드 -->
<script type="text/python">
from vpython import *
scene.width = 960
scene.height = 540
scene.background = {bg_color}

box_size = {box_size}
rot_speed = {rot_speed}

b = box(length=box_size, height=box_size, width=box_size, color=color.red)

# 축 표시
arrow(pos=vector(0,0,0), axis=vector(2,0,0), color=color.red)
arrow(pos=vector(0,0,0), axis=vector(0,2,0), color=color.green)
arrow(pos=vector(0,0,0), axis=vector(0,0,2), color=color.blue)

while True:
    rate(60)
    b.rotate(angle=rot_speed, axis=vec(0,1,0))
</script>
"""

st.components.v1.html(html, height=580)
