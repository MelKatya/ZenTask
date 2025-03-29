import copy
from datetime import datetime
import psycopg2
import os
import time
from dotenv import load_dotenv
load_dotenv()


conn = psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'))


class Task:
    def __init__(self, name, description="", priority_id=1, category_id=1, deadline=None, repeat=None):
        self.id = None
        self.name = name
        self.priority = priority_id
        self.category = category_id
        self.description = description
        self.status = 1
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None
        self.repeat = repeat
        self.timer = None

    def __str__(self):
        return (f"Задача: {self.name} ({task_priority_dict[self.priority]} {task_status_dict[self.status]}, " 
                f"{task_category_dict[self.category]}) - {self.description}")

    def start_timer(self):
        self.timer = time.time()

    def stop_timer(self):
        self.timer = round(time.time() - self.timer, 2)

    def save_task(self, cur):
        cur.execute("""
        INSERT INTO task 
        (name, priority_id, category_id, description, status_id, deadline, repeat, timer)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """, (self.name, self.priority, self.category, self.description,
              self.status, self.deadline, self.repeat, self.timer))
        self.id = cur.fetchone()[0]

    def change_task(self, cur):
        cur.execute("""
        UPDATE task SET
        name = %s, priority_id = %s, category_id = %s, description = %s, 
        status_id = %s, deadline = %s, repeat = %s, timer = %s
        WHERE id = %s
        """, (self.name, self.priority, self.category, self.description,
              self.status, self.deadline, self.repeat, self.timer, self.id))

    def delete_task(self, cur):
        cur.execute("""
                DELETE FROM task
                WHERE id = %s
                """, (self.id,))


class Notes:
    def __init__(self, text):
        self.id = None
        self.text = text
        self.attach = False
        self.page = None

    def save_note(self, cur):
        ...

    def delete_note(self, cur):
        cur.execute("""
                DELETE FROM task
                WHERE id = %s
                """, (self.id,))

    def attach_note(self, cur):
        ...

def crete_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS task (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    priority_id INTEGER REFERENCES task_priority(id),
    category_id INTEGER REFERENCES task_category(id),
    description TEXT,
    status_id INTEGER REFERENCES task_status(id),
    deadline DATE,
    repeat DATE,
    timer NUMERIC);
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    text TEXT,
    attach BOOL,
    page INTEGER);
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
    cur = conn.cursor()
    crete_tables(cur)
    task_status_dict, task_priority_dict, task_category_dict = get_dict_tables(cur)

    task_1 = Task('check time', 'walk in the park')




    conn.commit()

    conn.close()