from database import get_dict_tables
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


conn = psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'))
cur = conn.cursor()
task_status_dict, task_priority_dict, task_category_dict = get_dict_tables(cur)
conn.close()


def upload_category(combobox_cat):
    for category in task_category_dict.values():
        combobox_cat.addItem(category)


def upload_priority(combobox_pr):
    for priority in task_priority_dict.values():
        combobox_pr.addItem(priority)
