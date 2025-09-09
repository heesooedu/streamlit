import streamlit as st
import pandas as pd

# --- Streamlit UI 설정 ---
st.set_page_config(layout="wide")
st.title("🚀 GlowScript + Streamlit 통합 물리 시뮬레이터")

# 사이드바에서 파라미터 입력받기
with st.sidebar:
    st.header("시뮬레이션 조건 설정")
    v0 = st.slider("초기 속도 (m/s)", 10, 100, 50)
    angle = st.slider("발사 각도 (도)", 10, 80, 45)
    g = st.number_input("중력 가속도 (m/s^2)", value=9.8)

# --- GlowScript 코드 동적 생성 ---
# 입력받은 파라미터를 f-string을 이용해 VPython 코드에 삽입
glowscript_code = f"""
from vpython import *

scene.width = 600
scene.height = 400

ball = sphere(pos=vector(0,0,0), radius=0.5, color=color.red, make_trail=True)
ground = box(pos=vector(0,-1,0), size=vector(100,0.5,10))

g = {g}
v0 = {v0}
theta = radians({angle})

ball.v = vector(v0*cos(theta), v0*sin(theta), 0)
ball.m = 1

dt = 0.01
t = 0

print("t, x, y, vx, vy") # CSV 헤더 출력

while ball.pos.y >= 0:
    rate(100)
    F = vector(0, -ball.m*g, 0)
    ball.v = ball.v + F/ball.m * dt
    ball.pos = ball.pos + ball.v * dt
    t = t + dt
    print(f"{{t:.2f}}, {{ball.pos.x:.2f}}, {{ball.pos.y:.2f}}, {{ball.v.x:.2f}}, {{ball.v.y:.2f}}")
"""

# HTML로 감싸서 iframe 생성
# GlowScript 라이브러리를 로드하고 코드를 실행시키는 HTML 템플릿
html_template = f"""
<div id="glowscript" class="glowscript">
<script type="text/x-glowscript">
{glowscript_code}
</script>
</div>
"""

# --- 화면 레이아웃 구성 ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("GlowScript 3D 시뮬레이션")
    # `st.components.v1.html`을 사용해 GlowScript 렌더링
    st.components.v1.html(html_template, height=450)

with col2:
    st.subheader("데이터 분석 및 시각화")
    st.write("시뮬레이션이 끝나면 왼쪽 화면 아래에 나타나는 데이터를 복사해서 아래 칸에 붙여넣으세요.")
    
    # 데이터 붙여넣기 영역
    pasted_data = st.text_area("데이터 붙여넣기", height=200, placeholder="t, x, y, vx, vy\\n0.01, 0.35, 0.35, 35.35, 35.30\\n...")
    
    if st.button("📈 데이터 분석 실행"):
        if pasted_data:
            from io import StringIO
            df = pd.read_csv(StringIO(pasted_data))
            
            st.write("### 시간에 따른 위치(x, y) 그래프")
            st.line_chart(df, x='t', y=['x', 'y'])
            
            st.write("### 시간에 따른 속도(vx, vy) 그래프")
            st.line_chart(df, x='t', y=['vx', 'vy'])

            # GlowScript에서는 보기 힘든, x-y 관계 그래프 (포물선 궤적)
            st.write("### X-Y 궤적 그래프")
            st.altair_chart(
                {
                    "data": {"values": df.to_dict("records")},
                    "mark": "line",
                    "encoding": {
                        "x": {"field": "x", "type": "quantitative"},
                        "y": {"field": "y", "type": "quantitative"}
                    }
                }, use_container_width=True
            )
        else:
            st.warning("데이터를 먼저 붙여넣어 주세요.")
