from database import get_dict_tables, save_category
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


conn = psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'))
cur = conn.cursor()
task_status_dict, task_priority_dict, task_category_dict = get_dict_tables(cur)
conn.close()


def upload_category(combobox):
    combobox.clear()
    for category in task_category_dict.values():
        combobox.addItem(category)


def upload_priority(combobox):
    combobox.clear()
    for priority in task_priority_dict.values():
        combobox.addItem(priority)


def save_new_category(name):
    conn = psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'))
    cur = conn.cursor()
    save_category(cur, name)
    conn.commit()
    global task_category_dict
    _, _, task_category_dict = get_dict_tables(cur)
    conn.close()
