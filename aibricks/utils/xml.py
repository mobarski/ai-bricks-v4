import xml.etree.ElementTree as ET
import re


def top_level_tags(xml_string):
    """
    Extract top-level tags from XML string.
    """
    matches = re.findall(r'(<(\w+)\W.*?</\2>)', xml_string, re.DOTALL)
    return [match[0] for match in matches]


def parse_xml(xml_string):
    """
    Parse XML string into a list of tuples (tag, attributes, keyword arguments).
    """
    out = []
    for xml in top_level_tags(xml_string):
        et = ET.fromstring(xml)
        kw = {}
        for child in et:
            kw[child.tag] = child.text
        out.append((et.tag, et.attrib, kw))
    return out
