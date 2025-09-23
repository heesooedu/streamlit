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

BASE = "https://cdn.jsdelivr.net/gh/heesooedu/streamlit@main/static/glowscript"

html = f"""
<div id="glowscript" class="glowscript" style="outline:none;"></div>

<script>
// ---- 순차 로더 (필수: jQuery → GlowScript) ----
function loadScript(u) {{
  return new Promise((res, rej) => {{
    const s = document.createElement('script');
    s.src = u;
    s.async = false; // 로드 순서 보장
    s.onload = () => res(u);
    s.onerror = () => rej(u);
    document.head.appendChild(s);
  }});
}}
async function tryLoad(list) {{
  for (const u of list) {{
    try {{ await loadScript(u); return u; }} catch(e) {{}}
  }}
  throw new Error("모든 후보 URL 실패: " + list.join(", "));
}}

(async () => {{
  const B = "{BASE}/";

  // 1) jQuery (네가 올린 실제 파일명에 맞춰 후보를 시도)
  await tryLoad([B+"jquery/jquery.min.js", B+"jquery/3.1/jquery.min.js"]);
  await tryLoad([B+"jquery/jquery-ui.custom.min.js", B+"jquery/3.1/jquery-ui.custom.min.js"]);

  // 2) GlowScript 핵심 (네 리포의 정확한 파일명 사용)
  await loadScript(B+"glow.3.2.min.js");
  await loadScript(B+"RSrun.3.2.min.js");
  await loadScript(B+"RScompiler.3.2.min.js");

  // 3) GlowScript가 그릴 대상 지정 (jQuery 사용)
  window.__context = {{ glowscript_container: $("#glowscript") }};
})();
</script>

<!-- VPython code: 헤더 필수 -->
<script type="text/python">
GlowScript 3.2 VPython
from vpython import *

scene.width = 960
scene.height = 540
scene.background = {bg_color}

box_size  = {box_size}
rot_speed = {rot_speed}

b = box(length=box_size, height=box_size, width=box_size, color=color.red)

# axes
arrow(pos=vector(0,0,0), axis=vector(2,0,0), color=color.red)
arrow(pos=vector(0,0,0), axis=vector(0,2,0), color=color.green)
arrow(pos=vector(0,0,0), axis=vector(0,0,2), color=color.blue)

while True:
    rate(60)
    b.rotate(angle=rot_speed, axis=vec(0,1,0))
</script>
"""

st.components.v1.html(html, height=620)
st.caption(
    "Network 탭에서 jquery.min.js / jquery-ui.custom.min.js / glow.3.2.min.js / RSrun.3.2.min.js / RScompiler.3.2.min.js 가 모두 200 OK인지 확인하세요. "
    "경로가 다르면 BASE 하위 폴더만 맞춰 주세요."
)
