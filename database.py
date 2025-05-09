import copy
import logging
from typing import List, Tuple, Dict, Callable
from functools import wraps
from datetime import datetime, timedelta
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



def work_db(func: Callable) -> Callable:
    """Декоратор для того, чтобы не строчить везде подключения"""
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
    """Класс задачи"""
    def __init__(self, name: str, description: str = "", priority_id: int = 1, category_id: int = 1,
                 deadline=None, id_task=None, status_id=1, overdue=False,
                 timer=datetime.now().replace(hour=0, minute=0, second=0), repeats=None):
        self.id = id_task
        self.name = name
        self.priority = priority_id
        self.category = category_id
        self.description = description
        self.status = status_id
        self.overdue = overdue
        self.deadline = datetime.strftime(deadline, "%Y-%m-%d %H:%M:%S") if deadline else None
        self.repeats = repeats
        self.timer = timer

    def __repr__(self):
        return (f"Task: name - {self.name} (priority - {task_priority_dict[self.priority]}, "
                f"status - {task_status_dict[self.status]}, " 
                f"category - {task_category_dict[self.category]}, "
                f"deadline - {self.deadline}, overdue - {self.overdue}, "
                f"repeat - {self.repeats}) -- decription - {self.description}")


    @work_db
    def stop_timer(self, cur):
        """Останавливает таймер задачи"""
        logger.info(f'Остановка таймера: "{self}"')
        self.timer = self.timer.replace(microsecond=0).time()
        cur.execute("""
        UPDATE task 
        SET timer = %s
        WHERE id = %s
        """, (self.timer, self.id))

    @work_db
    def remove_timer(self, cur):
        """Очищает таймер задачи"""
        logger.info(f'Очистка таймера: "{self}"')
        self.timer = datetime.now().replace(hour=0, minute=0, second=0)
        cur.execute("""
            UPDATE task 
            SET timer = %s
            WHERE id = %s
            """, (self.timer, self.id))

    @work_db
    def save_task(self, cur) -> None:
        """Сохраняет задачу"""
        logger.info(f'Создание задачи: "{self}"')
        cur.execute("""
        INSERT INTO task 
        (name, priority_id, category_id, description, status_id, deadline, timer, overdue)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """, (self.name, self.priority, self.category, self.description,
              self.status, self.deadline, self.timer, self.overdue))
        self.id = cur.fetchone()[0]

    @work_db
    def change_task(self, cur) -> bool:
        """Изменяет задачу"""
        logger.info(f'Изменение задачи: {self.id}')
        cur.execute("""
        UPDATE task SET
        name = %s, priority_id = %s, category_id = %s, description = %s, 
        deadline = %s, timer = %s, overdue = %s
        WHERE id = %s
        """, (self.name, self.priority, self.category, self.description,
              self.deadline, self.timer, self.overdue, self.id))
        return True

    @work_db
    def change_status(self, cur, status_id) -> None:
        """Изменяет статус выполнения задачи"""
        logger.info(f'Изменение статуса задачи: {self.id}')
        cur.execute("""
        UPDATE task SET
        status_id = %s, overdue = %s
        WHERE id = %s
        """, (status_id, self.overdue, self.id))


    @work_db
    def delete_task(self, cur) -> None:
        """Удаляет задачу"""
        logger.info(f'Удаление задачи: {self.id}')
        cur.execute("""
                DELETE FROM task
                WHERE id = %s
                """, (self.id,))

    @classmethod
    @work_db
    def download_tasks_by_status(cls, cur, status_id):
        """Выгружает все задачи из бд со статусом status_id и создает объекты задач"""
        logger.info(f'Выгрузка всех задач со статусом {status_id}')
        cur.execute("""
            SELECT 
                t.*, 
                STRING_AGG(tr.repeat_type, ' ') AS repeat_type, 
                STRING_AGG(tr.repeat_value, ' ') AS repeat_value
            FROM task t
            LEFT JOIN task_repeat tr ON t.id = tr.task_id
            WHERE t.status_id = %s
            GROUP BY t.id
            """, (status_id,))
        res = cur.fetchall()

        tasks = [Task(id_task=task[0], name=task[1], priority_id=task[2], category_id=task[3],
                              description=task[4], status_id=task[5], deadline=task[6],
                              timer=datetime.now().replace(hour=task[7].hour, minute=task[7].minute, second=task[7].second),
                              overdue=task[8],
                              repeats=tuple(zip(task[9].split(), task[10].split())) if task[9] else None)
                         for task in res]

        return tasks

    @classmethod
    @work_db
    def download_all_tasks(cls, cur):
        """Выгружает все задачи из бд со статусом status_id и создает объекты задач"""
        logger.info(f'Выгрузка всех задач')
        cur.execute("""
            SELECT 
                t.*, 
                STRING_AGG(CAST(tr.start_date AS Text), ' ') AS start_date,
                STRING_AGG(tr.repeat_type, ' ') AS repeat_type, 
                STRING_AGG(tr.repeat_value, ' ') AS repeat_value
            FROM task t
            LEFT JOIN task_repeat tr ON t.id = tr.task_id
            GROUP BY t.id
            """,)
        res = cur.fetchall()

        tasks = [Task(id_task=task[0], name=task[1], priority_id=task[2], category_id=task[3],
                      description=task[4], status_id=task[5], deadline=task[6],
                      timer=datetime.now().replace(hour=task[7].hour, minute=task[7].minute, second=task[7].second),
                      overdue=task[8],
                      repeats=tuple(zip(task[9].split(), task[10].split(), task[11].split())) if task[9] else None)
                 for task in res]

        return tasks

    @classmethod
    @work_db
    def check_overdue(cls, cur):

        cur.execute("""
            UPDATE task
            SET overdue = true
            WHERE status_id in (1, 2) AND deadline is not null AND deadline < %s
                    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ))

    def add_repeat(self, repeat):
        self.repeats.append(repeat)


class TaskRepeat:
    def __init__(self, task_id, repeat_type, repeat_value, id_repeat=None):
        self.id = id_repeat
        self.task_id = task_id
        self.start_date = datetime.now()
        self.repeat_type = repeat_type
        self.repeat_value = repeat_value

    @classmethod
    @work_db
    def del_repeat(cls, cur, task_id):
        """Удаляет повторение"""
        cur.execute("""
                DELETE FROM task_repeat 
                WHERE task_id = %s
                """, (task_id, ))


    @work_db
    def save_repeat(self, cur, task_id):
        self.task_id = task_id
        """Сохраняет повторение"""
        cur.execute("""
                INSERT INTO task_repeat 
                (task_id, start_date, repeat_type, repeat_value)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """, (self.task_id, self.start_date, self.repeat_type, self.repeat_value))
        self.id = cur.fetchone()[0]
        return self.id


class Note:
    def __init__(self, text, id=None):
        self.id = id
        self.text = text
        self.attach = False

    def __repr__(self):
        return (f"Note: text - {self.text}, "
                f"id - {self.id}")

    @work_db
    def save_note(self, cur) -> None:
        """Сохраняет заметку в бд"""
        logger.info(f'Сохранение заметки: "{self}"')
        cur.execute("""
            INSERT INTO notes 
            (text, attach)
            VALUES (%s, %s)
            RETURNING id
            """, (self.text, self.attach))
        self.id = cur.fetchone()[0]

    @work_db
    def delete_note(self, cur) -> None:
        """Удаляет заметку из бд"""
        logger.info(f'Удаление заметки: "{self}"')
        cur.execute("""
            DELETE FROM notes
            WHERE id = %s
            """, (self.id,))

    @work_db
    def attach_note(self, cur) -> None:
        """Сохраняет в бд информацию о прикрепленной заметке"""
        logger.info(f'Прикрепление заметки: "{self}"')
        cur.execute("""
            UPDATE notes SET attach = True
            WHERE id = %s;
            UPDATE notes SET attach = False
            WHERE id != %s;
            """, (self.id, self.id))

    @work_db
    def change_note(self, cur, text) -> None:
        """Изменяет заметку"""
        self.text = text
        cur.execute("""
            UPDATE notes 
            SET text = %s
            WHERE id = %s;
            """, (self.text, self.id))

    @classmethod
    @work_db
    def download_notes(cls, cur) -> List[Tuple]:
        """Выгружает все заметки из бд"""
        cur.execute("""
        SELECT * FROM notes
        """)
        return cur.fetchall()


class TotalTimer:
    def __init__(self, planned_time):
        self.id = None
        self.date = datetime.now()
        self.planned_time = planned_time
        self.completed_time = None

    # def __getitem__(self, item: str) -> Any:
    #     return getattr(self, item)
    def __repr__(self):
        return (f"TotalTimer: id - {self.id}, "
                f"date - {self.date}, "
                f"planned_time - {self.planned_time}, " 
                f"completed_time - {self.completed_time}")

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
    def stop_timer(self, cur, completed_time: datetime) -> None:
        self.completed_time = completed_time.replace(microsecond=0).time()
        logger.info(f'Остановка работы таймера: {self}')
        cur.execute("""
        UPDATE timer
        SET completed_time = %s
        WHERE id = %s
        """, (self.completed_time, self.id))

    @classmethod
    @work_db
    def download_history(cls, cur) -> Tuple[List, datetime]:
        logger.info(f'Выгрузка истории таймера')
        cur.execute("""
        SELECT * FROM timer 
        WHERE completed_time IS NOT NULL
        """)
        all_timers = cur.fetchall()
        cur.execute("SELECT sum(completed_time) FROM public.timer")
        sum_time_work = cur.fetchall()[0][0]
        return all_timers, sum_time_work


@work_db
def create_tables(cur) -> None:
    logger.info(f'Создание таблиц')
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
       timer TIME,
       overdue BOOL);
       """)

    cur.execute("""
       CREATE TABLE IF NOT EXISTS task_repeat (
       id SERIAL PRIMARY KEY,
       task_id INTEGER REFERENCES task(id) ON DELETE CASCADE,
       start_date DATE,
       repeat_type TEXT,
       repeat_value TEXT);
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
def save_category(cur, name: str) -> None:
    """Сохраняет новую категорию в бд"""
    logger.info(f'Добавление новой категории {name}')
    cur.execute('''
        INSERT INTO task_category (name)
        SELECT %s
        WHERE NOT EXISTS (SELECT * FROM task_category WHERE name = %s)
    ''', (name, name))


@work_db
def get_dict_tables(cur):
    """
    Выгружает данные из таблиц: статус, приоритет и категория, и возвращает
    их в виде кортежа словарей
    """
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


task_status_dict, task_priority_dict, task_category_dict = get_dict_tables()


if __name__ == '__main__':
    create_tables()
    task_status_dict, task_priority_dict, task_category_dict = get_dict_tables()
    all_tasks = Task.download_all_tasks()
    for i in all_tasks:
        print(i.id, i)

