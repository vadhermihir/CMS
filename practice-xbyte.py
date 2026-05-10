import mysql.connector
from datetime import datetime, timedelta, date

from django.db.models.sql.compiler import cursor_iter

today=date.today()
db_name=f"{today.year}_{today.month}_{today.day}"

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

if conn.is_connected():
    print("Database Successfully Connected")
else:
    print("not Connected")

cursor=conn.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
