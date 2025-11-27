import sqlite3
from config import cur_year
from config import data_base

connecton = sqlite3.connect(database=data_base)
cursor = connecton.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS Mails
(
id,
name TEXT,
surname TEXT,
cls TEXT
)"""
)

file = open("users.txt", "r", encoding="utf8")
st = set()
n = 0

s = file.readline()
while s != "":
    a = s.split()
    mail, surname, name = a
    number = int(mail[1:3])
    if (surname, name, number) in st:
        print(s)
    cursor.execute(f"""INSERT INTO Mails id, name, surname, """)
    st.add((surname, name, number))
    s = file.readline()
    n += 1
