# app.py
import base64
import datetime as dt
from textwrap import dedent

import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="VPython in Streamlit (1-click Publish)", layout="wide")
st.title("VPython → GitHub Pages 원클릭 퍼블리시")

# --- 사용자 입력 ---
default_code = dedent("""\
from vpython import *

scene.width  = 640
scene.height = 400
scene.background = color.white

b = box(size=vector(1,1,1), color=color.red)
w = 2*pi/3

while True:
    rate(60)
    b.rotate(angle=w*0.016, axis=vector(0,1,0))
""")

user_code = st.text_area("VPython 코드 (GlowScript 문법)", value=default_code, height=300)

col1, col2 = st.columns([1,1])
run_local = col1.button("⛔ (참고) 로컬-직접 실행 시도")  # CSP 때문에 보통 실패
publish = col2.button("🚀 Run & Publish to GitHub Pages")

# --- HTML 템플릿 (GlowScript 사전 컴파일 없이 실행형) ---
# 이건 Streamlit CSP 때문에 보통 실행이 막힙니다. (참고용)
RUNTIME_HTML = """\
<div id="glowscript" class="glowscript" style="outline:none;"></div>

<script src="https://www.glowscript.org/lib/jquery/2.1/jquery.min.js"></script>
<script src="https://www.glowscript.org/lib/jquery/2.1/jquery-ui.custom.min.js"></script>
<script src="https://www.glowscript.org/package/glow.3.2.min.js"></script>
<script src="https://www.glowscript.org/package/RScompiler.3.2.min.js"></script>
<script src="https://www.glowscript.org/package/RSrun.3.2.min.js"></script>
<script>
  window.__context = {{ glowscript_container: $("#glowscript").removeAttr("id") }};
</script>
<script type="text/python">
{code}
</script>
<style>html,body{{margin:0;padding:0}}</style>
"""

# --- GitHub Pages로 퍼블리시할 HTML (브라우저에서 실행형) ---
# GitHub Pages는 CSP 제약 없이 eval 허용되므로 정상동작
PUBLISH_HTML = """\
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="Referrer-Policy" content="no-referrer-when-downgrade" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>GlowScript VPython</title>
  <style>html,body{{margin:0;padding:0;background:#fff}}</style>
</head>
<body>
  <div id="glowscript" class="glowscript" style="outline:none;"></div>

  <script src="https://www.glowscript.org/lib/jquery/2.1/jquery.min.js"></script>
  <script src="https://www.glowscript.org/lib/jquery/2.1/jquery-ui.custom.min.js"></script>

  <script src="https://www.glowscript.org/package/glow.3.2.min.js"></script>
  <script src="https://www.glowscript.org/package/RScompiler.3.2.min.js"></script>
  <script src="https://www.glowscript.org/package/RSrun.3.2.min.js"></script>

  <script>
    window.__context = {{ glowscript_container: $("#glowscript").removeAttr("id") }};
  </script>

  <script type="text/python">
{code}
  </script>
</body>
</html>
"""

def build_filename():
    ts = dt.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return f"static/glowscript/gs_{ts}.html"  # 필요시 디렉토리 변경

def github_put_file(path:str, content_html:str, message:str):
    """
    GitHub Contents API를 사용해 파일 생성/업데이트.
    """
    token = st.secrets["GITHUB_TOKEN"]
    repo  = st.secrets["GITHUB_REPO"]
    branch= st.secrets.get("GITHUB_BRANCH", "main")

    api = f"https://api.github.com/repos/{repo}/contents/{path}"
    # 파일 존재 여부 확인(sha 필요할 수 있음)
    r = requests.get(api, headers={"Authorization": f"token {token}"}, params={"ref": branch})
    sha = r.json().get("sha") if r.status_code == 200 else None

    data = {
        "message": message,
        "content": base64.b64encode(content_html.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if sha:
        data["sha"] = sha

    r = requests.put(api, headers={"Authorization": f"token {token}"}, json=data)
    if r.status_code not in (200,201):
        raise RuntimeError(f"GitHub API 실패: {r.status_code} {r.text}")
    return r.json()

# ---------------- 실행 경로 A: (참고) 로컬-직접 실행 시도 ----------------
if run_local and user_code.strip():
    components.html(RUNTIME_HTML.format(code=user_code), height=540, scrolling=True)
    st.warning("Streamlit의 CSP 때문에 이 모드는 대부분의 배포환경에서 동작하지 않습니다. (개발/로컬에서만 가끔 성공)")

# ---------------- 실행 경로 B: GitHub Pages 퍼블리시 후 임베드 ----------------
if publish and user_code.strip():
    try:
        html = PUBLISH_HTML.format(code=user_code)
        path = build_filename()  # 예: static/glowscript/gs_20250101-123000.html
        commit_msg = f"Publish GlowScript: {path}"
        github_put_file(path, html, commit_msg)

        base = st.secrets["GITHUB_BASE"].rstrip("/")
        url  = f"{base}/{path}"
        st.success(f"✅ 퍼블리시 완료: {url}")

        # 바로 스트림릿에 임베드
        components.html(f'<iframe src="{url}" style="width:100%;height:560px;border:0;"></iframe>', height=580)

    except Exception as e:
        st.error(f"퍼블리시 실패: {e}")
        st.stop()

st.caption("팁: GitHub Pages 경로/브랜치 구조에 따라 PAGES_DIR(여기선 static/glowscript)을 조정하세요.")
