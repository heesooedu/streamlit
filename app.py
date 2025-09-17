import streamlit as st
from datetime import datetime
import io
import pandas as pd

st.set_page_config(page_title="VPython + Streamlit (Plan A)", layout="wide")

# ========== 사이드/상단 컨트롤 ==========
st.title("GlowScript VPython × Streamlit (Plan A: 템플릿 치환)")

col_ctrl, col_sim = st.columns([1, 2], gap="large")

with col_ctrl:
    st.subheader("실험 설정")
    g = st.slider("중력 가속도 g (m/s²)", min_value=1.0, max_value=20.0, value=9.8, step=0.1)
    v0 = st.slider("초기속도 v0 (m/s)", min_value=1.0, max_value=50.0, value=20.0, step=0.5)
    angle = st.slider("발사각 (deg)", min_value=0, max_value=90, value=45, step=1)

    st.markdown("---")
    st.subheader("실험 기록")
    if "runs" not in st.session_state:
        st.session_state.runs = []

    # 기록 추가 버튼
    if st.button("현재 설정을 기록에 추가"):
        st.session_state.runs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "g": float(g),
            "v0": float(v0),
            "angle_deg": int(angle),
        })

    # 기록 테이블
    if len(st.session_state.runs) > 0:
        df = pd.DataFrame(st.session_state.runs)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # CSV 다운로드
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "CSV로 다운로드",
            data=csv,
            file_name="runs.csv",
            mime="text/csv"
        )
    else:
        st.info("아직 기록이 없습니다. 파라미터를 조정하고 '현재 설정을 기록에 추가'를 누르세요.")

with col_sim:
    st.subheader("시뮬레이션")
    # 템플릿 읽기 (캐시)
    # @st.cache_data
    def load_template():
        with open("templates/glowscript_vpython_template.html", "r", encoding="utf-8") as f:
            return f.read()

    html_template = load_template()
    # 토큰 치환
    html_filled = (html_template
                   .replace("__G__", str(g))
                   .replace("__V0__", str(v0))
                   .replace("__ANGLE__", str(angle))
                   )

    # 임베딩 (값 변경 시 재렌더링 → 시뮬 리셋)
    st.components.v1.html(html_filled, height=520, scrolling=False)

st.markdown("---")

# ======= 간단 분석(이론 사거리) =======
st.subheader("간단 분석 (공기저항 무시 이론값)")
import math
angle_rad = math.radians(angle)
range_theory = (v0**2 * math.sin(2*angle_rad)) / g if g > 0 else float('nan')
hmax_theory = (v0**2 * (math.sin(angle_rad)**2)) / (2*g) if g > 0 else float('nan')

col_a, col_b = st.columns(2)
with col_a:
    st.metric("이론 사거리 (m)", f"{range_theory:.2f}")
with col_b:
    st.metric("이론 최대높이 (m)", f"{hmax_theory:.2f}")

st.caption("※ 화면의 '측정값(실험)'은 시뮬레이션 결과를 이용한 추정치이며, 위의 메트릭은 이론식(공기저항 무시)입니다.")
