from typing import Dict, List
import json


def generate_meta_json(classes: Dict, aggregations: List, output_path: str):
    # 1. Создаем связи между классами
    child_classes = {}
    multiplicity_info = {}

    for agg in aggregations:
        target = agg['target']
        source = agg['source']

        if target not in child_classes:
            child_classes[target] = []
        child_classes[target].append(source)

        multiplicity_info[source] = {
            'min': agg['sourceMultiplicity'].split('..')[0],
            'max': agg['sourceMultiplicity'].split('..')[-1]
        }

    # 2. Формируем данные для каждого класса
    meta_data = []
    for class_name, class_info in classes.items():
        entry = {
            'class': class_name,
            'documentation': class_info['documentation'],
            'isRoot': class_info['isRoot'],
            'parameters': []
        }

        # Добавляем обычные атрибуты
        for attr in class_info['attributes']:
            entry['parameters'].append({
                'name': attr['name'],
                'type': attr['type']
            })

        # Добавляем вложенные классы (если есть)
        if class_name in child_classes:
            for child in child_classes[class_name]:
                entry['parameters'].append({
                    'name': child,
                    'type': 'class'
                })

        # Добавляем кратности (для не-root классов)
        if not class_info['isRoot'] and class_name in multiplicity_info:
            entry.update({
                'min': multiplicity_info[class_name]['min'],
                'max': multiplicity_info[class_name]['max']
            })

        meta_data.append(entry)

    # 3. Сортируем классы как в примере (не-root сначала)
    meta_data.sort(key=lambda x: (x['isRoot'], x['class']))

    # 4. Сохраняем в файл
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(meta_data, f, indent=4, ensure_ascii=False)