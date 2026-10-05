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




def print_conclusion(tasks, n_cpu, has_network):
    """Печатает текстовое заключение по системе."""
    U = utilization(tasks)
    crit = critical_task(tasks)
    all_feasible = all(is_feasible(t) for t in tasks)

    print("\nЗАКЛЮЧЕНИЕ")
    print(f"Класс системы: {classify_system(tasks)}")
    print(f"Архитектура: {classify_architecture(n_cpu, has_network)} "
          f"(процессоров: {n_cpu}, сеть: {'есть' if has_network else 'нет'})")

    if crit:
        print(f"Критическая задача: «{crit.name}» (L = {fmt(slack(crit))} мс)")
    else:
        print("Критическая задача: нет (жёстких задач нет)")

    print(f"Требуемое время реакции: R_треб = {fmt(required_reaction_time(tasks))} мс")

    # Слагаемые C/T показываем отдельно, чтобы был виден расчёт, а не только итог
    parts = " + ".join(f"{t.C / t.T:.3g}" for t in tasks)
    print(f"Коэффициент загрузки: U = {parts} = {U:.3f}", end=" ")
    print("<= 1 — условие выполнено" if U <= 1 else "> 1 — процессор перегружен")

    if all_feasible and U <= 1:
        print("Вывод: все дедлайны выполнимы, необходимое условие планируемости выполнено.")
    elif not all_feasible:
        print("Вывод: есть задачи с отрицательным запасом — их дедлайны невыполнимы.")
    else:
        print("Вывод: запас у всех задач есть, но U > 1 — набор задач не планируем.")