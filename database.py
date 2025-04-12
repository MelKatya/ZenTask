import copy
import logging
from functools import wraps
from datetime import datetime
from psycopg2 import pool
import psycopg2
from psycopg2 import errors
import os
import time
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG,
                    filename='log.log',
                    format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
logger = logging.getLogger('database')


db_pool = pool.SimpleConnectionPool(1, 10, database=os.getenv("database"), user=os.getenv("user"),
                                    password=os.getenv("password"))


def work_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = db_pool.getconn()
        cur = conn.cursor()
        try:
            result = func(cur=cur, *args, **kwargs)
            conn.commit()
            return result
        except errors.UniqueViolation as exc:
            logger.error(f'Возникла ошибка в функции {func.__name__}', exc_info=exc)
            return exc
        except Exception as exc:
            logger.error(f'Возникла ошибка в функции {func.__name__}', exc_info=exc)
        finally:
            cur.close()
            db_pool.putconn(conn)
    return wrapper


class Task:
    def __init__(self, name, description="", priority_id=1, category_id=1, deadline=None, repeat=None):
        self.id = None
        self.name = name
        self.priority = priority_id
        self.category = category_id
        self.description = description
        self.status = 1
        self.deadline = datetime.strftime(deadline, "%Y-%m-%d %H:%M:%S") if deadline else None
        # self.deadline = deadline
        self.repeat = repeat
        self.timer = None

    def __str__(self):
        return (f"Task: name - {self.name} (priority - {task_priority_dict[self.priority]}, "
                f"status - {task_status_dict[self.status]}, " 
                f"category - {task_category_dict[self.category]}, "
                f"deadline - {self.deadline}, "
                f"repeat - {self.repeat}) -- decription - {self.description}")

    def start_timer(self):
        self.timer = time.time()

    def stop_timer(self):
        self.timer = round(time.time() - self.timer, 2)

    @work_db
    def save_task(self, cur):
        logger.info(f'Создание задачи: "{self}"')
        cur.execute("""
        INSERT INTO task 
        (name, priority_id, category_id, description, status_id, deadline, repeat, timer)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """, (self.name, self.priority, self.category, self.description,
              self.status, self.deadline, self.repeat, self.timer))
        self.id = cur.fetchone()[0]

    @work_db
    def change_task(self, cur):
        logger.info(f'Изменение задачи: {self.id}')
        cur.execute("""
        UPDATE task SET
        name = %s, priority_id = %s, category_id = %s, description = %s, 
        status_id = %s, deadline = %s, repeat = %s, timer = %s
        WHERE id = %s
        """, (self.name, self.priority, self.category, self.description,
              self.status, self.deadline, self.repeat, self.timer, self.id))

    @work_db
    def delete_task(self, cur):
        logger.info(f'Удаление задачи: {self.id}')
        cur.execute("""
                DELETE FROM task
                WHERE id = %s
                """, (self.id,))


class Note:
    def __init__(self, text):
        self.id = None
        self.text = text
        self.attach = False
        self.page = None

    @work_db
    def save_note(self, cur):
        cur.execute("""
            INSERT INTO notes 
            (text, attach, page)
            VALUES (%s, %s, %s)
            RETURNING id
            """, (self.text, self.attach, self.page))
        self.id = cur.fetchone()[0]

    @work_db
    def delete_note(self, cur):
        cur.execute("""
            DELETE FROM notes
            WHERE id = %s
            """, (self.id,))

    @work_db
    def attach_note(self, cur):
        cur.execute("""
            UPDATE notes SET attach = True
            WHERE id = %s;
            UPDATE notes SET attach = False
            WHERE id != %s;
            """, (self.id,))


class TotalTimer:
    def __init__(self, planned_time):
        self.id = None
        self.date = datetime.now()
        self.planned_time = planned_time
        self.completed_time = None

    @work_db
    def save_time(self, cur):
        logger.info(f'Сохранение таймера работы: {self}')
        cur.execute("""
            INSERT INTO timer 
            (date, planned_time, completed_time)
            VALUES (%s, %s, %s)
            RETURNING id
            """, (self.date, self.planned_time, self.completed_time))
        self.id = cur.fetchone()[0]


@work_db
def create_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS task_status (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL);
    """)

    for name in ('Запланировано', 'Делаю', 'Сделано'):
        cur.execute('''
            INSERT INTO task_status (name)
            SELECT %s
            WHERE NOT EXISTS (SELECT 1 FROM task_status WHERE name = %s);
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
            WHERE NOT EXISTS (SELECT 1 FROM task_priority WHERE name = %s);
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
            WHERE NOT EXISTS (SELECT 1 FROM task_category WHERE name = %s);
        ''', (name, name))

    cur.execute("""
       CREATE TABLE IF NOT EXISTS task (
       id SERIAL PRIMARY KEY,
       name VARCHAR UNIQUE NOT NULL,
       priority_id INTEGER REFERENCES task_priority(id),
       category_id INTEGER REFERENCES task_category(id),
       description TEXT,
       status_id INTEGER REFERENCES task_status(id),
       deadline TIMESTAMP,
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
       CREATE TABLE IF NOT EXISTS timer (
       id SERIAL PRIMARY KEY,
       date DATE,
       planned_time TIME,
       completed_time TIME);
       """)


@work_db
def save_category(cur, name):
    logger.info(f'Добавление новой категории {name}')
    cur.execute('''
        INSERT INTO task_category (name)
        SELECT %s
        WHERE NOT EXISTS (SELECT * FROM task_category WHERE name = %s)
    ''', (name, name))



@work_db
def get_dict_tables(cur):
    logger.info('Выборка всех значений из task_status и сохранение в status_dict')
    cur.execute("""
    SELECT * FROM task_status
    """)
    status_dict = dict(cur.fetchall())

    logger.info('Выборка всех значений из task_priority и сохранение в priority_dict')
    cur.execute("""
    SELECT * FROM task_priority
    """)
    priority_dict = dict(cur.fetchall())

    logger.info('Выборка всех значений из task_category и сохранение в category_dict')
    cur.execute("""
    SELECT * FROM task_category
    """)
    category_dict = dict(cur.fetchall())

    return status_dict, priority_dict, category_dict



if __name__ == '__main__':
    # conn = db_pool.getconn()
    # cur = conn.cursor()
    #
    create_tables()
    task_status_dict, task_priority_dict, task_category_dict = get_dict_tables()
    # print(task_status_dict)
    # conn.commit()
    # cur.close()
    # db_pool.putconn(conn)
    # tme = datetime.now()
    # # datetime.strptime(tme, "%Y-%m-%d %H:%M:%S")
    # print(datetime.strftime(tme, "%Y-%m-%d %H:%M:%S"))
    task_1 = Task('check time', 'walk in the park', deadline=datetime.now())
    task_1.save_task()
    #
    # note_1 = Note('jjdjdjdj')
    # note_1.save_note(cur)
    # save_category('work')
