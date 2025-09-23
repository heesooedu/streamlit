import streamlit as st
from string import Template

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

# 너의 리포 경로 (브랜치가 master면 @master 로 바꾸기)
BASE = "https://cdn.jsdelivr.net/gh/heesooedu/streamlit@main/static/glowscript"

html_tpl = Template(r"""
<div id="glowscript" class="glowscript" style="outline:none;"></div>

<!-- 1) jQuery (네가 올린 파일명 그대로, 같은 폴더에 있다고 가정) -->
<script src="${BASE}/jquery.min.js"></script>
<script src="${BASE}/jquery-ui.custom.min.js"></script>

<!-- 2) GlowScript가 그릴 대상 지정 (jQuery 필요) -->
<script>
  window.__context = { glowscript_container: $("#glowscript") };
</script>

<!-- 3) GlowScript 핵심 라이브러리 (네 리포의 정확한 파일명 사용) -->
<script src="${BASE}/glow.3.2.min.js"></script>
<script src="${BASE}/RSrun.3.2.min.js"></script>
<script src="${BASE}/RScompiler.3.2.min.js"></script>

<!-- 4) VPython 코드 (첫 줄 헤더 필수) -->
<script type="text/python">
GlowScript 3.2 VPython
from vpython import *

scene.width = 960
scene.height = 540
scene.background = ${bg_color}

box_size  = ${box_size}
rot_speed = ${rot_speed}

b = box(length=box_size, height=box_size, width=box_size, color=color.red)

# 좌표축
arrow(pos=vector(0,0,0), axis=vector(2,0,0), color=color.red)
arrow(pos=vector(0,0,0), axis=vector(0,2,0), color=color.green)
arrow(pos=vector(0,0,0), axis=vector(0,0,2), color=color.blue)

while True:
    rate(60)
    b.rotate(angle=rot_speed, axis=vec(0,1,0))
</script>
""")

html = html_tpl.safe_substitute(
    BASE=BASE,
    bg_color=bg_color,
    box_size=box_size,
    rot_speed=rot_speed,
)

st.components.v1.html(html, height=620)

st.caption(
    "Network 탭에서 jquery.min.js / jquery-ui.custom.min.js / glow.3.2.min.js / "
    "RSrun.3.2.min.js / RScompiler.3.2.min.js 가 모두 200 OK인지 확인하세요. "
    "브랜치가 master면 BASE의 @main을 @master로 바꾸세요. "
    "jsDelivr 캐시가 느리면 URL 끝에 ?v=1 붙이고 강력 새로고침(Ctrl+F5)."
)
