import streamlit as st
import streamlit.components.v1 as components
from textwrap import dedent

st.set_page_config(page_title="VPython in Streamlit", layout="wide")

st.title("VPython ▶ Streamlit (GlowScript 런타임 직접 임베드)")

default_code = dedent("""\
from vpython import *

scene.width  = 640
scene.height = 400
scene.background = color.white

# 데모: 큐브와 회전
b = box(pos=vector(0,0,0), size=vector(1,1,1), color=color.red)
w = 2*pi/3  # rad/s

while True:
    rate(60)
    b.rotate(angle=w*0.016, axis=vector(0,1,0))
""")

user_code = st.text_area(
    "여기에 VPython 코드를 입력하세요 (GlowScript/VPython 문법)",
    value=default_code,
    height=300,
)

col_run, col_clear = st.columns([1,1])
run_clicked = col_run.button("▶ Run")
clear_clicked = col_clear.button("🧹 Clear")

if run_clicked and user_code.strip():
    # HTML 템플릿: GlowScript CDN을 불러와서 text/python 스크립트를 실행
    html_tpl = """
    <div id="glowscript" class="glowscript" style="outline:none;"></div>

    <script src="https://www.glowscript.org/lib/jquery/2.1/jquery.min.js"></script>
    <script src="https://www.glowscript.org/lib/jquery/2.1/jquery-ui.custom.min.js"></script>

    <!-- GlowScript / RapydScript 런타임 -->
    <script src="https://www.glowscript.org/package/glow.3.2.min.js"></script>
    <script src="https://www.glowscript.org/package/RScompiler.3.2.min.js"></script>
    <script src="https://www.glowscript.org/package/RSrun.3.2.min.js"></script>

    <script>
      // GlowScript가 쓸 컨테이너 바인딩
      window.__context = {{ glowscript_container: $("#glowscript").removeAttr("id") }};
    </script>

    <script type="text/python">
    {code}
    </script>

    <style>
      /* Streamlit의 스크롤 영역에서 캔버스가 잘 보이도록 여백 */
      body {{ margin:0; padding:0; }}
    </style>
    """

    # {code} 자리에 사용자 코드를 그대로 삽입
    html = html_tpl.format(code=user_code)

    # components.html 로 즉시 렌더 (height는 필요에 맞게 조절)
    components.html(html, height=520, scrolling=True)

elif clear_clicked:
    st.info("출력을 지웠습니다. 코드를 수정한 뒤 ▶ Run을 누르세요.")
else:
    st.caption("도움말: Run을 누르면 위 코드가 즉시 컴파일·실행되어 아래에 3D 캔버스가 나타납니다.")
