import streamlit as st
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(
    page_title="지진 데이터 시각화",
    page_icon="🌍",
    layout="wide" # wide layout으로 설정하여 더 넓게 표시
)

# --- 데이터 로딩 ---
# CSV 파일을 로드하는 함수 (캐시를 사용하여 성능 향상)
@st.cache_data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        # Streamlit의 st.map()을 위해 위도/경도 컬럼명을 맞춰줌
        data.rename(columns={'latitude': 'lat', 'longitude': 'lon'}, inplace=True)
        return data
    except FileNotFoundError:
        st.error(f"'{file_path}' 파일을 찾을 수 없습니다. app.py와 같은 위치에 있는지 확인하세요.")
        return None

# 데이터 로드
df = load_data('earthquake_1995-2023.csv')

# 데이터 로딩에 실패하면 앱 실행 중지
if df is None:
    st.stop()


# --- 사이드바 (필터) ---
st.sidebar.header('데이터 필터')

# 규모(magnitude) 필터
mag_range = st.sidebar.slider(
    '지진 규모(Magnitude) 선택:',
    min_value=float(df['magnitude'].min()),
    max_value=float(df['magnitude'].max()),
    value=(7.0, 9.0) # 기본값 설정
)

# 깊이(depth) 필터
depth_range = st.sidebar.slider(
    '지진 깊이(Depth) 선택 (km):',
    min_value=int(df['depth'].min()),
    max_value=int(df['depth'].max()),
    value=(0, 700) # 기본값 설정
)

# 선택된 범위로 데이터 필터링
filtered_df = df[
    (df['magnitude'] >= mag_range[0]) &
    (df['magnitude'] <= mag_range[1]) &
    (df['depth'] >= depth_range[0]) &
    (df['depth'] <= depth_range[1])
]


# --- 메인 페이지 ---
st.title('🌍 지진 데이터 대시보드')
st.write('사이드바의 필터를 사용하여 특정 규모와 깊이의 지진 데이터를 탐색할 수 있습니다.')

# 필터링된 결과 요약
st.markdown(f"**총 {len(df)}개의 데이터 중, 선택된 조건에 맞는 지진은 `{len(filtered_df)}`건 입니다.**")
st.write('---')

# 2개의 컬럼으로 레이아웃 분할
col1, col2 = st.columns((1, 1)) # (비율)

with col1:
    # 지도 시각화
    st.subheader('지진 발생 위치 지도')
    if not filtered_df.empty:
        st.map(filtered_df)
    else:
        st.warning("선택된 조건에 해당하는 데이터가 없습니다.")

with col2:
    # 규모(magnitude) 분포도
    st.subheader('규모(Magnitude)별 지진 발생 횟수')
    if not filtered_df.empty:
        # 규모를 기준으로 데이터의 개수를 세어 막대 차트로 표시
        mag_counts = filtered_df['magnitude'].value_counts().sort_index()
        st.bar_chart(mag_counts)
    else:
        st.warning("차트를 표시할 데이터가 없습니다.")

st.write('---')

# 필터링된 데이터 테이블 표시
st.subheader('필터링된 데이터 보기')
st.dataframe(filtered_df)
