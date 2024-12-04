import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os
import platform
from matplotlib import rc
from matplotlib.font_manager import FontProperties

# 데이터 저장용 파일
DATA_FILE = "survey_data.csv"
ADMIN_PASSWORD = "admin123"  # 관리자 비밀번호

# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "menu_choice" not in st.session_state:
    st.session_state["menu_choice"] = "메인"

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

# 한글 폰트 설정 함수
def set_custom_korean_font():
    # 현재 디렉토리에 있는 폰트 경로
    font_path = os.path.join(os.path.dirname(__file__), "Hakgyoansim Nadeuri TTF B.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {font_path}")
    
    custom_font = FontProperties(fname=font_path)
    rc("font", family=custom_font.get_name())

# 사전설문 결과 시각화
def visualize_survey_results(data):
    # 사용자 정의 폰트 설정
    set_custom_korean_font()

    # 사전설문 데이터 필터링
    survey_data = data[data["Survey"] == "사전설문"]
    
    # 1~7번 응답 카운팅
    predefined_answers = [
        "1. 예산 및 자원 부족",
        "2. 교사의 디지털 역량 강화 어려움",
        "3. AI 및 디지털 콘텐츠의 부족과 적절한 선택의 어려움",
        "4. 교사 및 학부모의 디지털 혁신에 대한 저항",
        "5. 학생의 디지털 윤리 및 책임 교육의 필요성",
        "6. 학생들의 디지털 역량 격차",
        "7. 교육 혁신에 대한 구체적인 성공 사례 부족"
    ]
    predefined_counts = Counter(answer for answer in survey_data["Answer"] if answer in predefined_answers)

    # 기타 응답 필터링
    other_responses = survey_data[~survey_data["Answer"].isin(predefined_answers)][["Answer"]]

    # 파이차트 데이터
    labels = list(predefined_counts.keys())
    sizes = list(predefined_counts.values())
    colors = plt.cm.Paired.colors[:len(labels)]  # 자동 색상 설정

    # 파이차트 시각화
    st.subheader("사전설문 응답 비율")
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    ax.axis("equal")  # 파이차트를 원형으로 유지
    st.pyplot(fig)

    # 기타 응답 표로 표시
    st.subheader("기타 응답 (표 형식)")
    if not other_responses.empty:
        st.table(other_responses)
    else:
        st.write("기타 응답이 없습니다.")

# 결과 보기 페이지
def admin_page():
    st.subheader("설문조사 결과")
    data = load_data()

    # 데이터가 비어있거나 열이 부족한 경우 처리
    if "Name" not in data.columns:
        data["Name"] = ""
    if "Answer" not in data.columns:
        data["Answer"] = ""

    if not data.empty:
        visualize_survey_results(data)

    for question in ["1번 질문(김태원 대표님)", "2번 질문(이준호 교장님)", "3번 질문(정진선 교장님)"]:
        st.subheader(f"{question} 데이터")
        question_data = data[data["Survey"] == question][["Name", "Answer"]]  # Name, Answer만 표시
        if not question_data.empty:
            st.table(
                question_data.style.set_properties(
                    subset=["Answer"], **{"white-space": "pre-wrap"}
                )
            )
        else:
            st.write("데이터가 없습니다.")

    # "소감" 데이터 표시
    st.subheader("소감 데이터")
    impression_data = data[data["Survey"] == "소감"][["Name", "Answer"]]
    if not impression_data.empty:
        st.table(
            impression_data.style.set_properties(
                subset=["Answer"], **{"white-space": "pre-wrap"}
            )
        )
    else:
        st.write("소감 데이터가 없습니다.")

    # 데이터 초기화 버튼
    st.markdown("<br><br>", unsafe_allow_html=True)  # 버튼 아래로 떨어뜨리기
    st.subheader("응답 데이터 초기화")
    if st.button("모든 응답 삭제"):
        delete_all_data()
        st.warning("모든 데이터가 삭제되었습니다!")

# 관리자 로그인 페이지
def admin_login():
    st.subheader("관리자 로그인")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("로그인"):
        if password == ADMIN_PASSWORD:
            st.session_state["logged_in"] = True
            st.success("로그인 성공! 이제 '결과 보기' 메뉴를 이용할 수 있습니다.")
        else:
            st.error("비밀번호가 틀렸습니다.")

# 메인 페이지
st.title("세션1 AI디지털 시대 학교경영")
st.title("설문조사")

# 기본 메뉴
menu = ["메인", "사전설문", "1번 질문(김태원 대표님)", "2번 질문(이준호 교장님)", "3번 질문(정진선 교장님)", "소감", "관리자 페이지"]

# 로그인 성공 시 '결과 보기' 추가
if st.session_state["logged_in"]:
    menu.append("결과 보기")

choice = st.sidebar.selectbox("메뉴 선택", menu, key="menu_choice")

# 선택 후 사이드바 닫기
if st.session_state.get("menu_choice") != choice:
    st.session_state["menu_choice"] = choice
    st.experimental_rerun()

if choice == "메인":
    st.subheader("좌측 상단 사이드바(>)에서 설문을 선택하세요.")

elif choice == "사전설문":
    st.subheader("사전설문 페이지")
    st.write("**학교에서 디지털 교육 혁신을 추진하는 과정에서 가장 큰 도전 과제는 무엇이라고 생각하십니까?**")

    # CSS 스타일링 적용
    st.markdown(
        """
        <style>
        /* 라디오 버튼 텍스트 크기 조절 */
        div[data-baseweb="radio"] > label p {
            font-size: 23px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    options = [
        "1. 예산 및 자원 부족",
        "2. 교사의 디지털 역량 강화 어려움",
        "3. AI 및 디지털 콘텐츠의 부족과 적절한 선택의 어려움",
        "4. 교사 및 학부모의 디지털 혁신에 대한 저항",
        "5. 학생의 디지털 윤리 및 책임 교육의 필요성",
        "6. 학생들의 디지털 역량 격차",
        "7. 교육 혁신에 대한 구체적인 성공 사례 부족",
        "8. 기타 (직접 입력)"
    ]

    selected_option = st.radio("다음 중 하나를 선택하세요", options)
    other_answer = ""

    # "8번 기타"를 선택한 경우 즉시 주관식 입력 필드 표시
    if selected_option == "8. 기타 (직접 입력)":
        other_answer = st.text_area("기타 의견을 입력하세요")

    if st.button("제출"):
        answer = selected_option
        if selected_option == "8. 기타 (직접 입력)" and other_answer:
            answer = f"{selected_option}: {other_answer}"

        save_data("사전설문", "", answer)  # 이름 없음
        st.success("설문이 저장되었습니다!")



elif choice in ["1번 질문(김태원 대표님)", "2번 질문(이준호 교장님)", "3번 질문(정진선 교장님)"]:
    st.subheader(f"{choice} 페이지")
    with st.form(f"{choice}_form"):
        name = st.text_input("이름")
        answer = st.text_area("질문에 대한 답변을 입력하세요")
        submitted = st.form_submit_button("제출")
        if submitted:
            save_data(choice, name, answer)
            st.success("설문이 저장되었습니다!")

elif choice == "소감":
    st.subheader("소감 페이지")
    with st.form("소감_form"):
        name = st.text_input("이름")
        impression = st.text_area("소감을 입력하세요")
        submitted = st.form_submit_button("제출")
        if submitted:
            save_data("소감", name, impression)
            st.success("소감이 저장되었습니다!")

elif choice == "관리자 페이지":
    if st.session_state["logged_in"]:
        st.info("이미 로그인 상태입니다. '결과 보기' 메뉴를 이용하세요.")
    else:
        admin_login()

elif choice == "결과 보기":
    if st.session_state["logged_in"]:
        admin_page()
    else:
        st.warning("관리자만 접근할 수 있습니다. 먼저 로그인하세요.")
        admin_login()
