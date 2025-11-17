import streamlit as st
import pandas as pd
import altair as alt

st.title("📀 아이돌 앨범 초동 판매량 사이트")

# CSV로 만든 데이터 불러오기
data = {
    "그룹": ["뉴진스", "아이브", "세븐틴", "르세라핌"],
    "앨범명": ["Get Up", "I've IVE", "FML", "UNFORGIVEN"],
    "초동판매량": [169, 110, 454, 125]
}
df = pd.DataFrame(data)

st.subheader("📋 데이터 표")
st.dataframe(df)

st.subheader("📈 판매량 차트")
chart = alt.Chart(df).mark_bar().encode(
    x="그룹",
    y="초동판매량",
    color="그룹"
)
st.altair_chart(chart, use_container_width=True)

