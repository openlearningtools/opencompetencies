import xml.etree.ElementTree as ET
filepath = '/home/ehmatthes/development_resources/project_notes/opencompetencies/Resources/standards/ccss_W_9-10.xml'

tree = ET.parse(filepath)
root = tree.getroot()

"""
print 'tag', root.tag
print 'attrib', root.attrib

for child in root:
    pass#print 'child tag, child attrib', child.tag, child.attrib

print '----\n'

for lsi in root:
    for child in lsi:
        if child.tag == 'StandardHierarchyLevel':
            for grandchild in child:
                if grandchild.tag == 'description':
                    if grandchild.text == 'Standard':
                        pass#print child[
"""


for lsi in root:
    for description in lsi.iter('description'):
        print description.text
