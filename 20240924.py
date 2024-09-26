import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query2 import *
import time

# 대시보드 만들기
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")
st.subheader("2023년도 중소기업 혁신바우처 사업")
st.markdown("##")  # 화면상에서 시각적인 구분을 위해 여백을 넣는 효과

# fetch data
result = view_all_data()
df = pd.DataFrame(result, columns=["소재지", "진행상황", "컨설팅지원", "기술지원", "마케팅지원", 
                                   "매출액_2021년", "매출액_2022년", "매출액_2023년",
                                   "1인당매출액_2022년", "1인당매출액_2023년",
                                   "영업이익_2021년", "영업이익_2022년", "영업이익_2023년",
                                   "종업원수_2021년", "종업원수_2022년", "종업원수_2023년",
                                   "매출액증가율_2022년", "매출액증가율_2023년", 
                                   "영업이익율_2022년", "영업이익율_2023년",
                                   "고용증가율_2022년", "고용증가율_2023년"])

# st.dataframe(df)

# side bar
st.sidebar.image("D:\Python\Streamlit\BS 22 엠블럼.png", caption="2023년도 성과분석 결과")

# switcher
# CSS로 multiselect 스타일링
st.markdown("""
    <style>
    /* multiselect 선택된 항목 배경색을 navy로 변경 */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: navy !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
# switcher
st.sidebar.header("FILTER")
소재지 = st.sidebar.multiselect(
    "소재지 선택",
    options=df["소재지"].unique(),
    default=df["소재지"].unique(),
)
컨설팅지원 = st.sidebar.multiselect(
    "컨설팅지원 선택",
    options=df["컨설팅지원"].unique(),
    default=df["컨설팅지원"].unique(),
)
기술지원 = st.sidebar.multiselect(
    "기술지원 선택",
    options=df["기술지원"].unique(),
    default=df["기술지원"].unique(),
)
마케팅지원 = st.sidebar.multiselect(
    "마케팅지원 선택",
    options=df["마케팅지원"].unique(),
    default=df["마케팅지원"].unique(),
)
df_selection = df.query(
    "소재지==@소재지 & 컨설팅지원==@컨설팅지원 & 기술지원==@기술지원 & 마케팅지원==@마케팅지원"
)

# 숫자 변환 및 결측값 처리 함수
def convert_to_numeric(column):
    return pd.to_numeric(df_selection[column], errors='coerce').fillna(0)

# Home 함수
def Home():
    with st.expander("Tabular"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=[])
        st.write(df_selection[showData])

    # 숫자로 변환 후 계산
    매출액_2023년_numeric = convert_to_numeric("매출액_2023년")
    일인당매출액_2023년_numeric = convert_to_numeric("1인당매출액_2023년")
    영업이익_2023년_numeric = convert_to_numeric("영업이익_2023년")
    종업원수_2023년_numeric = convert_to_numeric("종업원수_2023년")

    총매출액 = 매출액_2023년_numeric.sum()
    매출액 = 매출액_2023년_numeric.mean()
    일인당매출액 = 일인당매출액_2023년_numeric.mean()
    영업이익 = 영업이익_2023년_numeric.sum()
    종업원수 = 종업원수_2023년_numeric.sum()

    total1, total2, total3, total4, total5 = st.columns(5, gap='large')
    with total1:
        st.info('총 매출액', icon="➕")
        st.metric(label="2023년 총합(단위: 백만원)", value=f"{총매출액:,.0f}")
    with total2:
        st.info('매출액', icon="📐")
        st.metric(label="2023년 평균(단위: 백만원)", value=f"{매출액:,.0f}")

    with total3:
        st.info('일인당매출액', icon="📐")
        st.metric(label="2023년 평균(단위: 백만원)", value=f"{일인당매출액:,.0f}")

    with total4:
        st.info('영업이익', icon="➕")
        st.metric(label="2023년 총합(단위: 백만원)", value=f"{영업이익:,.0f}")

    with total5:
        st.info('종업원수', icon="➕")
        st.metric(label="2023년 총합(단위: 명)", value=f"{종업원수:,.0f}")

    st.markdown("""---""")

Home()

# graph 함수
def graph():
    # 평균을 먼저 계산하고 그 후에 반올림
    total_sales = round(df_selection["매출액_2023년"].mean(), 2)

    # simple bar graph(컨설팅)
    sales_by_type = (
        df_selection.groupby(by=["컨설팅지원"]).count()[["매출액_2023년"]].sort_values(by="매출액_2023년")
    )
    fig_sales = px.bar(
        sales_by_type,
        x="매출액_2023년",
        y=sales_by_type.index,
        orientation="h",
        title="<b> 컨설팅지원별 2023년도 매출액 </b>",
        color_discrete_sequence=["#0083b8"] * len(sales_by_type),
        template="plotly_white",
    )

    fig_sales.update_layout(
        xaxis_title="매출액(백만원)",
        yaxis_title="지원 종류",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        title_font_size=20,
    )
    # simple bar graph(기술지원)
    sales_by_tech = (
        df_selection.groupby(by=["기술지원"]).count()[["매출액_2023년"]].sort_values(by="매출액_2023년")
    )
    fig_tech = px.bar(
        sales_by_tech,
        x="매출액_2023년",
        y=sales_by_tech.index,
        orientation="h",
        title="<b> 기술지원별 2023년도 매출액 </b>",
        color_discrete_sequence=["#0083b8"] * len(sales_by_tech),
        template="plotly_white",
    )

    fig_tech.update_layout(
        xaxis_title="매출액(백만원)",
        yaxis_title="지원 종류",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        title_font_size=20,
    )   
    # simple bar graph(마케팅지원)
    sales_by_marketing = (
        df_selection.groupby(by=["마케팅지원"]).count()[["매출액_2023년"]].sort_values(by="매출액_2023년")
    )
    fig_marketing = px.bar(
        sales_by_marketing,
        x="매출액_2023년",
        y=sales_by_marketing.index,
        orientation="h",
        title="<b> 마케팅지원별 2023년도 매출액 </b>",
        color_discrete_sequence=["#0083b8"] * len(sales_by_marketing),
        template="plotly_white",
    )

    fig_marketing.update_layout(
        xaxis_title="매출액(백만원)",
        yaxis_title="지원 종류",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        title_font_size=20,
    )

    # simple bar graph(소재지)
    sales_location = df_selection.groupby(by=["소재지"]).sum(numeric_only=True)[["매출액_2023년"]]
    fig_location = px.area(
        sales_location,
        x=sales_location.index, 
        y="매출액_2023년",
        title="<b> 소재지별 2023년도 매출액 </b>",
        template="plotly_white",
        color_discrete_sequence=["#1f77b4"],
        hover_data={"매출액_2023년": ":,.0f"},
    )

    fig_location.update_layout(
        xaxis_title="소재지",
        yaxis_title="매출액(백만원)",
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)", #배경 투명화
        yaxis=dict(showgrid=False),
        title_font_size=20,  # 제목 글꼴 크기
    )


    left, right = st.columns(2)
    right.plotly_chart(fig_tech, use_container_width=True)
    right.plotly_chart(fig_location, use_container_width=True)
    left.plotly_chart(fig_sales, use_container_width=True)
    left.plotly_chart(fig_marketing, use_container_width=True)

graph()