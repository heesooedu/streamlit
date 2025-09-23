import streamlit as st

st.set_page_config(page_title="VPython in Streamlit", layout="wide")
st.title("GlowScript VPython × Streamlit Demo")

# ---- Controls ----
col1, col2, col3 = st.columns(3)
with col1:
    rot_speed = st.slider("회전 속도 (rad/step)", 0.0, 0.2, 0.03, 0.005)
with col2:
    box_size = st.slider("박스 크기", 0.1, 3.0, 1.0, 0.1)
with col3:
    bg_white = st.toggle("배경: 흰색", value=True)

bg_color = "color.white" if bg_white else "vec(0.1,0.1,0.12)"

# ---- JS base paths ----
USER_BASE = "https://cdn.jsdelivr.net/gh/heesooedu/streamlit@main/static/glowscript"
OFFICIAL  = "https://cdn.jsdelivr.net/gh/vpython/glowscript@master/lib"

# ---- HTML with strict load order ----
html = f"""
<div id="glowscript" class="glowscript" style="outline:none;"></div>

<!-- 1) jQuery 먼저 -->
<script src="{OFFICIAL}/jquery/3.1/jquery.min.js"></script>
<script src="{OFFICIAL}/jquery/3.1/jquery-ui.min.js"></script>

<!-- 2) 컨테이너 지정(jQuery 사용) -->
<script type="text/javascript">
  // jQuery가 준비된 후 컨테이너 지정
  window.__context = {{ glowscript_container: $("#glowscript") }};
</script>

<!-- 3) GlowScript 라이브러리 (네 리포에서) -->
<script src="{USER_BASE}/glow.3.2.min.js"></script>
<script src="{USER_BASE}/RSrun.3.2.min.js"></script>
<script src="{USER_BASE}/RScompiler.3.2.min.js"></script>

<!-- 4) VPython 코드 -->
<script type="text/python">
GlowScript 3.2 VPython  # <-- 이 헤더가 중요합니다
from vpython import *

scene.width  = 960
scene.height = 540
scene.background = {bg_color}

box_size  = {box_size}
rot_speed = {rot_speed}

b = box(length=box_size, height=box_size, width=box_size, color=color.red)

# 좌표축
arrow(pos=vector(0,0,0), axis=vector(2,0,0), color=color.red)
arrow(pos=vector(0,0,0), axis=vector(0,2,0), color=color.green)
arrow(pos=vector(0,0,0), axis=vector(0,0,2), color=color.blue)

while True:
    rate(60)
    b.rotate(angle=rot_speed, axis=vec(0,1,0))
</script>
"""

st.components.v1.html(html, height=620)
st.caption("Network 탭에서 5개(jquery 2개 + glow/RSrun/RScompile(또는 RScompiler)) 모두 200 OK인지 확인하세요.")
