import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import altair as alt

# ---------------------------
# 1. 웹페이지 제목
# ---------------------------
st.title("📀 아이돌 앨범 초동 판매량 사이트")
st.write("위키백과에서 데이터를 수집해 표시하는 사이트입니다!")

# ---------------------------
# 2. 위키백과에서 데이터 수집 함수
# ---------------------------
def get_album_data(group):
    url = f"https://ko.wikipedia.org/wiki/{group}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})

    album_list = []

    for table in tables:
        rows = table.find_all("tr")

        # 첫 번째 행 = 열 제목
        headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]

        # "발매일" "앨범" "판매량" 같은 정보가 있는 표만 사용
        if not any(keyword in headers for keyword in ["판매", "앨범", "발매"]):
            continue

        # 나머지 행들 = 실제 데이터
        for row in rows[1:]:
            cols = [td.get_text(strip=True) for td in row.find_all("td")]

            if len(cols) >= 2:
                album_list.append(cols[:3])  # 앞 3개 열만 사용

    if not album_list:
        return None

    df = pd.DataFrame(album_list, columns=["앨범명", "발매일", "판매 관련 정보"])
    return df


# ---------------------------
# 3. 검색 기능
# ---------------------------
st.subheader("🔍 아이돌 그룹 검색하여 데이터 모으기")

group_name = st.text_input("아이돌 그룹 이름을 입력하세요 (예: 뉴진스, 아이브, 세븐틴 등)")

if st.button("데이터 가져오기"):
    with st.spinner("데이터 수집 중..."):
        df = get_album_data(group_name)

        if df is None:
            st.error("데이터를 찾을 수 없습니다. 위키백과에 정보가 있는 그룹인지 확인해 주세요!")
        else:
            st.success(f"'{group_name}' 데이터 가져오기 성공!")
            st.dataframe(df)

            # ---------------------------
            # 4. 판매량 숫자만 추출해 그래프 만들기
            # ---------------------------
            # 판매량에 숫자 있는 행만 필터링
            df_sales = df[df["판매 관련 정보"].str.contains(r"\d", na=False)]

            # 숫자만 추출 (예: '100만 장' → 100)
            df_sales["판매량(추정)"] = (
                df_sales["판매 관련 정보"]
                .str.replace(",", "")
                .str.extract(r"(\d+)")
                .astype(float)
            )

            # 판매량 데이터가 있다면 그래프 표시
            if df_sales["판매량(추정)"].notnull().sum() > 0:
                st.subheader("📈 판매량 그래프")

                chart = (
                    alt.Chart(df_sales)
                    .mark_bar()
                    .encode(
                        x="앨범명",
                        y="판매량(추정)",
                        color="앨범명"
                    )
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("판매량 숫자를 가진 데이터가 없어 그래프를 만들 수 없습니다.")
