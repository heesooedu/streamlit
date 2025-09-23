import streamlit as st

st.set_page_config(page_title="VPython in Streamlit", layout="wide")
st.title("GlowScript VPython × Streamlit Demo")

col1, col2, col3 = st.columns(3)
with col1:
    rot_speed = st.slider("회전 속도 (rad/s)", 0.0, 0.2, 0.03, 0.005)
with col2:
    box_size = st.slider("박스 크기", 0.1, 3.0, 1.0, 0.1)
with col3:
    bg_white = st.toggle("배경: 흰색", value=True)

bg_color = "color.white" if bg_white else "vec(0.1,0.1,0.12)"

html = f"""
<div id="glowscript" class="glowscript"></div>

<!-- GlowScript 필수 라이브러리 (버전표시 없는 경로) -->
<script src="https://www.glowscript.org/lib/glow.min.js"></script>
<script src="https://www.glowscript.org/lib/RSrun.min.js"></script>
<script src="https://www.glowscript.org/lib/RScompile.min.js"></script>

<!-- 컨테이너 지정: 순정 JS -->
<script>
  window.__context = {{ glowscript_container: document.getElementById("glowscript") }};
</script>

<!-- VPython 코드 -->
<script type="text/python">
from vpython import *
scene.width = 960
scene.height = 540
scene.background = {bg_color}
b = box(length={box_size}, height={box_size}, width={box_size}, color=color.red)
arrow(pos=vector(0,0,0), axis=vector(2,0,0), color=color.red)
arrow(pos=vector(0,0,0), axis=vector(0,2,0), color=color.green)
arrow(pos=vector(0,0,0), axis=vector(0,0,2), color=color.blue)
while True:
    rate(60)
    b.rotate(angle={rot_speed}, axis=vec(0,1,0))
</script>
"""
st.components.v1.html(html, height=600)
