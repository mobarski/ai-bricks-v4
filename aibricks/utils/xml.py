import xml.etree.ElementTree as ET


def dict_from_xml(xml_string):
    try:
        root = ET.fromstring(xml_string)
        return {child.tag.lower(): child.text for child in root}
    except Exception as e:
        print(xml_string)
        raise e


def list_from_xml(xml_string):
    try:
        root = ET.fromstring(xml_string)
        return [dict_from_xml(ET.tostring(child)) for child in root]
    except Exception as e:
        print(xml_string)
        raise e
