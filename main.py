from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()



conn = psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'))


class Task:
    __task_status_categories = ('Запланировано', 'Делаю', 'Сделано')
    __task_priorities = ('Низкий', 'Средний', 'Высокий')
    __task_category = ('Общее', 'Учеба', 'Работа', 'Дом', 'Здоровье', 'Хобби', 'Финансы', 'Проекты')

    def __init__(self, name, description="", priority_id=1, deadline=None, category_id=0):
        self.name = name
        self.priority = priority_id
        self.task_category = category_id
        self.description = description
        self.task_status = 1
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None
        self.repeat = None
        self.timer = None

    def __str__(self):
        return f"{self.name} ({self.priority}) - {self.task_status}"

    def copy_task(self):
        ...

    # def __deepcopy__

    def start_timer(self):
        ...

    def save_task(self):
        ...

    def change_task(self):
        ...


def crete_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS task (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    priority_id INTEGER REFERENCES task_priority(id),
    status_id INTEGER REFERENCES task_status(id),
    category_id INTEGER REFERENCES task_category(id),
    deadline DATE);
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS task_status (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL);
    """)

    for name in ('Запланировано', 'Делаю', 'Сделано'):
        cur.execute('''
            INSERT INTO task_status (name)
            SELECT %s
            WHERE NOT EXISTS (SELECT 1 FROM task_status WHERE name = %s)
        ''', (name, name))

    cur.execute("""
    CREATE TABLE IF NOT EXISTS task_priority (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL);
    """)

    for name in ('Низкий', 'Средний', 'Высокий'):
        cur.execute('''
            INSERT INTO task_priority (name)
            SELECT %s
            WHERE NOT EXISTS (SELECT 1 FROM task_priority WHERE name = %s)
        ''', (name, name))

    cur.execute("""
    CREATE TABLE IF NOT EXISTS task_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL);
    """)

    for name in ('Общее', 'Учеба', 'Работа', 'Дом', 'Здоровье', 'Хобби', 'Финансы', 'Проекты'):
        cur.execute('''
            INSERT INTO task_category (name)
            SELECT %s
            WHERE NOT EXISTS (SELECT 1 FROM task_category WHERE name = %s)
        ''', (name, name))


def get_dict_tables(cur):
    cur.execute("""
    SELECT * FROM task_status
    """)
    status_dict = dict(cur.fetchall())

    cur.execute("""
    SELECT * FROM task_priority
    """)
    priority_dict = dict(cur.fetchall())

    cur.execute("""
    SELECT * FROM task_category
    """)
    category_dict = dict(cur.fetchall())

    return status_dict, priority_dict, category_dict


if __name__ == '__main__':
    task_1 = Task('walk')
    print(task_1)
    if task_1:
        print('here')

    cur = conn.cursor()

    crete_tables(cur)
    task_status_dict, task_priority_dict, task_category_dict = get_dict_tables(cur)
    print(task_status_dict, task_priority_dict, task_category_dict)

    conn.commit()

    conn.close()