"""Расчёты временных характеристик и классификация системы реального времени."""

from models import HARD


def slack(task):
    """Запас времени L = D - C."""
    return task.D - task.C


def is_feasible(task):
    """Дедлайн выполним, если запас не отрицательный (L >= 0)."""
    return slack(task) >= 0



def deadline_type(task):
    """Тип дедлайна по соотношению D и T."""
    # Сначала проверяем равенство: случай D = T подходит и под D <= T,
    # поэтому если проверить его вторым, неявный дедлайн никогда не определится
    if task.D == task.T:
        return "неявный"
    if task.D < task.T:
        return "ограниченный"
    return "произвольный"




def hard_tasks(tasks):
    """Вспомогательная функция: только жёсткие задачи."""
    return [t for t in tasks if t.hardness == HARD]


def classify_system(tasks):
    """Система жёсткого РВ, если есть хотя бы одна жёсткая задача, иначе мягкого."""
    if hard_tasks(tasks):
        return "жёсткого реального времени"
    return "мягкого реального времени"


def critical_task(tasks):
    """Критическая задача — жёсткая задача с наименьшим запасом. None, если жёстких нет."""
    hard = hard_tasks(tasks)
    if not hard:
        return None
    return min(hard, key=slack)


def required_reaction_time(tasks):
    """R_треб = min(D) по жёстким задачам, а если их нет — по всем задачам."""
    hard = hard_tasks(tasks)
    source = hard if hard else tasks
    return min(t.D for t in source)




def utilization(tasks):
    """Коэффициент загрузки процессора U = сумма(C / T)."""
    return sum(t.C / t.T for t in tasks)


def classify_architecture(n_cpu, has_network):
    """Архитектурный класс системы по числу процессоров и наличию сети."""
    # Сеть проверяем первой: узлы, связанные сетью, — это уже распределённая система,
    # сколько бы процессоров ни было в каждом узле
    if has_network:
        return "распределённая"
    if n_cpu > 1:
        return "многопроцессорная"
    return "однопроцессорная"