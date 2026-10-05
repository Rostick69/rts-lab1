"""Практическая работа 1 (СРВ). Вариант 2: бортовая система автомобиля.

Запуск: python src/main.py [путь_к_файлу.json]
Без аргумента берётся data/variant2.json.
"""

import sys
from pathlib import Path

from models import load_variant
from output import print_table, print_conclusion

# Путь строим от расположения этого файла, а не от текущей папки,
# поэтому программа находит данные при запуске и из Visual Studio, и из консоли
DEFAULT_DATA = Path(__file__).parent.parent / "data" / "variant2.json"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA
    tasks, n_cpu, has_network = load_variant(path)

    print("Анализ системы реального времени: бортовая система автомобиля\n")
    print_table(tasks)
    print_conclusion(tasks, n_cpu, has_network)


if __name__ == "__main__":
    main()