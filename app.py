import streamlit as st

# MBTI 유형별 직업 추천 데이터
# 실제로는 더 정교하고 많은 데이터가 필요하지만, 예시로 간단하게 구성했습니다.
job_recommendations = {
    'ISTJ': ['회계사', '법률가', '프로젝트 관리자', '데이터 분석가', '공무원'],
    'ISFJ': ['간호사', '교사', '사회 복지사', '사서', '상담사'],
    'INFJ': ['상담사', '작가', '인사 관리자', '예술가', '비영리 단체 운영자'],
    'INTJ': ['전략 컨설턴트', '과학자', '엔지니어', '변호사', '개발자'],
    'ISTP': ['엔지니어', '파일럿', '운동선수', '소방관', '요리사'],
    'ISFP': ['예술가', '디자이너', '수의사', '작곡가', '플로리스트'],
    'INFP': ['작가', '심리학자', '그래픽 디자이너', '편집자', '사회 운동가'],
    'INTP': ['프로그래머', '철학자', '교수', '데이터 과학자', '연구원'],
    'ESTP': ['영업 관리자', '기업가', '마케터', '경찰관', '스포츠 코치'],
    'ESFP': ['배우', '이벤트 플래너', '영업 담당자', '가이드', '피트니스 트레이너'],
    'ENFP': ['크리에이티브 디렉터', '저널리스트', '광고 기획자', '상담가', '강사'],
    'ENTP': ['변호사', '컨설턴트', '발명가', '정치인', '기업가'],
    'ESTJ': ['경영진', '감독관', '재무 관리자', '군 장교', '교장'],
    'ESFJ': ['교사', '인사 담당자', '이벤트 코디네이터', '의료 전문가', '고객 서비스 관리자'],
    'ENFJ': ['교사', '정치인', 'HR 전문가', '경영 컨설턴트', '사회 복지사'],
    'ENTJ': ['CEO', '변호사', '경영 컨설턴트', '투자 은행가', '기업가']
}

# --- 웹 앱 UI 구성 ---

st.title('MBTI 기반 직업 추천')
st.write('자신의 MBTI 유형을 선택하면, 어울리는 직업들을 추천해 드립니다.')
st.write('---')

# MBTI 선택을 위한 4개의 selectbox 생성
col1, col2, col3, col4 = st.columns(4)

with col1:
    first = st.selectbox('**E / I**', ('E (외향)', 'I (내향)'), index=None, placeholder="선택...")
with col2:
    second = st.selectbox('**S / N**', ('S (감각)', 'N (직관)'), index=None, placeholder="선택...")
with col3:
    third = st.selectbox('**T / F**', ('T (사고)', 'F (감정)'), index=None, placeholder="선택...")
with col4:
    fourth = st.selectbox('**J / P**', ('J (판단)', 'P (인식)'), index=None, placeholder="선택...")

# 모든 지표가 선택되었는지 확인
if first and second and third and fourth:
    # 선택된 값에서 첫 글자만 추출하여 MBTI 조합
    mbti_type = first[0] + second[0] + third[0] + fourth[0]

    st.write('---')
    st.header(f'당신의 MBTI는 **{mbti_type}** 입니다.', anchor=False)

    # 추천 직업 목록 가져오기
    recommended_jobs = job_recommendations.get(mbti_type, [])

    if recommended_jobs:
        st.subheader('추천 직업 목록:', anchor=False)
        # 추천 직업을 글머리 기호 목록으로 표시
        for job in recommended_jobs:
            st.markdown(f"- {job}")
    else:
        st.warning('해당 MBTI 유형에 대한 추천 직업 정보가 없습니다.')

    st.info('**주의:** 이 추천은 일반적인 경향에 따른 것이며, 개인의 흥미와 적성에 따라 결과는 달라질 수 있습니다.')

else:
    st.info('위에서 4가지 지표를 모두 선택해주세요.')
