import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# 데이터 저장용 파일
DATA_FILE = "survey_data.csv"

# 데이터 불러오기 함수
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Survey", "Name", "Answer"])

# 데이터 저장 함수
def save_data(survey, name, answer):
    data = load_data()
    new_data = pd.DataFrame({"Survey": [survey], "Name": [name], "Answer": [answer]})
    data = pd.concat([data, new_data], ignore_index=True)
    data.to_csv(DATA_FILE, index=False)

# 데이터 초기화 함수
def delete_all_data():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    # 빈 파일 생성
    pd.DataFrame(columns=["Survey", "Name", "Answer"]).to_csv(DATA_FILE, index=False)

# 워드클라우드 생성 함수
def generate_wordcloud(text):
    font_path = "Hakgyoansim Nadeuri TTF B.ttf"  # 폰트 파일 이름
    wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color="white").generate(text)
    return wordcloud

# 메인 페이지
st.title("세션1 AI디지털 시대 학교경영")
st.title("설문조사")

menu = ["메인", "사전설문", "1번 질문(김태원 대표님)", "2번 질문(이준호 교장님)", "3번 질문(정진선 교장님)", "결과 보기"]
choice = st.sidebar.selectbox("메뉴 선택", menu)

if choice == "메인":
    st.subheader("좌측 사이드바에서 설문을 선택하세요.")

elif choice in ["사전설문", "1번 질문(김태원 대표님)", "2번 질문(이준호 교장님)", "3번 질문(정진선 교장님)"]:
    st.subheader(f"{choice} 페이지")
    with st.form(f"{choice}_form"):
        name = st.text_input("이름")
        answer = st.text_area("질문에 대한 답변을 입력하세요")
        submitted = st.form_submit_button("제출")
        if submitted:
            save_data(choice, name, answer)
            st.success("설문이 저장되었습니다!")

elif choice == "결과 보기":
    st.subheader("설문조사 결과")
    data = load_data()

    if st.checkbox("1번 설문 결과 (워드클라우드) 보기"):
        survey1_data = data[data["Survey"] == "사전설문"]["Answer"].dropna()
        text = " ".join(survey1_data)
        if text:
            wordcloud = generate_wordcloud(text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            st.pyplot(plt)
        else:
            st.write("데이터가 없습니다.")

    if st.checkbox("2, 3, 4번 설문 데이터 보기"):
        st.dataframe(data)
        csv = data.to_csv(index=False)
        st.download_button(
            label="CSV 다운로드",
            data=csv,
            file_name="survey_data.csv",
            mime="text/csv",
        )
    
    # 데이터 초기화 버튼
    st.subheader("응답 데이터 초기화")
    if st.button("모든 응답 삭제"):
        delete_all_data()
        st.warning("모든 데이터가 삭제되었습니다!")
