import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
@st.cache_data
def load_data():
    file_url = "https://raw.githubusercontent.com/heesooedu/streamlit/refs/heads/main/2022%7E2024.csv"
    df = pd.read_csv(file_url)
    return df

# 데이터 로드
df = load_data()

# '월계1동' 데이터 필터링
wolgae_df = df[df['행정동명'] == '월계1동']

# Streamlit 페이지 설정
st.title("📊 월계1동 인구 및 통계 시각화")
st.write("이 대시보드는 월계1동의 인구 통계를 시각화합니다.")

# 연령대별 총인구수 시각화
st.subheader("🔹 연령대별 총인구수")
age_population_cols = [col for col in wolgae_df.columns if '연령대' in col]
age_population_data = wolgae_df[['기준년도'] + age_population_cols].set_index('기준년도')
st.line_chart(age_population_data)

# 1인 가구수 시각화
st.subheader("🔹 1인 가구수 변화")
one_person_household = wolgae_df[['기준년도', '1인가구수']].set_index('기준년도')
st.bar_chart(one_person_household)

# 출근 소요시간 미추정 인구수 시각화
st.subheader("🔹 출근 소요시간 미추정 인구수")
unknown_commute_time = wolgae_df[['기준년도', '출근소요시간미추정인구수']].set_index('기준년도')
st.area_chart(unknown_commute_time)

# 데이터프레임 전체 보기
st.subheader("🔹 전체 데이터")
st.dataframe(wolgae_df)

