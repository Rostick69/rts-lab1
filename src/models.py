"""Модель задачи реального времени и загрузка исходных данных из JSON."""

import json
from dataclasses import dataclass

# Допустимые классы жёсткости задач
HARD = "жёсткое"
FIRM = "твёрдое"
SOFT = "мягкое"
HARDNESS_CLASSES = (HARD, FIRM, SOFT)


@dataclass
class Task:
    """Задача реального времени. Все времена в миллисекундах."""
    name: str       # имя задачи
    hardness: str   # класс жёсткости: жёсткое / твёрдое / мягкое
    C: float        # время выполнения
    D: float        # относительный дедлайн
    T: float        # период



def load_variant(path):
    """Читает файл варианта и возвращает (список задач, число процессоров, наличие сети)."""
    # utf-8-sig читает файл и с BOM, и без него
    # (Visual Studio иногда сохраняет файлы с BOM, и обычный utf-8 на этом падает)
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)

    tasks = []
    for item in data["tasks"]:
        task = Task(item["name"], item["hardness"], item["C"], item["D"], item["T"])

        # Проверяем данные сразу при загрузке, чтобы расчёты не упали позже
        # (например, деление на T = 0 в коэффициенте загрузки)
        if task.hardness not in HARDNESS_CLASSES:
            raise ValueError(f"Неизвестный класс жёсткости у задачи «{task.name}»: {task.hardness}")
        if task.C <= 0 or task.D <= 0 or task.T <= 0:
            raise ValueError(f"У задачи «{task.name}» C, D и T должны быть больше нуля")

        tasks.append(task)

    n_cpu = data["system"]["n_cpu"]
    has_network = data["system"]["has_network"]
    return tasks, n_cpu, has_network