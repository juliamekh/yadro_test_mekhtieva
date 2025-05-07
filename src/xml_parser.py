import xml.etree.ElementTree as ET


def parse_xml(xml_path: str) -> tuple:
    # Парсит XML-модель, возвращает классы и агрегации
    tree = ET.parse(xml_path)
    root = tree.getroot()

    classes = {}
    aggregations = []

    for elem in root.findall('Class'):
        class_name = elem.get('name')
        classes[class_name] = {
            'isRoot': elem.get('isRoot') == 'true',
            'documentation': elem.get('documentation'),
            'attributes': [
                {'name': attr.get('name'), 'type': attr.get('type')}
                for attr in elem.findall('Attribute')
            ],
            'children': []
        }

    for agg in root.findall('Aggregation'):
        aggregations.append({
            'source': agg.get('source'),
            'target': agg.get('target'),
            'sourceMultiplicity': agg.get('sourceMultiplicity'),
            'targetMultiplicity': agg.get('targetMultiplicity')
        })

    return classes, aggregations