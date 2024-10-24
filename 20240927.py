import random
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from data_as_python import data
import time

# 대시보드 만들기
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")
st.header("2023년도 중소기업 혁신바우처 사업", divider="gray")
st.markdown("##")  # 화면상에서 시각적인 구분을 위한 여백

# 데이터 프레임으로 변환
df = pd.DataFrame(data)

# side bar
df.set_index("기업명", inplace=True)
st.sidebar.image("BS 22 엠블럼.png", caption="2023년도 성과분석 결과")

# CSS 사용
st.markdown("""
    <style>
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #00215E !important;
        color: white !important;
    }
    div[data-testid="metric-container"] {
            justify-content: left !important;
            text-align: left !important;
    }
    div[data-testid="metric-container"] > div {
            font-size: 17px !important;
    }
    div[data-testid="metric-container"] > div:nth-child(2) {
            justify-content: left !important;
            text-align: left !important;}
    </style>
    """, unsafe_allow_html=True)

# 필터
st.sidebar.header("FILTER")

진행상황 = st.sidebar.multiselect(
    "진행상황 선택",
    options=df["진행상황"].unique(),
    default=df["진행상황"].unique(),
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

소재지 = st.sidebar.multiselect(
    "소재지 선택",
    options=df["소재지"].unique(),
    default=df["소재지"].unique(),
)

# 필터링된 데이터
df_selection = df.query(
    "진행상황==@진행상황 & 컨설팅지원==@컨설팅지원 & 기술지원==@기술지원 & 마케팅지원==@마케팅지원 & 소재지==@소재지"
)

# 숫자 변환 및 결측값 처리 함수
def convert_to_numeric(column):
    return pd.to_numeric(df_selection[column], errors='coerce').fillna(0)

# Home 함수 (상단에 테이블이나 메트릭 등을 표시하는 부분)
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
    일인당매출액 = 매출액_2023년_numeric.sum() / 종업원수_2023년_numeric.sum()
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

# 그래프와 테이블을 좌우로 나눈 두 개의 탭을 한 줄에 배치
def graph_and_table_row():
    # 첫 번째 줄
    left1, right1 = st.columns(2)

    with left1:
        tab1, tab2 = st.tabs(["Graph", "Table"])
        with tab1:
            sales_by_type = df_selection.groupby(by=["컨설팅지원"]).count()[["매출액_2023년"]].sort_values(by="매출액_2023년")
            fig_sales = px.bar(
                sales_by_type,
                x="매출액_2023년",
                y=sales_by_type.index,
                orientation="h",
                title="컨설팅지원별 2023년도 매출액",
                color_discrete_sequence=["#6B8A7A"] * len(sales_by_type),
                template="plotly_white",
            )
            fig_sales.update_layout(
                xaxis_title="총 매출액(백만원)",
                yaxis_title="지원 종류",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False),
                title_font_size=20,
            )
            st.plotly_chart(fig_sales, use_container_width=True)
        with tab2:
            st.subheader("컨설팅지원별 데이터")
            st.dataframe(df_selection[["컨설팅지원", "매출액_2023년"]])

    with right1:
        tab3, tab4 = st.tabs(["Graph", "Table"])
        with tab3:
            sales_by_tech = df_selection.groupby(by=["기술지원"]).count()[["매출액_2023년"]].sort_values(by="매출액_2023년")
            fig_tech = px.bar(
                sales_by_tech,
                x="매출액_2023년",
                y=sales_by_tech.index,
                orientation="h",
                title="기술지원별 2023년도 매출액",
                color_discrete_sequence=["#6295A2"] * len(sales_by_tech),
                template="plotly_white",
            )
            fig_tech.update_layout(
                xaxis_title="총 매출액(백만원)",
                yaxis_title="지원 종류",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False),
                title_font_size=20,
            )
            st.plotly_chart(fig_tech, use_container_width=True)
        with tab4:
            st.subheader("기술지원별 데이터")
            st.dataframe(df_selection[["기술지원", "매출액_2023년"]])

    # 두 번째 줄
    left2, right2 = st.columns(2)

    with left2:
        tab5, tab6 = st.tabs(["Graph", "Table"])
        with tab5:
            sales_by_marketing = df_selection.groupby(by=["마케팅지원"]).count()[["매출액_2023년"]].sort_values(by="매출액_2023년")
            fig_marketing = px.bar(
                sales_by_marketing,
                x="매출액_2023년",
                y=sales_by_marketing.index,
                orientation="h",
                title="마케팅지원별 2023년도 매출액",
                color_discrete_sequence=["#40A578"] * len(sales_by_marketing),
                template="plotly_white",
            )
            fig_marketing.update_layout(
                xaxis_title="총 매출액(백만원)",
                yaxis_title="지원 종류",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False),
                title_font_size=20,
            )
            st.plotly_chart(fig_marketing, use_container_width=True)
        with tab6:
            st.subheader("마케팅지원별 데이터")
            st.dataframe(df_selection[["마케팅지원", "매출액_2023년"]])

    with right2:
        tab7, tab8 = st.tabs(["Graph", "Table"])
        with tab7:
            sales_location = df_selection.groupby(by=["소재지"]).sum(numeric_only=True)[["매출액_2023년"]]
            fig_location = px.bar(
                sales_location,
                x=sales_location.index,
                y="매출액_2023년",
                title="소재지별 2023년도 매출액",
                template="plotly_white",
                color_discrete_sequence=["#0A6847"],
                hover_data={"매출액_2023년": ":,.0f"},
            )
            fig_location.update_layout(
                xaxis_title="소재지",
                yaxis_title="총 매출액(백만원)",
                xaxis=dict(tickmode="linear"),
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(showgrid=False),
                title_font_size=20,
            )
            st.plotly_chart(fig_location, use_container_width=True)
        with tab8:
            st.subheader("소재지별 데이터")
            st.dataframe(df_selection[["소재지", "매출액_2023년"]])

graph_and_table_row()
