import mysql.connector
import streamlit as Dashboard

#connection

conn = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    passwd = "",
    db = "myDb"
)
c=conn.cursor()

#fetch
def view_all_data():
    c.execute('SELECT * FROM data_20240925')
    data = c.fetchall()
    print(data)
    return data