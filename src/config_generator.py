import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List

def generate_config_xml(classes: Dict, aggregations: List, output_path: str):
    # Создает XML-конфиг на основе модели классов и их связей
    # Собираем информацию о родительских и дочерних классах
    class_relations = {}
    for agg in aggregations:
        if agg['target'] not in class_relations:
            class_relations[agg['target']] = []
        class_relations[agg['target']].append(agg['source'])

    # Ищем главный класс (помеченный как isRoot="true")
    root_class = next((name for name, data in classes.items() if data['isRoot']), None)
    if not root_class:
        raise ValueError("Не найден корневой класс в модели данных")

    def build_xml_element(class_name: str) -> ET.Element:
        # Рекурсивно строит XML-элемент для класса и его потомков
        element = ET.Element(class_name)

        # Добавляем все атрибуты текущего класса
        for attr in classes[class_name]['attributes']:
            attr_element = ET.SubElement(element, attr['name'])
            attr_element.text = attr['type']

        # Добавляем вложенные классы, если они есть
        for child_class in class_relations.get(class_name, []):
            element.append(build_xml_element(child_class))

        return element

    # Строим и форматируем итоговый XML
    root_element = build_xml_element(root_class)
    pretty_xml = minidom.parseString(
        ET.tostring(root_element, encoding='utf-8')
    ).toprettyxml(indent="    ", encoding='utf-8')

    # Сохраняем в файл, убирая лишние пустые строки
    with open(output_path, 'wb') as f:
        for line in pretty_xml.splitlines():
            if line.strip():
                f.write(line + b'\n')