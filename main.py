import os
import json
from datetime import datetime
from src.xml_parser import parse_xml
from src.config_generator import generate_config_xml
from src.meta_generator import generate_meta_json
from src.json_diff import compare_configs, apply_delta


def get_next_output_folder(base_path="output"):
    os.makedirs(base_path, exist_ok=True)

    # Ищем существующие папки с номерами
    existing_runs = [
        int(folder) for folder in os.listdir(base_path)
        if folder.isdigit()
    ]

    # Определяем номер для новой папки
    next_run = max(existing_runs) + 1 if existing_runs else 1

    # Создаем путь к новой папке
    run_folder = os.path.join(base_path, str(next_run))
    os.makedirs(run_folder, exist_ok=True)

    return run_folder


def main():
    try:
        # Создаем папку для этого запуска
        run_folder = get_next_output_folder()
        print(f"Запуск #{os.path.basename(run_folder)}")

        # 1. Генерация файлов из XML
        classes, aggregations = parse_xml("input/impulse_test_input.xml")
        generate_config_xml(classes, aggregations, os.path.join(run_folder, "config.xml"))
        generate_meta_json(classes, aggregations, os.path.join(run_folder, "meta.json"))

        # 2. Сравнение конфигов
        delta = compare_configs(
            "input/config.json",
            "input/patched_config.json"
        )

        delta_path = os.path.join(run_folder, "delta.json")
        with open(delta_path, 'w') as f:
            json.dump(delta, f, indent=4)

        # 3. Применение дельты
        apply_delta(
            "input/config.json",
            delta_path,
            os.path.join(run_folder, "res_patched_config.json")
        )

        # Добавляем мета-информацию о запуске
        with open(os.path.join(run_folder, "run_info.txt"), 'w') as f:
            f.write(f"Запуск #{os.path.basename(run_folder)}\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Статус: Успешно\n")

        print(f"Результаты сохранены в {run_folder}/")

    except Exception as e:
        if 'run_folder' in locals():
            with open(os.path.join(run_folder, "run_info.txt"), 'w') as f:
                f.write(f"Запуск #{os.path.basename(run_folder)}\n")
                f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Ошибка: {str(e)}\n")
        print(f"Ошибка: {str(e)}")


if __name__ == "__main__":
    main()