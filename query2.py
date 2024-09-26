import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Google Sheets API와 통신할 수 있도록 자격 증명 설정
service_account_info = {
    "type": "service_account",
    "project_id": "sonic-shuttle-436809-s5",
    "private_key_id": "83ba96075115122e374dcb4423a8d4bcc5ebbfcb",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDVJhie3uS/kTMk
c9CeCeWEpUrASChE5bH65TKCMTrFnh4raf/v6U8l50k7kdkFt0k2l/tCsjcpqxMt
lJorpRv7a9qGEcPFWXnl3/hs6LXlpMQrSnYrKUxJqmRUg9F4cnW55rZ4FM0KpzVU
Qf2kJ9LJJuSLvbuGQR/Fk9tdLfr6Wd30qK0Ofa9aAXVqxAecm1f7JrnrEZPcfi8z
DT0CztAOLO1Ek9za4027C3W7UzLRVTzew5Bs6txFRqwlCNzTOhXt7XeWfZFFs4vx
qFIt1oJ9GkAPht39Jt7hGDypgBf1eiCyR1859qQThyttqBbwVhTo83YIpNzzUZx2
5gNHe3wRAgMBAAECggEAPiBSgMv65JNP0som/kloKpd7CDx/8ET68WQoqqXquXry
1DibLrRUK3oUcFZ8aRwZLN5zj+ceCPkiJ+DuZtZDJ68yDG3VIAqKayQy5puVmQ/D
VdLoSoBJCheuEqwxO+gwxDSo7qsxcG94LczmPxiUaaj6aHiu1dzZg98qyygBxUIw
D7nORGIvNBndBboBdGpQHijxEheCjUT5cqdRIa9JMRGvucxuGMY7d93B6OyA9va9
nAjYKQqTuQazgV+LDFEN4UYkeHxUnOzpXo8WZEGTCMEV24UdsB5Hb/6jgLjGO3Eg
uGB5YO57oxTWExYImmryJ/f5CxaKRdptFC8M7BLKuQKBgQD0EkW/ojg4tPqku4SE
ktvrep6nyGxkb/xiFEeRG4V19leX/MggalxDdCv4HKjlFSYSVQxjk+cAspDft5Df
1CII+3DktNrXlaaak1yxmJHoaU2cuLJynDmNPsJNZVgSu+qLLuoZTMtZZMcyzVNL
nF3x1QIb3iPnMqnzvnh0uEKNFwKBgQDfkO61KO9Zc6rIpiXfNaerN0Nv/LzDgKtq
3RfoThlcqVZvUEN+1DtlwXuESON6GhuJ0F0IUOyHSA6JqL5y7wKvgYJ5VEpJNBdC
G4WXKDSAou2m16JcdZfLgYAabavTviOyp7h9GJDXrLu4g2+Ff7f2OTKooeRbF1rT
62Evhq0JFwKBgQDETw4anHdr5OTUKp7jotuQAwgpG2NTRV9R483MQL6Pqpu5e2/b
4rBi8MWMwkB2QRRmGlHkpclfHkC4MAUugoj9gH/E9FIwpAVkvrIHhheVP11VeJjO
5ijEGn5dke3M46g6Wnmf78x/EjfF/K/KWPKW2CTiFUH7axyXF9P6zVl58QKBgGYN
ZqnTkc6neiI1lbwaZftGMsZ//DrSFW2mly8312Pw+L+/R9AxWRvOAnAURaKLIF78
ejs9lXr7bYdxO96DNBqhZ8myrGZWHPfUUFr7w1ulBA7RCBBkrXH8H1nxDiqN9QWs
gg64lAWfl+FWPiYWcwc2fOV1YSQjuRZbr/Vd6MbpAoGAGdm+zmVDOjARVqjEY0K0
c7fKjKBWJ7J5v+H1lJYhaTVKbZ3rWKM6D/bK+6wl6ZffqY93DZ5g1FgoWWmSl3ga
I/Cw3Wn0RNw5vEYLmB3n1oseNsrpxFownqoJdpKAftCf1VUstKD/JN+VarZHIHnu
VzELmhurwlc9pghInPlbf10=
-----END PRIVATE KEY-----""",
    "client_email": "koms-928@sonic-shuttle-436809-s5.iam.gserviceaccount.com",
    "client_id": "105480077311693659014",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/koms-928%40sonic-shuttle-436809-s5.iam.gserviceaccount.com"
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
