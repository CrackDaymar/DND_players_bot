from setting import connections_params
from loguru import logger
import psycopg2
from exeptions import NotCorrectCharacters, NotCorrectValues, FailedToConnectDB

logger.add('info.log', format="{time} {level} {message}",
           level='INFO', rotation="10KB", compression='zip')


def connect_db():
    try:
        conn = psycopg2.connect(**connections_params)
        return conn
    except FailedToConnectDB:
        return None


class characters():
    def __init__(self, name: str = None, heal_point_max: int = 0, telegram_id="797523735",
                 current_hp: int = 0):
        pass


def create_new_character(name: str, max_hp: int, telegramm_id: str):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO characters (name, max_hp, curr_hp, telegram_id) VALUES (%s, %s, %s, %s)"
        data = (name, max_hp, max_hp, telegramm_id)
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except NotCorrectCharacters:
        cursor.close()
        conn.close()
        return False


def find_characters(name: str):
    conn = connect_db()
    cursor = conn.cursor()
    sql = f"SELECT * FROM characters WHERE name = '{name}'"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def take_all_characters():
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM characters"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def take_curr_hp(name):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        sql = f"SELECT curr_hp FROM characters WHERE name = '{name}'"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data[0][0]
    except NotCorrectCharacters:
        pass
    cursor.close()
    conn.close()


def change_characters_current_hp(name: str, change_hp: int):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        curr_hp = take_curr_hp(name)
        new_hp = curr_hp - int(change_hp)
        sql = f"UPDATE characters SET curr_hp = {new_hp} WHERE name = '{name}'"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return new_hp
    except NotCorrectValues:
        cursor.close()
        conn.close()
        return None


def update_curr_hp():
    conn = connect_db()
    cursor = conn.cursor()
    sql = "UPDATE characters SET curr_hp = max_hp"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return True


def delete_characters(name: str):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        sql = f"DELETE FROM characters WHERE name = '{name}'"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except NotCorrectCharacters:
        cursor.close()
        conn.close()
        return False