import logging
from typing import List, Tuple, Dict, Callable, Any, Optional
from functools import wraps
from datetime import datetime
from psycopg2 import pool, errors
from psycopg2.extensions import cursor
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG,
                    filename='log.log',
                    format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

logger = logging.getLogger(__name__)


db_pool = pool.SimpleConnectionPool(1, 10, database=os.getenv("database"), user=os.getenv("user"),
                                    password=os.getenv("password"))


def work_db(func: Callable) -> Callable:
    """
    Декоратор, который автоматически управляет подключением к базе данных:
    получает соединение и курсор, коммитит изменения, закрывает соединение.

    Обрабатывает ошибки и логирует исключения.
    """
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
    """
    Представляет задачу, хранящуюся в БД.

    Args:
        name (str): Название задачи.
        description (str): Описание задачи.
        priority_id (int): Приоритет задачи.
        category_id (int): Категория задачи.
        deadline Any: Дата и время дедлайна.
        id_task (Optional[int]): ID задачи в базе.
        status_id (int): Статус выполнения.
        overdue (bool): Просрочена ли задача.
        timer (datetime, time): Время, затраченное на выполнение.
        repeats (Optional[tuple["TaskRepeat"]]): Повторения задачи.
    """
    def __init__(self, name: str, description: str = "", priority_id: int = 1, category_id: int = 1,
                 deadline: Any = None, id_task: Optional[int] = None, status_id: int = 1,
                 overdue: bool = False,
                 timer=datetime.now().replace(hour=0, minute=0, second=0),
                 repeats: Optional[tuple["TaskRepeat"]] = None):

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

    def __repr__(self) -> str:
        return (f"Task: name - {self.name} (priority - {task_priority_dict[self.priority]}, "
                f"status - {task_status_dict[self.status]}, " 
                f"category - {task_category_dict[self.category]}, "
                f"deadline - {self.deadline}, overdue - {self.overdue}, "
                f"repeat - {self.repeats}) -- description - {self.description}")

    @work_db
    def stop_timer(self, cur: cursor) -> None:
        """
        Останавливает таймер задачи и сохраняет в базу.
        """
        logger.info(f'Остановка таймера: "{self}"')

        self.timer = self.timer.replace(microsecond=0).time()
        cur.execute("""
        UPDATE task 
        SET timer = %s
        WHERE id = %s
        """, (self.timer, self.id))

    @work_db
    def remove_timer(self, cur: cursor) -> None:
        """
        Очищает таймер задачи.
        """
        logger.info(f'Очистка таймера: "{self}"')

        self.timer = datetime.now().replace(hour=0, minute=0, second=0)
        cur.execute("""
            UPDATE task 
            SET timer = %s
            WHERE id = %s
            """, (self.timer, self.id))

    @work_db
    def save_task(self, cur: cursor) -> None:
        """
        Сохраняет новую задачу в базу данных.
        """
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
    def change_task(self, cur: cursor) -> bool:
        """
        Обновляет существующую задачу в базе данных.
        """
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
    def change_status(self, cur: cursor, status_id: int) -> None:
        """
        Меняет статус выполнения задачи.
        """
        logger.info(f'Изменение статуса задачи: {self.id}')

        cur.execute("""
        UPDATE task SET
        status_id = %s, overdue = %s
        WHERE id = %s
        """, (status_id, self.overdue, self.id))

    @work_db
    def delete_task(self, cur: cursor) -> None:
        """
        Удаляет задачу из базы данных.
        """
        logger.info(f'Удаление задачи: {self.id}')

        cur.execute("""
                DELETE FROM task
                WHERE id = %s
                """, (self.id,))

    @classmethod
    @work_db
    def download_tasks_by_status(cls, cur: cursor, status_id: int) -> List["Task"]:
        """
        Выгружает все задачи из бд со статусом status_id и создает объекты задач

        Args:
            cur (cursor): Курсор БД.
            status_id (int): Статус выполнения.
        """

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
    def download_all_tasks(cls, cur: cursor) -> List["Task"]:
        """
        Выгружает все задачи из базы данных и создает объекты задач.
        """
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
    def check_overdue(cls, cur: cursor) -> None:
        """
        Проверяет, просрочена ли задача, и обновляет флаг 'overdue'.
        """
        logger.info(f'Проверка просроченных задач')

        cur.execute("""
            UPDATE task
            SET overdue = true
            WHERE status_id in (1, 2) AND deadline is not null AND deadline < %s
                    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ))

    def add_repeat(self, repeat: "TaskRepeat") -> None:
        """
        Добавляет повторение задачи в список.

        Args:
            repeat ("TaskRepeat"): экземпляр повторения задачи.
        """
        logger.info(f'добавлено повторение {repeat} в задачу {self.id}')

        if self.repeats is None:
            self.repeats = []
        self.repeats.append(repeat)


class TaskRepeat:
    """
    Класс, представляющий повторение задачи

    Args:
        task_id (int): ID задачи.
        repeat_type (str): Тип повтора (День, Неделя, Месяц).
        repeat_value (str): Значение повтора (например, 'Пн' для Неделя).
        id_repeat (Optional[int]): ID повтора.
    """
    def __init__(self, task_id: int, repeat_type: str, repeat_value: str, id_repeat: Optional[int] = None) -> None:
        self.id = id_repeat
        self.task_id = task_id
        self.start_date = datetime.now()
        self.repeat_type = repeat_type
        self.repeat_value = repeat_value

    @classmethod
    @work_db
    def del_repeat(cls, cur: cursor, task_id: int) -> None:
        """
         Удаляет повторение задачи из базы данных по ID задачи.

        Args:
            cur (cursor): Курсор БД.
            task_id (int): ID задачи.
        """
        logger.info(f'Повторение у задачи {task_id} удалено из бд')

        cur.execute("""
                DELETE FROM task_repeat 
                WHERE task_id = %s
                """, (task_id, ))

    @work_db
    def save_repeat(self, cur: cursor, task_id: int) -> int:
        """
        Сохраняет повторение задачи в базу данных.

        Args:
            cur (cursor): Курсор БД.
            task_id (int): ID задачи.
        """
        logger.info(f'Повторение у задачи {task_id} добавлено в бд')

        self.task_id = task_id
        cur.execute("""
                INSERT INTO task_repeat 
                (task_id, start_date, repeat_type, repeat_value)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """, (self.task_id, self.start_date, self.repeat_type, self.repeat_value))
        self.id = cur.fetchone()[0]
        return self.id


class Note:
    """
    Класс заметки.

    Args:
        text (str): Текст заметки.
        id_note (Optional[int]): ID заметки в базе данных.
    """
    def __init__(self, text: str, id_note: Optional[int] = None):
        self.id = id_note
        self.text = text
        self.attach = False

    def __repr__(self) -> str:
        return f"Note: text - {self.text}, id - {self.id}, attach={self.attach}"

    @work_db
    def save_note(self, cur: cursor) -> None:
        """
        Сохраняет заметку в базу данных и присваивает ей ID.
        """
        logger.info(f'Сохранение заметки: "{self}"')

        cur.execute("""
            INSERT INTO notes 
            (text, attach)
            VALUES (%s, %s)
            RETURNING id
            """, (self.text, self.attach))
        self.id = cur.fetchone()[0]

    @work_db
    def delete_note(self, cur: cursor) -> None:
        """
        Удаляет заметку из базы данных.
        """
        logger.info(f'Удаление заметки: "{self}"')

        cur.execute("""
            DELETE FROM notes
            WHERE id = %s
            """, (self.id,))

    @work_db
    def attach_note(self, cur: cursor) -> None:
        """
        Закрепляет заметку, открепляя все остальные.
        """
        logger.info(f'Прикрепление заметки: "{self}"')

        cur.execute("""
            UPDATE notes SET attach = True
            WHERE id = %s;
            UPDATE notes SET attach = False
            WHERE id != %s;
            """, (self.id, self.id))

    @work_db
    def edit_note(self, cur: cursor, text: str) -> None:
        """
        Изменяет текст заметки.

        Args:
            cur (cursor): Курсор БД.
            text (str): Измененный текст заметки.
        """
        logger.info(f'Изменение заметки: "{self}"')

        self.text = text
        cur.execute("""
            UPDATE notes 
            SET text = %s
            WHERE id = %s;
            """, (self.text, self.id))

    @classmethod
    @work_db
    def download_notes(cls, cur: cursor) -> List[Tuple]:
        # todo
        """
        Загружает все заметки из базы данных и возвращает список объектов Note.
        """
        logger.info('Заметки выгружаются')

        cur.execute("""
        SELECT * FROM notes
        """)
        return cur.fetchall()


class TotalTimer:
    """
    Класс таймера для отслеживания общего времени работы.

    Args:
        planned_time (str): Запланированное время (например, "08:00").
    """
    def __init__(self, planned_time: str):
        self.id = None
        self.date = datetime.now()
        self.planned_time = planned_time
        self.completed_time = None

    def __repr__(self) -> str:
        return (f"TotalTimer: id - {self.id}, "
                f"date - {self.date}, "
                f"planned_time - {self.planned_time}, " 
                f"completed_time - {self.completed_time}")

    @work_db
    def save_time(self, cur: cursor) -> None:
        """
        Сохраняет таймер работы в базу данных.
        """
        logger.info(f'Сохранение таймера работы: {self}')

        cur.execute("""
            INSERT INTO timer 
            (date, planned_time, completed_time)
            VALUES (%s, %s, %s)
            RETURNING id
            """, (self.date, self.planned_time, self.completed_time))
        self.id = cur.fetchone()[0]

    @work_db
    def stop_timer(self, cur: cursor, completed_time: datetime) -> None:
        """
        Сохраняет время завершения таймера.

        Args:
            cur (cursor): Курсор БД.
            completed_time (datetime): Отработанное время.
        """
        logger.info(f'Остановка работы таймера: {self}')

        self.completed_time = completed_time.replace(microsecond=0).time()
        cur.execute("""
        UPDATE timer
        SET completed_time = %s
        WHERE id = %s
        """, (self.completed_time, self.id))

    @classmethod
    @work_db
    def download_history(cls, cur) -> Tuple[List, datetime]:
        """
        Выгружает из базы данных всю историю таймеров.
        """
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

