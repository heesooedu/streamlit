import streamlit as st

# =========================
# Streamlit × GlowScript VPython Demo (heesooedu/streamlit)
# =========================
st.set_page_config(page_title="VPython in Streamlit", layout="wide")
st.title("GlowScript VPython × Streamlit Demo")

# ---- Controls ----
col1, col2, col3 = st.columns(3)
with col1:
    rot_speed = st.slider("회전 속도 (rad/step)", min_value=0.0, max_value=0.2, value=0.03, step=0.005)
with col2:
    box_size = st.slider("박스 크기", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
with col3:
    bg_white = st.toggle("배경: 흰색", value=True)

bg_color = "color.white" if bg_white else "vec(0.1,0.1,0.12)"

# ---- HTML with GlowScript embed ----
# We load JS libraries from your GitHub via jsDelivr first (main → master),
# then fall back to the official vpython/glowscript repo.
html = f"""
<div id="glowscript" class="glowscript"></div>

<script>
// --- tiny script loader with fallbacks ---
function loadScript(u) {{
  return new Promise((res, rej) => {{
    const s = document.createElement('script');
    s.src = u;
    s.async = true;
    s.onload = () => res(u);
    s.onerror = () => rej(u);
    document.head.appendChild(s);
  }});
}}
async function tryLoad(list) {{
  for (const u of list) {{
    try {{
      await loadScript(u);
      return u;
    }} catch (e) {{}}
  }}
  throw new Error("모든 후보 URL이 실패했습니다: " + list.join(", "));
}}

(async () => {{
  // Your repo (main → master), then official repo
  const B_USER_MAIN   = "https://cdn.jsdelivr.net/gh/heesooedu/streamlit@main/static/glowscript/";
  const B_USER_MASTER = "https://cdn.jsdelivr.net/gh/heesooedu/streamlit@master/static/glowscript/";
  const B_OFFICIAL    = "https://cdn.jsdelivr.net/gh/vpython/glowscript@master/lib/";

  // Some archives name files as RScompile..., 일부는 RScompiler... 로 배포되기도 함
  // (네 리포에 올라간 '정확한' 파일명이 먼저 시도됨)
  const glowCandidates = [
    B_USER_MAIN + "glow.3.2.min.js",
    B_USER_MAIN + "glow.min.js",
    B_USER_MASTER + "glow.3.2.min.js",
    B_USER_MASTER + "glow.min.js",
    B_OFFICIAL + "glow.3.2.min.js",
    B_OFFICIAL + "glow.min.js",
  ];

  const rsrunCandidates = [
    B_USER_MAIN + "RSrun.3.2.min.js",
    B_USER_MAIN + "RSrun.min.js",
    B_USER_MASTER + "RSrun.3.2.min.js",
    B_USER_MASTER + "RSrun.min.js",
    B_OFFICIAL + "RSrun.3.2.min.js",
    B_OFFICIAL + "RSrun.min.js",
  ];

  const rscompileCandidates = [
    // 두 표기 모두 시도
    B_USER_MAIN + "RScompile.3.2.min.js",
    B_USER_MAIN + "RScompiler.3.2.min.js",
    B_USER_MAIN + "RScompile.min.js",
    B_USER_MAIN + "RScompiler.min.js",
    B_USER_MASTER + "RScompile.3.2.min.js",
    B_USER_MASTER + "RScompiler.3.2.min.js",
    B_USER_MASTER + "RScompile.min.js",
    B_USER_MASTER + "RScompiler.min.js",
    B_OFFICIAL + "RScompile.3.2.min.js",
    B_OFFICIAL + "RScompile.min.js",
  ];

  await tryLoad(glowCandidates);
  await tryLoad(rsrunCandidates);
  await tryLoad(rscompileCandidates);

  // Tell GlowScript where to render
  window.__context = {{ glowscript_container: document.getElementById("glowscript") }};
}})();
</script>

<!-- VPython code -->
<script type="text/python">
from vpython import *
scene.width = 960
scene.height = 540
scene.background = {bg_color}

box_size = {box_size}
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
    "네트워크 탭에서 glow / RSrun / RScompile(또는 RScompiler) 3개가 모두 200 OK인지 확인하세요. "
    "리포 기본 브랜치가 master면 코드 상단의 경로가 자동으로 master도 시도합니다. "
    "캐시 문제시 URL 끝에 ?v=1 추가 후 강력 새로고침(Ctrl+F5)."
)
