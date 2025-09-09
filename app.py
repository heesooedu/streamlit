# 필요한 라이브러리를 가져옵니다.
import streamlit as st
import pandas as pd
from io import StringIO

# --- 1. 스트림릿 페이지 기본 설정 ---
st.set_page_config(layout="wide") # 페이지 레이아웃을 넓게 설정
st.title("🚀 GlowScript + Streamlit 통합 물리 시뮬레이터")
st.write("GlowScript의 3D 시뮬레이션과 Streamlit의 데이터 분석 기능을 결합한 웹 앱입니다.")
st.write("---")


# --- 2. 사이드바에서 시뮬레이션 조건 입력받기 ---
with st.sidebar:
    st.header("⚙️ 시뮬레이션 조건 설정")
    # 슬라이더와 숫자 입력을 통해 초기 속도, 발사 각도, 중력 가속도 값을 받습니다.
    v0 = st.slider("초기 속도 (m/s)", min_value=10, max_value=100, value=50, step=1)
    angle = st.slider("발사 각도 (도)", min_value=10, max_value=80, value=45, step=1)
    g = st.number_input("중력 가속도 (m/s²)", value=9.8, format="%.2f")


# --- 3. 입력받은 조건으로 VPython(GlowScript) 코드 동적 생성 ---
# f-string을 사용하여 사이드바에서 입력받은 변수들을 코드에 삽입합니다.
glowscript_code = f"""
from vpython import *

# 3D 캔버스 설정
scene.width = 600
scene.height = 400

# 객체 생성 (공, 땅)
ball = sphere(pos=vector(0,0,0), radius=0.5, color=color.red, make_trail=True, trail_color=color.yellow)
ground = box(pos=vector(0,-1,0), size=vector(150,0.5,10), color=color.green)

# 물리 변수 설정 (Streamlit에서 받은 값 사용)
g = {g}
v0 = {v0}
theta = radians({angle})

ball.v = vector(v0*cos(theta), v0*sin(theta), 0) # 속도의 x, y 성분
ball.m = 1 # 질량

# 시간 변수 설정
dt = 0.01
t = 0

# 데이터 출력을 위한 CSV 헤더
print("t, x, y, vx, vy")

# 시뮬레이션 루프 (공이 땅 위(y>=0)에 있을 동안 반복)
while ball.pos.y >= 0:
    rate(100) # 초당 100번의 계산 실행
    
    # 물리 계산 (힘 -> 속도 -> 위치)
    F = vector(0, -ball.m*g, 0)
    ball.v = ball.v + F/ball.m * dt
    ball.pos = ball.pos + ball.v * dt
    t = t + dt
    
    # 현재 상태 데이터 출력 (소수점 둘째 자리까지)
    print(f"{{t:.2f}}, {{ball.pos.x:.2f}}, {{ball.pos.y:.2f}}, {{ball.v.x:.2f}}, {{ball.v.y:.2f}}")

"""


# --- 4. GlowScript 라이브러리를 포함한 완전한 HTML 코드 생성 ---
# 시뮬레이션이 웹에서 실행되도록 JS 라이브러리를 CDN으로 불러오는 HTML 코드입니다.
full_html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GlowScript</title>
    <script type="text/javascript" src="https://www.glowscript.org/lib/jquery/2.1/jquery.min.js"></script>
    <script type="text/javascript" src="https://www.glowscript.org/lib/glow/3.2/glow.min.js"></script>
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
# 화면을 두 개의 컬럼으로 나눕니다.
col1, col2 = st.columns([1, 1.2]) # 왼쪽 컬럼이 조금 더 좁게

# 왼쪽 컬럼: GlowScript 시뮬레이션 화면
with col1:
    st.subheader("GlowScript 3D 시뮬레이션")
    # `st.components.v1.html`을 사용해 위에서 생성한 HTML 코드를 렌더링합니다.
    st.components.v1.html(full_html_code, height=450, scrolling=False)

# 오른쪽 컬럼: 데이터 분석 및 시각화 영역
with col2:
    st.subheader("데이터 분석 및 시각화")
    st.info("시뮬레이션이 끝나면 왼쪽 화면 아래에 나타나는 데이터를 복사해서 아래 칸에 붙여넣으세요.")
    
    # 데이터 붙여넣기 영역
    pasted_data = st.text_area("데이터 붙여넣기", height=200, placeholder="t, x, y, vx, vy\\n0.01, 0.35, 0.35, 35.35, 35.30\\n...")
    
    # '데이터 분석 실행' 버튼
    if st.button("📈 데이터 분석 실행"):
        if pasted_data:
            try:
                # 붙여넣은 텍스트 데이터를 Pandas DataFrame으로 변환
                df = pd.read_csv(StringIO(pasted_data))
                
                st.write("#### 📊 데이터 분석 결과")

                # 데이터 프레임 테이블 출력
                st.dataframe(df.head())
                
                # GlowScript에서는 그리기 어려운 다양한 그래프 시각화
                st.write("##### 시간에 따른 위치(x, y) 그래프")
                st.line_chart(df, x='t', y=['x', 'y'])
                
                st.write("##### 시간에 따른 속도(vx, vy) 그래프")
                st.line_chart(df, x='t', y=['vx', 'vy'])

                st.write("##### X-Y 궤적 그래프 (포물선)")
                st.scatter_chart(df, x='x', y='y')
                
            except Exception as e:
                # 데이터 형식이 잘못되었을 경우 에러 메시지 출력
                st.error(f"데이터를 처리하는 중 오류가 발생했습니다. 형식을 확인해주세요: {e}")
        else:
            # 데이터가 없을 경우 경고 메시지 출력
            st.warning("데이터를 먼저 붙여넣어 주세요.")
