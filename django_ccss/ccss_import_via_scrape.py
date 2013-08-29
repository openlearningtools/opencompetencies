import xml.etree.ElementTree as ET
import requests
from django_ccss.models import *

standard = Standard.objects.get(pk=2)

def get_statement_from_url(url, component_dn):
    r = requests.get(url)
    if r.status_code == 200:

        #print '\n\n---url', url
        #print '\nstring', r.text

        root = ET.fromstring(r.text)
        #print '\nroot', root
        if root.findall('.//content'):
            content_string = root.findall('.//content')[0].text
            if 'Error 404' in content_string:
                #print 'failed, 404 in xml'
                return False
        component = root.findall('.//Statement')[0]
        print '\nComponent:', component.text
        new_component = Component()
        new_component.component = component.text
        new_component.standard = standard
        new_component.dot_notation = 'CCSS.ELA-Literacy.W.9-10.2.' + component_dn
        new_component.save()
        print '\n*** nc: ', new_component
        return True
    else:
        print 'failed', r.status_code, type(r.status_code)
        return False


for component_dn in ['a','b','c','d','e','f','g','h','i']:
    urlstring = 'http://www.corestandards.org/ELA-Literacy/W/9-10/2/' + component_dn + '.xml'
    element_found = get_statement_from_url(urlstring, component_dn)
    if not element_found:
        break

print '\n\nFinished.\n\n'
