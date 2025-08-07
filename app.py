import streamlit as st
import pandas as pd
import numpy as np

# 1. 제목과 헤더 설정
st.title('나의 첫 Streamlit 웹 앱')
st.header('간단한 인터랙티브 기능을 체험해보세요.')
st.write('---') # 구분선

# 2. 사용자 이름 입력 받기 (텍스트 입력 위젯)
st.subheader('1. 텍스트 입력')
name = st.text_input('이름을 입력해주세요:')

# 이름이 입력되었을 경우에만 인사 메시지 출력
if name:
    st.write(f'👋 안녕하세요, **{name}**님! 만나서 반갑습니다.')

st.write('---')

# 3. 숫자 입력 받기 (슬라이더 위젯)
st.subheader('2. 숫자 선택과 계산')
x = st.slider('제곱할 숫자를 선택하세요.', min_value=0, max_value=100, value=25, step=1)
st.write(f'선택한 숫자 **{x}**의 제곱은 **{x*x}**입니다.')

st.write('---')

# 4. 데이터 시각화 (선택 박스 위젯과 차트)
st.subheader('3. 데이터 시각화')
st.write('아래 드롭다운 메뉴에서 보고 싶은 데이터를 선택하면, 해당 데이터로 라인 차트를 생성합니다.')

# 샘플 데이터 생성
chart_data = pd.DataFrame(
    np.random.randn(20, 3), # 20x3 크기의 난수 데이터 생성
    columns=['데이터 A', '데이터 B', '데이터 C']
)

# 사용자가 차트에 표시할 데이터를 선택
option = st.selectbox(
    '어떤 데이터를 시각화할까요?',
    ('데이터 A', '데이터 B', '데이터 C')
)

# 선택된 데이터로 라인 차트 그리기
st.line_chart(chart_data[option])

st.write('---')
st.success('축하합니다! Streamlit 앱의 기본 기능을 모두 체험하셨습니다. 🎉')
