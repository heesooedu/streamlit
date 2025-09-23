import streamlit as st
from textwrap import dedent


st.set_page_config(page_title="VPython in Streamlit", layout="wide")
st.title("GlowScript VPython × Streamlit Demo")


# Streamlit 컨트롤(파라미터)
col1, col2, col3 = st.columns(3)
with col1:
rot_speed = st.slider("회전 속도 (rad/s)", 0.0, 0.2, 0.03, 0.005)
with col2:
box_size = st.slider("박스 크기", 0.1, 3.0, 1.0, 0.1)
with col3:
bg_white = st.toggle("배경: 흰색", value=True)


bg_color = "color.white" if bg_white else "vec(0.1,0.1,0.12)"


# GlowScript + VPython을 HTML에 주입
html = f"""
<div id=\"glowscript\" class=\"glowscript\"></div>
<!-- GlowScript 필수 라이브러리 -->
<script src=\"https://www.glowscript.org/lib/glow.3.2.min.js\"></script>
<script src=\"https://www.glowscript.org/lib/RSrun.3.2.min.js\"></script>
<script src=\"https://www.glowscript.org/lib/RScompile.3.2.min.js\"></script>


<!-- VPython 코드 -->
<script type=\"text/python\">
from vpython import *
scene.width = 960
scene.height = 540
scene.background = {bg_color}


box_size = {box_size}
rot_speed = {rot_speed}


# 오브젝트
b = box(length=box_size, height=box_size, width=box_size, color=color.red)


# 축
x = arrow(pos=vector(0,0,0), axis=vector(2,0,0), color=color.red)
y = arrow(pos=vector(0,0,0), axis=vector(0,2,0), color=color.green)
z = arrow(pos=vector(0,0,0), axis=vector(0,0,2), color=color.blue)


# 애니메이션 루프
while True:
rate(60)
b.rotate(angle=rot_speed, axis=vec(0,1,0))
</script>
"""


# 임베딩 (높이는 장면 크기에 맞춰 여유 있게)
st.components.v1.html(html, height=580)


st.markdown(
dedent(
f"""
**Tip**
- 위 슬라이더/토글을 바꾸면 Streamlit이 리런되며 VPython 장면도 즉시 반영됩니다.
- 무한 루프에서는 반드시 `rate(60)`처럼 프레임 제한을 주세요.
- 배포 시 외부 스크립트 로드는 glowscript.org 가용성에 의존합니다. (대안: 자체 호스팅, 아래 README 참조)
"""
)
)
