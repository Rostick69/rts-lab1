"""Расчёты временных характеристик и классификация системы реального времени."""

from models import HARD


def slack(task):
    """Запас времени L = D - C."""
    return task.D - task.C


def is_feasible(task):
    """Дедлайн выполним, если запас не отрицательный (L >= 0)."""
    return slack(task) >= 0