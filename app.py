import io, time
import pandas as pd
import numpy as np
import streamlit as st

# (선택) GitHub 저장용
USE_GITHUB = False
try:
    from github import Github
    USE_GITHUB = True
except:
    USE_GITHUB = False

st.set_page_config(page_title="Sim Hub", layout="wide")

st.title("Sim Hub — Web VPython 데이터 업로드/시각화/다운로드")

with st.sidebar:
    st.markdown("### 1) Glowscript에서 CSV 다운")
    st.markdown("- 시뮬레이션 끝나면 **CSV 다운로드 링크** 클릭")
    st.markdown("### 2) 여기로 업로드")
    st.markdown("- 여러 파일 한번에 가능")
    st.markdown("### 3) 그래프/가공/다운로드")
    st.markdown("### (선택) GitHub 저장")
    st.markdown("- `Secrets`에 토큰 넣으면 버튼 활성화")

uploaded = st.file_uploader("CSV 파일 업로드 (여러 개 가능)", type=["csv"], accept_multiple_files=True)

def auto_parse_csv(file):
    df = pd.read_csv(file)
    # 숫자 컬럼 자동 캐스팅
    for c in df.columns:
        try:
            df[c] = pd.to_numeric(df[c])
        except:
            pass
    return df

if uploaded:
    tabs = st.tabs([f"{f.name}" for f in uploaded])

    for file, tab in zip(uploaded, tabs):
        with tab:
            df = auto_parse_csv(file)

            st.subheader("원본 미리보기")
            st.dataframe(df.head(50), use_container_width=True)

            # 시간열 감지
            time_cols = [c for c in df.columns if c.lower() in ("t","time","t_sec","time_s")]
            default_t = time_cols[0] if time_cols else None
            tcol = st.selectbox("시간 열 선택", [None] + list(df.columns), index=(0 if default_t is None else (1 + list(df.columns).index(default_t))))
            ycols = st.multiselect("값(여러 열 선택 가능, 라인 그래프)", [c for c in df.columns if c != tcol],
                                   default=[c for c in df.columns if c != tcol][:1])

            # 파생량(속도/가속도) 계산 옵션
            make_derivatives = st.checkbox("파생량 생성: 속도/가속도", value=bool(tcol and len(ycols)>0))
            if make_derivatives and tcol:
                try:
                    tvals = df[tcol].to_numpy()
                    for yc in ycols:
                        y = df[yc].to_numpy()
                        v = np.gradient(y, tvals)
                        a = np.gradient(v, tvals)
                        df[f"{yc}_v"] = v
                        df[f"{yc}_a"] = a
                except Exception as e:
                    st.info(f"파생량 계산 스킵: {e}")

            # 리샘플링/스무딩
            with st.expander("전처리 옵션"):
                resample = st.checkbox("균일 dt로 리샘플", value=False, help="불균일 시간 간격 → 균일 시계열")
                sg = st.checkbox("Savitzky-Golay 스무딩", value=False)
                if resample and tcol:
                    dt = st.number_input("목표 dt (초)", min_value=0.0001, value=0.01, step=0.01, format="%.4f")
                    tmin, tmax = float(df[tcol].min()), float(df[tcol].max())
                    new_t = np.arange(tmin, tmax+dt/2, dt)
                    df = df.sort_values(tcol)
                    df_int = {tcol: new_t}
                    for c in df.columns:
                        if c == tcol: continue
                        try:
                            df_int[c] = np.interp(new_t, df[tcol], df[c])
                        except:
                            df_int[c] = np.nan
                    df = pd.DataFrame(df_int)

                if sg:
                    try:
                        from scipy.signal import savgol_filter
                        win = st.slider("윈도우(홀수)", 5, 101, 21, step=2)
                        poly = st.slider("다항차수", 1, 5, 3)
                        for c in df.columns:
                            if c == tcol: continue
                            if pd.api.types.is_numeric_dtype(df[c]):
                                df[c] = savgol_filter(df[c], window_length=min(win, len(df[c])//2*2-1), polyorder=min(poly, 5))
                    except Exception:
                        st.warning("`scipy`가 없으면 스무딩은 비활성입니다. (requirements에 scipy 추가 가능)")

            st.subheader("그래프")
            if tcol and ycols:
                import altair as alt
                base = alt.Chart(df).transform_fold(
                    ycols, as_=['series','value']
                )
                chart = base.mark_line().encode(
                    x=alt.X(f"{tcol}:Q", title=tcol),
                    y=alt.Y("value:Q", title="value"),
                    color="series:N",
                    tooltip=[tcol, "series:N", "value:Q"]
                ).interactive()
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("시간 열과 값 열을 선택하면 그래프가 표시됩니다.")

            # 다운로드
            st.subheader("가공 데이터 다운로드")
            save_name = st.text_input("파일명", value=file.name.replace(".csv","") + "_processed.csv")
            st.download_button("CSV 다운로드", data=df.to_csv(index=False).encode("utf-8"), file_name=save_name, mime="text/csv")

            # (선택) GitHub 저장
            st.subheader("GitHub 저장 (선택)")
            if USE_GITHUB and "github" in st.secrets:
                repo_name = st.secrets["github"].get("repo")
                branch    = st.secrets["github"].get("branch","main")
                token     = st.secrets["github"].get("token")
                subdir    = st.secrets["github"].get("subdir","data")
                if repo_name and token:
                    if st.button(f"GitHub에 `{subdir}/{save_name}`로 저장"):
                        try:
                            gh = Github(token)
                            repo = gh.get_repo(repo_name)
                            path = f"{subdir}/{save_name}"
                            content = df.to_csv(index=False)
                            msg = f"Add {path} via Streamlit ({time.strftime('%Y-%m-%d %H:%M:%S')})"
                            # 파일 존재여부 체크 → 있으면 update, 없으면 create
                            try:
                                existing = repo.get_contents(path, ref=branch)
                                repo.update_file(path, msg, content, existing.sha, branch=branch)
                            except Exception:
                                repo.create_file(path, msg, content, branch=branch)
                            st.success(f"Saved to GitHub: {repo_name}/{path}")
                        except Exception as e:
                            st.error(f"GitHub 저장 실패: {e}")
                else:
                    st.info("Streamlit Secrets에 `[github] token/repo/branch/subdir`를 설정하세요.")
            else:
                st.info("PyGithub 또는 GitHub secrets가 없어서 'GitHub 저장' 버튼을 비활성화했습니다.")
else:
    st.info("왼쪽 사이드바 안내를 따라 CSV를 업로드하세요.")
