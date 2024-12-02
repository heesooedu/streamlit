import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re  # 정규표현식 사용

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

# 한글 단어 추출 함수
def extract_nouns(text):
    # 정규표현식을 사용하여 한글 명사형 단어 추출
    words = re.findall(r"[가-힣]{2,}", text)  # 2글자 이상의 한글 단어 추출
    return " ".join(words)

# 워드클라우드 생성 함수
def generate_wordcloud(text):
    # 한글 명사 추출
    processed_text = extract_nouns(text)
    font_path = "Hakgyoansim Nadeuri TTF B.ttf"  # 폰트 파일 이름
    wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color="white").generate(processed_text)
    return wordcloud

# 메인 페이지
st.title("세션1 AI디지털 시대 학교경영")
st.title("설문조사")

menu = ["메인", "사전설문", "2번 설문", "3번 설문", "4번 설문", "결과 보기"]
choice = st.sidebar.selectbox("메뉴 선택", menu)

if choice == "메인":
    st.subheader("설문조사에 참여해주세요!")
    st.write("좌측 사이드바에서 설문을 선택하세요.")

elif choice in ["사전설문", "2번 설문", "3번 설문", "4번 설문"]:
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
