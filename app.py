import streamlit as st
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl
from datetime import datetime

st.set_page_config(page_title="VPython in Streamlit", layout="wide")

# 🔗 사전 컴파일된 GlowScript HTML의 URL을 넣어주세요.
# 예: "https://<username>.github.io/<repo>/static/glowscript/cube.html"
EXPORTED_URL = "https://heesooedu.github.io/streamlit/static/glowscript/cube.html"  # ← 이 줄만 고치면 됩니다.

st.title("GlowScript VPython × Streamlit (Precompiled Embed)")

with st.sidebar:
    st.header("Embed Settings")
    url = st.text_input("Exported HTML URL", value=EXPORTED_URL, help="GitHub Pages 또는 rawcdn.githack.com 주소")
    height = st.slider("Canvas height (px)", min_value=400, max_value=1200, value=660, step=10)
    add_cache_bust = st.checkbox("Cache bust param 추가(새로고침 강제)", value=True)

# 쿼리스트링에 캐시버스트 파라미터 추가(선택)
def with_cache_bust(u: str) -> str:
    if not add_cache_bust:
        return u
    try:
        parts = list(urlparse(u))
        q = dict(parse_qsl(parts[4]))
        q["_t"] = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        parts[4] = urlencode(q)
        return urlunparse(parts)
    except Exception:
        return u

safe_url = with_cache_bust(url.strip())

# 기본 안내
if not safe_url or "<YOUR_PAGES_HOST>" in safe_url:
    st.info("왼쪽 사이드바의 **Exported HTML URL**에 GitHub Pages(또는 rawcdn) 주소를 넣어주세요.")
else:
    # iframe 임베드
    st.components.v1.html(
        f"""
        <iframe src="{safe_url}"
                style="width:100%; height:{height}px; border:0;"
                allow="fullscreen *; xr-spatial-tracking *; accelerometer *; gyroscope *; magnetometer *; microphone *; camera *">
        </iframe>
        """,
        height=height + 10,
    )

st.caption(
    "이 방식은 GlowScript 코드를 미리 JS로 컴파일한 정적 HTML을 불러옵니다. "
    "Streamlit iframe의 보안정책으로 런타임 컴파일이 차단되는 문제를 우회해 캔버스가 정상 표시됩니다."
)
