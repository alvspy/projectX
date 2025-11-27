import sqlite3
from config import data_base
from config import days


def throw_error(error="undefined error"):
    print(f"\033[31m{error}\033[0m")


def new_day(
    cls_id=None,
    cls=None,
    day="md",
    l1="",
    l2="",
    l3="",
    l4="",
    l5="",
    l6="",
    l7="",
    t1="",
    t2="",
    t3="",
    t4="",
    t5="",
    t6="",
    t7="",
):
    connection = sqlite3.connect(database=data_base)
    cursor = connection.cursor()
    if cls_id is None:
        if cls is None:
            throw_error("wrong class")
            return
        cursor.execute("SELECT id, number FROM Classes WHERE letter = ?", (cls[-1],))
        result = cursor.fetchall()
        for id, number in result:
            if number == int(cls[:-1]):
                cls_id = id
    if cls_id is None:
        throw_error("wrong class")
        return
    if cls is None:
        cursor.execute("SELECT letter, number FROM Classes WHERE id = ?", (cls_id,))
        result = cursor.fetchall()
        cls = str(result[1]) + result[0]
    if day not in days:
        throw_error("wrong day")
        return
    cursor.execute(
        f"""UPDATE {day}
                   SET _1 = ?, _2 = ?, _3 = ?, _4 = ?, _5 = ?, _6 = ?, _7 = ? 
                   WHERE cls_id = ?""",
        (l1, l2, l3, l4, l5, l6, l7, t1, t2, t3, t4, t5, t6, t7, cls_id),
    )
    connection.commit()


def show_day(cls, day):
    connection = sqlite3.connect(database=data_base)
    cursor = connection.cursor()
    cursor.execute(
        f"""SELECT l1, l2, l3, l4, l5, l6, l7, t1, t2, t3, t4, t5, t6, t7 FROM {day} WHERE cls = ?""",
        (cls,),
    )
    l1, l2, l3, l4, l5, l6, l7, t1, t2, t3, t4, t5, t6, t7 = cursor.fetchall()
    print(f"{l1}({t1})")
    print(f"{l2}({t2})")
    print(f"{l3}({t3})")
    print(f"{l4}({t4})")
    print(f"{l5}({t5})")
    print(f"{l6}({t6})")
    print(f"{l7}({t7})")
