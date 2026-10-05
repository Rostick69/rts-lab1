"""Вывод таблицы результатов и заключения в консоль."""

from calculations import (slack, is_feasible, deadline_type, classify_system,
                          critical_task, required_reaction_time, utilization,
                          classify_architecture)


def fmt(x):
    """Число без лишнего «.0»: 5.0 -> 5, 0.25 -> 0.25."""
    return f"{x:g}"


def print_table(tasks):
    """Печатает таблицу: Задача | Класс | C | D | T | L | Выполнимо | Тип дедлайна."""
    # Ширина первой колонки подстраивается под самое длинное имя задачи
    name_w = max(len("Задача"), max(len(t.name) for t in tasks))

    header = (f"{'Задача':<{name_w}} | {'Класс':<8} | {'C':>4} | {'D':>4} | {'T':>5} | "
              f"{'L':>4} | {'Выполнимо':<9} | Тип дедлайна")
    print(header)
    print("-" * len(header))

    for t in tasks:
        feasible = "да" if is_feasible(t) else "НЕТ"
        print(f"{t.name:<{name_w}} | {t.hardness:<8} | {fmt(t.C):>4} | {fmt(t.D):>4} | "
              f"{fmt(t.T):>5} | {fmt(slack(t)):>4} | {feasible:<9} | {deadline_type(t)}")