import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------
# 1. 페이지 제목
# ---------------------------
st.title("📀 아이돌 앨범 초동 판매량 사이트")
st.write("여기는 아이돌 음반의 초동 판매량을 보여주는 사이트입니다!")

# ---------------------------
# 2. 데이터 예시 (직접 수정 가능)
# ---------------------------
data = {
    "그룹": ["뉴진스", "아이브", "엔시티드림", "세븐틴", "르세라핌"],
    "앨범명": ["Get Up", "I've IVE", "ISTJ", "FML", "UNFORGIVEN"],
    "초동판매량(만 장)": [169, 110, 373, 454, 125]
}

df = pd.DataFrame(data)

st.subheader("📊 아이돌 초동 판매량 표")
st.dataframe(df)

# ---------------------------
# 3. 차트 시각화
# ---------------------------
st.subheader("📈 초동 판매량 차트")

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="그룹",
        y="초동판매량(만 장)",
        color="그룹"
    )
)

st.altair_chart(chart, use_container_width=True)

# ---------------------------
# 4. 사용자 입력 기능 추가 (원한다면)
# ---------------------------
st.subheader("➕ 새로운 데이터 추가하기")

with st.form("add_data_form"):
    new_group = st.text_input("그룹 이름")
    new_album = st.text_input("앨범명")
    new_sales = st.number_input("초동판매량(만 장)", min_value=0)

    submitted = st.form_submit_button("추가하기")

    if submitted:
        st.success(f"{new_group} 추가 완료! (저장 기능은 추가 구현 필요)")
