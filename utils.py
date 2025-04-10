from database import get_dict_tables, save_category, Task
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
    save_category(name)
    global task_category_dict
    _, _, task_category_dict = get_dict_tables(cur)



def save_task(name, priority, category, descrirton, deadline = None, replay = None):
    conn = psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'))
    cur = conn.cursor()
    global task_priority_dict, task_category_dict
    cat_id = list(filter(lambda x: x[1] == category, task_category_dict.items()))[0][0]
    prior_id = list(filter(lambda x: x[1] == priority, task_priority_dict.items()))[0][0]

    new_task = Task(name=name, description=descrirton,
                    priority_id=prior_id, category_id=cat_id)
    new_task.save_task(cur)
    conn.commit()

    conn.close()



