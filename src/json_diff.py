import json
from typing import Dict, List, Union


def compare_configs(original_path: str, patched_path: str) -> Dict[str, List]:
    # Сравнивает две версии конфига и возвращает различия
    with open(original_path, 'r') as f:
        original = json.load(f)
    with open(patched_path, 'r') as f:
        patched = json.load(f)

    delta = {
        "additions": [],  # Новые параметры
        "deletions": [],  # Удаленные параметры
        "updates": []  # Измененные параметры
    }

    # Поиск новых параметров в patched-версии
    for key in patched:
        if key not in original:
            delta["additions"].append({
                "key": key,
                "value": patched[key]
            })

    # Поиск удаленных параметров
    for key in original:
        if key not in patched:
            delta["deletions"].append(key)

    # Поиск измененных значений
    for key in original:
        if key in patched and original[key] != patched[key]:
            delta["updates"].append({
                "key": key,
                "from": original[key],
                "to": patched[key]
            })

    return delta


def apply_delta(original_path: str, delta_path: str, output_path: str):
    # Обновляет конфиг на основе файла с изменениями
    with open(original_path, 'r') as f:
        config = json.load(f)

    with open(delta_path, 'r') as f:
        delta = json.load(f)

    # Применяем все типы изменений
    for key in delta["deletions"]:
        config.pop(key, None)
    for item in delta["updates"]:
        config[item["key"]] = item["to"]
    for item in delta["additions"]:
        config[item["key"]] = item["value"]

    with open(output_path, 'w') as f:
        json.dump(config, f, indent=4)