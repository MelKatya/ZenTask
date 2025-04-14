from database import get_dict_tables, save_category, Task, TotalTimer, download_history


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


def save_task(name, priority, category, descrirtion, deadline=None, replay=None):
    """Сохраняет новую задачу"""
    global task_priority_dict, task_category_dict
    cat_id = list(filter(lambda x: x[1] == category, task_category_dict.items()))[0][0]
    prior_id = list(filter(lambda x: x[1] == priority, task_priority_dict.items()))[0][0]

    new_task = Task(name=name, description=descrirtion,
                    priority_id=prior_id, category_id=cat_id, deadline=deadline)
    return new_task.save_task()


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
    data_from_db, total_time = download_history()
    print(data_from_db, total_time)
    for timer in data_from_db:
        timer_data = []
        timer_data.append(timer[1].strftime("%Y-%m-%d"))
        timer_data.extend([t.strftime("%H:%M:%S") for t in timer[2:]])
        all_timers.append(timer_data)
    return total_time, all_timers







