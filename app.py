import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 불러오기
url = "https://raw.githubusercontent.com/heesooedu/streamlit/refs/heads/main/2022%7E2024.csv"
data = pd.read_csv(url)

# 데이터 가공
grouped_data = data.groupby(['행정동', '연령대', '성별'])[['총인구수', '1인가구수']].sum().reset_index()

# Streamlit UI 설정
st.title("행정동별 연령대 및 성별에 따른 인구 데이터 시각화")

# 선택 옵션
selected_district = st.selectbox("행정동 선택", grouped_data['행정동'].unique())

# 선택된 행정동에 대한 데이터 필터링
filtered_data = grouped_data[grouped_data['행정동'] == selected_district]

# 그래프 생성
fig, axes = plt.subplots(2, 1, figsize=(10, 10))

# 총인구수 시각화
sns.barplot(data=filtered_data, x='연령대', y='총인구수', hue='성별', ax=axes[0])
axes[0].set_title(f'{selected_district} - 연령대 및 성별에 따른 총인구수')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)

# 1인가구수 시각화
sns.barplot(data=filtered_data, x='연령대', y='1인가구수', hue='성별', ax=axes[1])
axes[1].set_title(f'{selected_district} - 연령대 및 성별에 따른 1인가구수')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)

plt.tight_layout()
st.pyplot(fig)

# 추가 설명
st.write("이 대시보드는 특정 행정동에 대한 연령대 및 성별 인구 데이터를 시각화합니다.")
