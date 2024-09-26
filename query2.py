import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd

# Google Sheets API와 통신할 수 있도록 자격 증명 설정
service_account_info = {
    "type": st.secrets["google"]["type"],
    "project_id": st.secrets["google"]["project_id"],
    "private_key_id": st.secrets["google"]["private_key_id"],
    "private_key": st.secrets["google"]["private_key"],
    "client_email": st.secrets["google"]["client_email"],
    "client_id": st.secrets["google"]["client_id"],
    "auth_uri": st.secrets["google"]["auth_uri"],
    "token_uri": st.secrets["google"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["google"]["client_x509_cert_url"]
}

# 자격 증명 생성
creds = Credentials.from_service_account_info(service_account_info)

# Google Sheets에 연결
client = gspread.authorize(creds)

# 스프레드시트 열기 (Google Sheets URL이나 ID로 스프레드시트 열기)
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1rsMwe-x7ZHgs-hk-HGj9GEr3av_aCl2ts7EMyZmOwjY/edit?usp=sharing")

# 첫 번째 워크시트 가져오기
worksheet = spreadsheet.sheet1

# 워크시트에서 모든 데이터 가져오기
data = worksheet.get_all_records()

# 데이터프레임으로 변환하는 함수
def view_all_data():
    return pd.DataFrame(data)
