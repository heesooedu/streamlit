# app.py
import base64
import json
import re
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st

st.set_page_config(page_title="Web VPython Builder", layout="wide")

# ------------------------------------------------------------
# 0) 유틸
# ------------------------------------------------------------
def secrets_ok(keys=("GITHUB_TOKEN", "GITHUB_REPO", "GITHUB_BRANCH", "GITHUB_BASE")):
    return {k: (k in st.secrets and bool(st.secrets[k])) for k in keys}

def sanitize_filename(name: str, default="scene"):
    # 파일명 안전화
    name = name.strip()
    if not name:
        name = default
    name = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", name)
    return name

def gh_upsert_file(path_in_repo: str, text: str):
    """GitHub repo에 파일 생성/업데이트. 응답을 그대로 반환(디버깅용)."""
    token = st.secrets["GITHUB_TOKEN"]
    repo  = st.secrets["GITHUB_REPO"]          # "heesooedu/streamlit"
    branch= st.secrets.get("GITHUB_BRANCH","main")

    api = f"https://api.github.com/repos/{repo}/contents/{path_in_repo}"

    headers = {
        "Authorization": f"token {token}",     # Classic PAT/Fine-grained 모두 OK
        "Accept": "application/vnd.github+json",
    }

    # 현재 파일 sha 조회 (있으면 업데이트, 없으면 생성)
    sha = None
    r_get = requests.get(api, headers=headers, params={"ref": branch})
    if r_get.status_code == 200:
        try:
            sha = r_get.json().get("sha")
        except Exception:
            pass

    payload = {
        "message": f"streamlit: upsert {path_in_repo}",
        "content": base64.b64encode(text.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    r_put = requests.put(api, headers=headers, data=json.dumps(payload))
    return {
        "get_status": r_get.status_code,
        "get_body": r_get.text,
        "put_status": r_put.status_code,
        "put_body": r_put.text,
        "api_url": api,
        "branch": branch,
        "path": path_in_repo,
    }

# ------------------------------------------------------------
# 1) Web VPython(GlowScript) HTML 템플릿
#    - 사용자가 입력한 Python 소스를 <script type="text/python">로 삽입
#    - GlowScript 런타임(CDN)로 브라우저 내 트랜스파일/실행
# ------------------------------------------------------------
_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>

<!-- jQuery (GlowScript가 기대하는 버전대) -->
<script src="https://www.glowscript.org/lib/jquery/2.1/jquery.min.js"></script>
<script src="https://www.glowscript.org/lib/jquery/2.1/jquery-ui.custom.min.js"></script>
<link rel="stylesheet" href="https://www.glowscript.org/css/redmond/2.1/jquery-ui.custom.css" />

<!-- GlowScript / Web VPython 런타임 -->
<script src="https://www.glowscript.org/package/glow.3.2.min.js"></script>
<!-- *중요*: 브라우저 내 Python 실행을 위한 런타임 (RapydScript 등) -->
<script src="https://www.glowscript.org/lib/RSrun.3.2.min.js"></script>

<style>
  html, body {{ height: 100%; margin: 0; background: #111; color: #eee; }}
  .container {{ max-width: 1000px; margin: 0 auto; padding: 12px; }}
  #glowscript {{ outline: none; }}
</style>
</head>
<body>
<div class="container">
  <h3 style="margin: 8px 0 12px;">{title}</h3>
  <div id="glowscript" class="glowscript" style="outline:none;">[loading GlowScript...]</div>
</div>

<script>
  // GlowScript 컨테이너 지정
  window.__context = {{ glowscript_container: $("#glowscript").removeAttr("id") }};
</script>

<!-- 사용자 Python 소스 (브라우저에서 트랜스파일되어 실행) -->
<script type="text/python">
GlowScript 3.2 VPython
{code}
</script>
</body>
</html>
"""

def make_glowscript_html(py_source: str, title="Web VPython Scene"):
    # 사용자가 "GlowScript 3.x VPython" 선두 라인을 이미 넣었어도 중복되지 않게 가공
    cleaned = re.sub(r"^\s*GlowScript\s+\d+(\.\d+)?\s+VPython\s*\n", "", py_source, flags=re.IGNORECASE|re.MULTILINE)
    return _HTML_TEMPLATE.format(title=title, code=cleaned)

# ------------------------------------------------------------
# 2) UI
# ------------------------------------------------------------
st.title("🧪 Web VPython Builder (Streamlit → GitHub Pages)")

cols = st.columns([2, 1])
with cols[0]:
    default_code = """# 예시: 자유낙하
from vpython import *
scene.width = 800
scene.height = 450
center = sphere(pos=vec(0,10,0), color=color.yellow, radius=0.3, emissive=True)
ball = sphere(pos=vector(5,10,0), radius=0.5, color=color.red, make_trail=True)
velocity = vector(0,0,0)
acceleration = vector(0,-9.8,0)
dt = 0.01
while True:
    rate(100)
    ball.pos = ball.pos + velocity*dt
    velocity = velocity + acceleration*dt
"""
    code = st.text_area("VPython 코드 입력", value=default_code, height=420)

with cols[1]:
    st.subheader("파일/퍼블리시 설정")
    file_stem = st.text_input("파일명(확장자 제외)", value="scene")
    subdir = st.text_input("저장 경로(리포지토리 내부)", value="static/glowscript")
    title = st.text_input("HTML title", value="My VPython Scene")
    timestamp_suffix = st.checkbox("이름에 타임스탬프 붙이기", value=True)

    # Secrets 상태 표시
    chk = secrets_ok()
    st.caption("Secrets 상태:")
    st.write(chk)

    # 디버그: GitHub API 업/다운 테스트
    if st.button("GitHub 퍼블리시 테스트(텍스트 파일)"):
        if not all(chk.values()):
            st.error("Secrets가 비어 있습니다. Streamlit Cloud의 이 앱 Settings → Secrets에 4개 모두 저장하세요.")
        else:
            resp = gh_upsert_file(f"{subdir}/_probe.txt", "hello from streamlit")
            st.code(json.dumps(resp, indent=2, ensure_ascii=False))

st.markdown("---")

c1, c2 = st.columns(2)

# ------------------------------------------------------------
# 3) A: 로컬/개발용 '직접 실행' 미리보기 (CSP로 배포환경에서 실패할 수 있음)
# ------------------------------------------------------------
with c1:
    st.subheader("A) 로컬 개발 미리보기 (직접 실행)")
    st.caption("배포 환경(CSP)에서는 보통 안 됩니다. 개발/로컬에서만 가끔 성공.")
    html_srcdoc = make_glowscript_html(code, title=title)
    # iframe(srcdoc) 미리보기
    st.components.v1.html(
        html_srcdoc,
        height=520,
        scrolling=True,
    )

# ------------------------------------------------------------
# 4) B: GitHub Pages로 퍼블리시 → 안정적 임베드
# ------------------------------------------------------------
with c2:
    st.subheader("B) GitHub Pages로 퍼블리시")
    st.caption("Secrets에 GITHUB_TOKEN/REPO/BRANCH/BASE가 있어야 합니다.")

    if st.button("➡️ 퍼블리시 & 임베드"):
        chk = secrets_ok()
        if not all(chk.values()):
            st.error("Secrets가 비어 있습니다. Settings → Secrets에 4개 모두 저장 후 앱 재시작하세요.")
        else:
            # 파일명/경로 구성
            stem = sanitize_filename(file_stem or "scene")
            if timestamp_suffix:
                stem += "-" + datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = stem + ".html"
            path_in_repo = f"{subdir.strip().strip('/')}/{filename}"

            html_text = make_glowscript_html(code, title=title)
            resp = gh_upsert_file(path_in_repo, html_text)
            st.code(json.dumps(resp, indent=2, ensure_ascii=False))

            if resp.get("put_status") in (200, 201):
                base = st.secrets["GITHUB_BASE"].rstrip("/")
                url = f"{base}/{path_in_repo}"
                st.success("퍼블리시 성공! 아래에 바로 임베드합니다.")
                st.write("URL:", url)

                # 외부 URL 임베드 (CSP 영향 없음)
                iframe_html = f'<iframe src="{url}" style="width:100%;height:520px;border:0;" allow="fullscreen *; xr-spatial-tracking *; accelerometer; magnetometer; gyroscope"></iframe>'
                st.components.v1.html(iframe_html, height=540)
            else:
                st.error("퍼블리시 실패. 위의 응답 본문(put_body/get_body)을 확인하세요. (권한/경로/브랜치 문제 가능)")

st.markdown("---")
st.caption("Tip: GitHub Pages는 보통 수 초 내 서빙됩니다. 같은 이름으로 덮어쓰면 캐시 때문에 새로고침(강력 새로고침)이 필요할 수 있어요.")
