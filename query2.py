import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Google Sheets API와 통신할 수 있도록 자격 증명 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('path_to_your_service_account.json', scopes=scope)

# Google Sheets에 연결
client = gspread.authorize(creds)

# 스프레드시트 열기 (Google Sheets URL이나 ID로 스프레드시트 열기)
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/xxxxxxx/edit#gid=0")

# 첫 번째 워크시트 가져오기
worksheet = spreadsheet.sheet1

# 워크시트에서 모든 데이터 가져오기
data = worksheet.get_all_records()

# 데이터프레임으로 변환
df = pd.DataFrame(data)

# 결과 출력
st.write(df)

