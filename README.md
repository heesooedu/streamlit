# Streamlit × GlowScript VPython Demo


브라우저에서 실행되는 GlowScript(Web VPython)를 Streamlit 앱 안에 임베드하는 예제입니다.
Streamlit Cloud와 같이 CDN 접근이 제한된 환경에서도 동작하도록 GlowScript 런타임 스크립트를 저장소에 함께 두고,
필요 시 인라인으로 삽입할 수 있는 옵션을 제공합니다.

## 주요 기능

- Streamlit UI에서 VPython 코드를 작성하고 즉시 미리보기
- GlowScript 자산 로딩 방식을 선택(CDN 혹은 저장소에 포함된 스크립트 인라인)
- 생성된 HTML을 다운로드하여 직접 배포하거나, GitHub API를 통해 지정한 리포지토리에 업로드
- GitHub Pages URL을 즉시 iframe으로 임베드하여 배포 결과 확인


## 로컬 실행
```bash
# 1) 가상환경(선택)
python -m venv .venv && source .venv/bin/activate # Windows: .venv\\Scripts\\activate


# 2) 의존성 설치
pip install -r requirements.txt


# 3) 실행
streamlit run app.py
```

## Streamlit Cloud에서 사용하기

1. 앱 배포 전 `secrets.toml`에 다음 키를 설정합니다.
   - `GITHUB_TOKEN`: 파일 업로드 권한이 있는 Personal Access Token
   - `GITHUB_REPO`: 예) `username/repo`
   - `GITHUB_BRANCH`: 업로드할 브랜치 (기본값 `main`)
   - `GITHUB_BASE`: GitHub Pages 혹은 정적 호스팅의 베이스 URL
2. 앱 우측 패널에서 "GlowScript 자원 로딩 방식"을 `저장소의 GlowScript 라이브러리 인라인`으로 설정하면,
   외부 CDN 접근이 어려울 때도 저장소에 포함된 스크립트로 실행됩니다.
3. 미리보기 하단의 "HTML 파일 다운로드" 버튼으로 결과를 내려받아 직접 업로드할 수도 있습니다.
