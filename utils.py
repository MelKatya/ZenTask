import copy
from datetime import datetime, time
from typing import Optional, Union, Tuple, List
from PySide6.QtWidgets import QComboBox
from database import (get_dict_tables, save_category, Task, TotalTimer, Note, TaskRepeat)
import psycopg2.errors


task_status_dict, task_priority_dict, task_category_dict = get_dict_tables()


def load_stylesheet(path: str = "forms/style.css") -> str:
    """
    Загружает и возвращает CSS-стили из файла.
    """
    with open(path, "r") as f:
        return f.read()


def upload_category(combobox: QComboBox) -> None:
    """
    Загружает все категории из базы данных в переданный QComboBox.
    """
    combobox.clear()
    for category in task_category_dict.values():
        combobox.addItem(category)


def upload_priority(combobox: QComboBox) -> None:
    """
    Загружает все приоритеты из базы данных в переданный QComboBox.
    """
    combobox.clear()
    for priority in task_priority_dict.values():
        combobox.addItem(priority)


def save_new_category(name: str) -> None:
    """
    Сохраняет новую категорию в базу данных.
    """

    save_category(name=name)
    global task_category_dict
    _, _, task_category_dict = get_dict_tables()


def save_task(name: str, priority: int, category: int,
              description: str, deadline: Optional = None) -> Union[int, psycopg2.errors.UniqueViolation]:
    """
    Сохраняет новую задачу в базу данных.
    """

    new_task = Task(name=name, description=description,
                    priority_id=priority, category_id=category, deadline=deadline)

    result_save = new_task.save_task()

    return new_task.id if not result_save else result_save


def save_timer(planned_time: str) -> TotalTimer:
    """
    Сохраняет запланированное время работы.
    """
    new_timer = TotalTimer(planned_time)
    new_timer.save_time()
    return new_timer


def stop_timer(timer: TotalTimer, completed_time: datetime) -> None:
    """
    Останавливает таймер, передает в базу данных отработанное время.
    """
    timer.stop_timer(completed_time=completed_time)


def show_history_time() -> Tuple[datetime, List[List[str]]]:
    """
    Загружает из базы данных историю и полное время работы с таймером.

    Returns:
        total_time (datetime): Общее отработанное время.
        all_timers (List[List[str]]): Список таймеров в виде [дата, начало, конец, общее время] (в формате строк)
    """
    all_timers = []
    data_from_db, total_time = TotalTimer.download_history()
    for timer in data_from_db:
        timer_data = []
        timer_data.append(timer[1].strftime("%Y-%m-%d"))
        timer_data.extend([t.strftime("%H:%M:%S") for t in timer[2:]])
        all_timers.append(timer_data)
    return total_time, all_timers


def save_note_to_db(text: str) -> Note:
    """
    Сохраняет заметки в базу данных.
    """
    new_note = Note(text=text)
    new_note.save_note()
    return new_note


def download_all_tasks_from_db() -> Tuple[List[Task], List[Task], List[Task]]:
    """
    Выгружает все задачи из БД и сортирует их по статусам:
        - 1: Запланировано
        - 2: Выполняется
        - 3: Выполнено
    Returns:
        Tuple[List[Task], List[Task], List[Task]]: Списки задач по статусу.
    """
    planned_tasks = []
    doing_tasks = []
    done_task = []
    for task in Task.download_all_tasks():
        if task.status == 1:
            planned_tasks.append(task)
        elif task.status == 2:
            doing_tasks.append(task)
        else:
            done_task.append(task)
    return planned_tasks, doing_tasks, done_task


def add_new_repeat(task_id: int, repeat: str) -> Optional[TaskRepeat]:
    """
    Добавляет новое повторение для задачи.
    """
    repeat_type, repeat_value = repeat.split(' / ')
    repeat = TaskRepeat(task_id, repeat_type, repeat_value)
    TaskRepeat.del_repeat(task_id=task_id)
    task_repeat_id = repeat.save_repeat(task_id=task_id)

    if task_repeat_id:
        return repeat


def return_task() -> None:
    """
    Проверяет повторяющиеся задачи и создает новые, если наступил момент для повторения.

    - "Месяц / ДД" — создает задачу, если текущий день месяца совпадает.
    - "Неделя / Пн-Вс" — создает задачу, если сегодня нужный день недели.
    - "День / HH:MM" — создает задачу, если текущее время позже указанного.

    Если подходящее условие выполнено, задача клонируется, получает статус запанированно, и сохраняется как новая.
    """
    all_task = Task.download_all_tasks()
    week = dict(zip(("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"), range(7)))
    for task in all_task:
        if task.repeats:
            for rep in task.repeats:
                if datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) > datetime.strptime(rep[0],
                                                                                                         '%Y-%m-%d'):
                    new_task = copy.copy(task)
                    flag_create = False

                    if rep[1] == 'Месяц' and datetime.now().strftime("%m") == rep[2]:
                        flag_create = True
                    elif rep[1] == 'Неделя' and datetime.now().weekday() == week[rep[2]]:
                        flag_create = True
                    elif rep[1] == 'День' and datetime.now() > datetime.now().replace(hour=int(rep[2].split(':')[0]),
                                                                                      minute=0):
                        flag_create = True

                    if flag_create:
                        new_task.name = new_task.name + f' {datetime.now().strftime("%Y-%m-%d")}'
                        new_task.status = 1
                        new_task.save_task()
                        break
