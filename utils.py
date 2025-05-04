from database import (get_dict_tables, save_category, Task, TotalTimer, Note, TaskRepeat)


task_status_dict, task_priority_dict, task_category_dict = get_dict_tables()


def upload_category(combobox):
    """Загружает все категории из бд в combobox"""
    combobox.clear()
    for category in task_category_dict.values():
        combobox.addItem(category)


def upload_priority(combobox):
    """Загружает все приоритеты из бд в combobox"""
    combobox.clear()
    for priority in task_priority_dict.values():
        combobox.addItem(priority)


def save_new_category(name):
    """Сохраняет новую категорию в бд"""
    save_category(name=name)
    global task_category_dict
    _, _, task_category_dict = get_dict_tables()


def save_task(name, priority, category, descrirtion, deadline=None):
    """Сохраняет новую задачу"""

    new_task = Task(name=name, description=descrirtion,
                    priority_id=priority, category_id=category, deadline=deadline)

    result_save = new_task.save_task()

    return new_task.id if not result_save else result_save


def save_timer(planned_time):
    """Сохраняет запланированное время работы"""
    new_timer = TotalTimer(planned_time)
    new_timer.save_time()
    return new_timer


def stop_timer(timer, completed_time):
    """Останавливает таймер, передает в бд отработанное время"""
    timer.stop_timer(completed_time=completed_time)


def show_history_time():
    """Загружает из бд историю и полное время работы с таймером"""
    all_timers = []
    data_from_db, total_time = TotalTimer.download_history()
    for timer in data_from_db:
        timer_data = []
        timer_data.append(timer[1].strftime("%Y-%m-%d"))
        timer_data.extend([t.strftime("%H:%M:%S") for t in timer[2:]])
        all_timers.append(timer_data)
    return total_time, all_timers


def save_note_to_db(text):
    """Сохраняет заметки в бд"""
    new_note = Note(text=text)
    new_note.save_note()
    return new_note


def download_noticed_from_db():
    """Выгружает все заметки из бд"""
    all_note = Note.download_notes()
    return all_note


def download_all_tasks_from_db():
    """Выгружает все задачи из бд"""
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


def add_new_repeat(task_id, replay):
    """Добавляет новое повторение"""
    repeat_type, repeat_value = replay.split(' / ')
    repeat = TaskRepeat(task_id, repeat_type, repeat_value)
    task_repeat_id = repeat.save_repeat(task_id=task_id)

    if task_repeat_id:
        return repeat






