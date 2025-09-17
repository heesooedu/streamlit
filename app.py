# app.py — Streamlit × GlowScript (인라인 라이브러리 + 안전한 문자열 처리)
import streamlit as st
from datetime import datetime
import math
import os

st.set_page_config(page_title="VPython × Streamlit (Plan A, Inline Libs)", layout="wide")

# 리포지토리에 동봉해야 할 파일 (static/glowscript/ 아래)
#   jquery.min.js
#   jquery-ui.custom.min.js
#   glow.3.2.min.js
#   RSrun.3.2.min.js
#   RScompile.3.2.min.js

# 새 코드: app.py 위치 기준으로 후보 경로를 검색해 자동 선택
ROOT = os.path.dirname(os.path.abspath(__file__))
CANDIDATES = [
    os.path.join(ROOT, "static", "glowscript"),             # 일반 구조
    os.path.join(ROOT, "streamlit", "static", "glowscript") # 지금 네 저장소 구조
]

LIB_DIR = None
for p in CANDIDATES:
    if os.path.isdir(p):
        LIB_DIR = p
        break
if LIB_DIR is None:
    # 못 찾으면 기본값으로 두고, 아래 에러 패널이 경로 누락 안내를 띄움
    LIB_DIR = CANDIDATES[0]

REQUIRED_LIBS = [
    "jquery.min.js",
    "jquery-ui.custom.min.js",
    "glow.3.2.min.js",
    "RSrun.3.2.min.js",
    "RScompile.3.2.min.js",
]

def read_js_or_none(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

def _libs_fingerprint(lib_dir:str):
    fp = []
    for fname in REQUIRED_LIBS:
        p = os.path.join(lib_dir, fname)
        try:
            fp.append((fname, os.path.getmtime(p)))
        except FileNotFoundError:
            fp.append((fname, None))
    return tuple(fp)

@st.cache_data(show_spinner=False)
def load_libs_inline(lib_dir:str, fingerprint:tuple):
    missing = []
    blocks = []
    for fname in REQUIRED_LIBS:
        p = os.path.join(lib_dir, fname)
        try:
            with open(p, "r", encoding="utf-8") as f:
                blocks.append(f"<script>{f.read()}</script>")
        except Exception:
            missing.append(p)
    return "\n".join(blocks), missing

def build_sim_html(g: float, v0: float, angle_deg: int, mode: str = "projectile") -> str:
    """mode='hello'면 빨간 박스, 'projectile'이면 투사체 시뮬"""
    libs_html, missing = load_libs_inline(LIB_DIR, _libs_fingerprint(LIB_DIR))

    head = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
  html, body {{ width:100%; height:100%; margin:0; padding:0; }}
  #glowscript {{ width:100%; height:100%; }}
  #err {{
    position:absolute; left:8px; bottom:8px; right:8px;
    background:#fff3cd; color:#663c00; font:12px/1.4 sans-serif;
    border:1px solid #ffe69c; padding:6px; display:none; z-index:9999;
  }}
</style>
{libs_html}
</head>
<body>
<div id="glowscript"></div>
<div id="err"></div>
<script>
  // GlowScript 컨테이너 지정
  window.__context = {{ glowscript_container: $("#glowscript") }};
  // 에러 패널
  (function(){{
    var p = document.getElementById('err');
    function show(msg){{ p.style.display='block'; p.textContent += (p.textContent?'\\n':'') + msg; }}
    window.onerror = function (msg, src, line, col, err) {{
      show("[Error] " + msg + " @" + src + ":" + line + ":" + col);
    }};
    ['log','warn','error'].forEach(function(k){{
      var orig = console[k];
      console[k] = function(){{
        try {{ show("[console."+k+"] " + Array.from(arguments).join(" ")); }} catch(e){{}}
        if (orig) orig.apply(console, arguments);
      }};
    }});
  }})();
</script>
"""

    if missing:
        # 라이브러리 누락 시 안내만 표시
        missing_list = "\\n".join(missing)
        guide = f"""
<script>
  var p = document.getElementById('err');
  p.style.display='block';
  p.textContent = "GlowScript 라이브러리 파일을 찾을 수 없습니다.\\n" +
                  "다음 파일을 리포지토리에 추가하세요:\\n{missing_list}";
</script>
"""
        tail = """
<script type="text/python">
from vpython import *
# 라이브러리 누락으로 실행 불가
</script>
</body>
</html>
"""
        return head + guide + tail

    # ⚠️ 중첩 f-string 문제 방지: 바깥은 .format 사용, 안쪽 f-string 중괄호는 {{ }}
    if mode == "hello":
        pycode = """
from vpython import *
scene.title = "Hello GlowScript"
scene.background = color.white
box(color=color.red)
"""
    else:
        pycode = """
from vpython import *
g = {g}
v0 = {v0}
angle_deg = {angle_deg}

scene.title = "Projectile (GlowScript VPython)"
scene.background = color.white
scene.width = 700
scene.height = 450
scene.center = vector(15,5,0)

ground = box(pos=vector(15,-0.05,0), size=vector(60,0.1,4), color=vector(0.9,0.9,0.9))
curve(pos=[vector(0,0,0), vector(60,0,0)], color=color.gray(0.7))
curve(pos=[vector(0,0,0), vector(0,15,0)], color=color.gray(0.7))

ball = sphere(pos=vector(0,0,0), radius=0.3, color=color.blue, make_trail=True, trail_color=color.cyan)
angle = radians(angle_deg)
v = vector(v0*cos(angle), v0*sin(angle), 0)
dt = 0.01
t = 0

label(pos=vector(30,14,0), text="측정값(실험)", box=False, height=16, color=color.black)
info = label(pos=vector(30,12,0), text="", box=False, height=14, color=color.black)

while ball.pos.y >= 0:
    rate(200)
    v = v + vector(0, -g, 0)*dt
    ball.pos = ball.pos + v*dt
    t += dt

ball.pos = ball.pos - v*dt
t -= dt
tau = ball.pos.y/(-v.y) if v.y < 0 else 0.0
ball.pos = ball.pos + v*tau
t += tau

range_est = ball.pos.x
time_of_flight = t
hmax_est = (v0**2 * sin(angle)**2) / (2*g)

info.text = f"사거리 ≈ {{range_est:.2f}} m\\n비행시간 ≈ {{time_of_flight:.2f}} s\\n이론 최대높이 ≈ {{hmax_est:.2f}} m"
scene.center = vector(max(15, range_est/2), 5, 0)
""".format(g=g, v0=v0, angle_deg=angle_deg)

    tail = """
<script type="text/vpython">
# 위에서 구성한 pycode가 이 자리에 삽입됩니다.
</script>
</body>
</html>
"""
    return head + tail.replace("# 위에서 구성한 pycode가 이 자리에 삽입됩니다.", pycode)

# ----------------------- UI -----------------------
st.title("GlowScript VPython × Streamlit (Plan A: Inline Libraries)")

col_ctrl, col_sim = st.columns([1, 2], gap="large")

with col_ctrl:
    st.subheader("실험 설정")
    g = st.slider("중력 가속도 g (m/s²)", min_value=1.0, max_value=20.0, value=9.8, step=0.1)
    v0 = st.slider("초기속도 v0 (m/s)", min_value=1.0, max_value=50.0, value=20.0, step=0.5)
    angle = st.slider("발사각 (deg)", min_value=0, max_value=90, value=45, step=1)

    st.markdown("---")
    st.subheader("실험 기록")
    if "runs" not in st.session_state:
        st.session_state.runs = []

    if st.button("현재 설정을 기록에 추가"):
        st.session_state.runs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "g": float(g), "v0": float(v0), "angle_deg": int(angle),
        })

    if st.session_state.runs:
        import pandas as pd
        st.dataframe(pd.DataFrame(st.session_state.runs), use_container_width=True, hide_index=True)
        csv = pd.DataFrame(st.session_state.runs).to_csv(index=False).encode("utf-8-sig")
        st.download_button("CSV로 다운로드", data=csv, file_name="runs.csv", mime="text/csv")
    else:
        st.info("아직 기록이 없습니다. 파라미터를 조정하고 '현재 설정을 기록에 추가'를 누르세요.")

with col_sim:
    st.subheader("시뮬레이션")
    # 처음엔 "hello"로 바꿔 빨간 박스 확인 -> 되면 "projectile"로 변경
    html = build_sim_html(g=g, v0=v0, angle_deg=angle, mode="projectile")
    st.components.v1.html(html, height=520, scrolling=False)  # key 인자 쓰지 마세요

st.markdown("---")

# 간단 이론값 메트릭
st.subheader("간단 분석 (공기저항 무시 이론값)")
angle_rad = math.radians(angle)
range_theory = (v0**2 * math.sin(2*angle_rad)) / g if g > 0 else float('nan')
hmax_theory = (v0**2 * (math.sin(angle_rad)**2)) / (2*g) if g > 0 else float('nan')

c1, c2 = st.columns(2)
with c1:
    st.metric("이론 사거리 (m)", f"{range_theory:.2f}")
with c2:
    st.metric("이론 최대높이 (m)", f"{hmax_theory:.2f}")

st.caption("※ 위 메트릭은 이론식(공기저항 무시), 화면 라벨은 시뮬레이션 추정치입니다.")
st.caption(f"LIB_DIR = {LIB_DIR}")

