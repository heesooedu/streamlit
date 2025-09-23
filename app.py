import streamlit as st
from string import Template

st.set_page_config(page_title="VPython in Streamlit", layout="wide")
st.title("GlowScript VPython × Streamlit — Minimal DOM init")

# ---- Controls ----
col1, col2, col3 = st.columns(3)
with col1:
    rot_speed = st.slider("회전 속도 (rad/step)", 0.0, 0.2, 0.03, 0.005)
with col2:
    box_size = st.slider("박스 크기", 0.1, 3.0, 1.0, 0.1)
with col3:
    bg_white = st.toggle("배경: 흰색", value=True)

bg_color = "color.white" if bg_white else "vec(0.1,0.1,0.12)"

# 네 리포(브랜치가 master면 @master로 바꾸기)
BASE = "https://cdn.jsdelivr.net/gh/heesooedu/streamlit@main/static/glowscript"

html_tpl = Template(r"""
<div id="glowscript" class="glowscript" style="outline:none;">[loading GlowScript...]</div>

<!-- 1) (선택) jQuery: 일부 버전의 glow가 jQuery를 참조하므로 최소본만 -->
<script src="${BASE}/jquery.min.js"></script>

<!-- 2) 컨테이너를 '순수 DOM 노드'로 지정 -->
<script>
  // jQuery 객체가 아니라 '진짜 DOM 노드'를 넘깁니다.
  window.__context = { glowscript_container: document.getElementById("glowscript") };
  console.log("Glow container prepared:", window.__context.glowscript_container);
</script>

<!-- 3) GlowScript 핵심 라이브러리 (순서: glow -> RSrun -> RScompiler) -->
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

<!-- 5) 안전장치: 2초 후에 캔버스가 안 붙었으면 경고를 띄움 -->
<script>
  setTimeout(() => {
    const host = document.getElementById("glowscript");
    const hasCanvas = host && host.querySelector("canvas");
    console.log("Glow post-check, canvas exists?", !!hasCanvas, host);
    if (!hasCanvas) {
      host.innerHTML = "<div style='color:#c00;font-weight:600'>GlowScript 캔버스가 생성되지 않았습니다. 콘솔 에러와 Network를 다시 확인하세요.</div>";
    }
  }, 2000);
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
    "필수 체크: Network에서 jquery.min.js / glow.3.2.min.js / RSrun.3.2.min.js / RScompiler.3.2.min.js 모두 200 OK. "
    "Console에 에러가 없어야 하며, 2초 뒤 'canvas exists? true'가 찍혀야 정상."
)
