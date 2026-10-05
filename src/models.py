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