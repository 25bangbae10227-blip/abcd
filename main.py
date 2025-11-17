import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import altair as alt

# ---------------------------
# 0. 그룹명 자동 변환(중요!)
# ---------------------------
group_name_map = {
    "뉴진스": "NewJeans",
    "르세라핌": "Le_Sserafim",
    "세븐틴": "세븐틴_(음악_그룹)",
    "아이브": "Ive",
    "엔하이픈": "Enhypen",
    "에스파": "Aespa",
    "트와이스": "Twice",
}

def convert_group_name(name):
    return group_name_map.get(name, name)


# ---------------------------
# 1. 위키백과에서 데이터 수집
# ---------------------------
def get_album_data(group):
    group = convert_group_name(group)  # 🔥 자동 변환 추가됨
    url = f"https://ko.wikipedia.org/wiki/{group}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})

    album_list = []

    for table in tables:
        rows = table.find_all("tr")

        if not rows:
            continue

        headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]

        if not any(keyword in headers for keyword in ["판매", "앨범", "발매"]):
            continue

        for row in rows[1:]:
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) >= 2:
                album_list.append(cols[:3])

    if not album_list:
        return None

    return pd.DataFrame(album_list, columns=["앨범명", "발매일", "판매 관련 정보"])


# ---------------------------
# 2. Streamlit 화면
# ---------------------------
st.title("📀 아이돌 앨범 초동 판매량 정보")

group = st.text_input("아이돌 그룹 이름 입력 (예: 뉴진스, 아이브, 세븐틴)")

if st.button("데이터 가져오기"):
    with st.spinner("데이터 불러오는 중..."):
        df = get_album_data(group)

    if df is None:
        st.error("데이터를 찾을 수 없습니다! 위키백과에 페이지가 있는지 확인해 주세요.")
    else:
        st.success(f"'{group}' 데이터 가져오기 성공!")
        st.dataframe(df)
