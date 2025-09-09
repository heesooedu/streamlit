import streamlit as st
import pandas as pd
from io import StringIO

# --- 1. 스트림릿 페이지 기본 설정 ---
st.set_page_config(layout="wide")
st.title("🚀 GlowScript + Streamlit 통합 물리 시뮬레이터")
st.write("GlowScript의 3D 시뮬레이션과 Streamlit의 데이터 분석 기능을 결합한 웹 앱입니다.")
st.write("---")

# --- 2. 사이드바에서 시뮬레이션 조건 입력받기 ---
with st.sidebar:
    st.header("⚙️ 시뮬레이션 조건 설정")
    v0 = st.slider("초기 속도 (m/s)", min_value=10, max_value=100, value=50, step=1)
    angle = st.slider("발사 각도 (도)", min_value=10, max_value=80, value=45, step=1)
    g = st.number_input("중력 가속도 (m/s²)", value=9.8, format="%.2f")

# --- 3. VPython(GlowScript) 코드 동적 생성 ---
glowscript_code = f"""
from vpython import *
scene.width = 600
scene.height = 400
ball = sphere(pos=vector(0,0,0), radius=0.5, color=color.red, make_trail=True, trail_color=color.yellow)
ground = box(pos=vector(0,-1,0), size=vector(150,0.5,10), color=color.green)
g = {g}
v0 = {v0}
theta = radians({angle})
ball.v = vector(v0*cos(theta), v0*sin(theta), 0)
ball.m = 1
dt = 0.01
t = 0
print("t, x, y, vx, vy")
while ball.pos.y >= 0:
    rate(100)
    F = vector(0, -ball.m*g, 0)
    ball.v = ball.v + F/ball.m * dt
    ball.pos = ball.pos + ball.v * dt
    t = t + dt
    print(f"{{t:.2f}}, {{ball.pos.x:.2f}}, {{ball.pos.y:.2f}}, {{ball.v.x:.2f}}, {{ball.v.y:.2f}}")
"""

# --- 4. 완전한 HTML 코드 생성 (수정된 최종본) ---
full_html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GlowScript</title>
    <script type="text/javascript" src="https://s3.amazonaws.com/glowscript/py/jquery.min.js"></script>
    <script type="text/javascript" src="https://s3.amazonaws.com/glowscript/py/glow.min.js"></script>
</head>
<body>
    <div id="glowscript" class="glowscript">
        <script type="text/x-glowscript">
        {glowscript_code}
        </script>
    </div>
</body>
</html>
"""

# --- 5. 화면 레이아웃 구성 및 렌더링 ---
col1, col2 = st.columns([1, 1.2])
with col1:
    st.subheader("GlowScript 3D 시뮬레이션")
    st.components.v1.html(full_html_code, height=450, scrolling=False)
with col2:
    st.subheader("데이터 분석 및 시각화")
    st.info("시뮬레이션이 끝나면 왼쪽 화면 아래에 나타나는 데이터를 복사해서 아래 칸에 붙여넣으세요.")
    pasted_data = st.text_area("데이터 붙여넣기", height=200, placeholder="t, x, y, vx, vy\\n0.01, 0.35, 0.35, 35.35, 35.30\\n...")
    if st.button("📈 데이터 분석 실행"):
        if pasted_data:
            try:
                df = pd.read_csv(StringIO(pasted_data))
                st.write("#### 📊 데이터 분석 결과")
                st.dataframe(df.head())
                st.write("##### 시간에 따른 위치(x, y) 그래프")
                st.line_chart(df, x='t', y=['x', 'y'])
                st.write("##### X-Y 궤적 그래프 (포물선)")
                st.scatter_chart(df, x='x', y='y')
            except Exception as e:
                st.error(f"데이터를 처리하는 중 오류가 발생했습니다. 형식을 확인해주세요: {e}")
        else:
            st.warning("데이터를 먼저 붙여넣어 주세요.")
