from xml.etree import ElementTree
import settings

root = ElementTree.parse(settings.FACT_FILE).getroot()


def get_fact_list(tag):
    """
    Creates a list of elements based on a specific tag in the associated XML file.
    :param tag: Tag whose contents are to be returned
    :return: List of elements within the chosen tag.
    """
    facts = []
    for child in root.iter(tag):
        for e in child.findall("fct"):
            facts.append(e.text)
    return facts


def get_listdict():
    """
    Returns all 'top-level' tags and associated regular-expressions.
    :return: Dictionary containing regular expressions as a key, and associated tag as the values
    """
    result = {}
    for child in root:
        result[child.attrib["regex"]] = child.tag
    return result
