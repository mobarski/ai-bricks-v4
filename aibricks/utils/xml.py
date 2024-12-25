import xml.etree.ElementTree as ET
import re


def extract_xml_chunks(text):
    """
    Extract top-level xml tags from a text.
    """
    matches = re.findall(r'(<(\w+)\W.*?</\2>)', text, re.DOTALL)
    return [match[0] for match in matches]


def parse_xml(text):
    """
    Parse top level xml tags within a text into a list of tuples
    (tag, attributes, keyword arguments).
    """
    out = []
    for xml in extract_xml_chunks(text):
        et = ET.fromstring(xml)
        kw = {}
        for child in et:
            kw[child.tag] = child.text
        out.append((et.tag, et.attrib, kw))
    return out
