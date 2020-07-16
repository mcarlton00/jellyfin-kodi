import xml.etree.ElementTree as ET
import yaml
import sys

def indent(elem, level=0):
    '''
    Nicely formats output xml with newlines and spaces
    https://stackoverflow.com/a/33956544
    '''
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

try:
    py_version = sys.argv[1]
except IndexError:
    print('No version specified')
    sys.exit(1)

# Load template file
with open('template.xml', 'r') as f:
    tree = ET.parse(f)
    root = tree.getroot()

# Load version dependencies
with open(f'{py_version}.yaml', 'r') as f:
    deps = yaml.safe_load(f)

# Populate xml template
for dep in deps:
    ET.SubElement(root.find('requires'), 'import', attrib=dep)

# Format xml tree
indent(root)

# Update version string
addon_version = root.attrib['version']
root.attrib['version'] = f'{addon_version}-{py_version}'

tree.write('../addon.xml', encoding='utf-8', xml_declaration=True)
