import xml.etree.ElementTree as ET
import requests

def get_statement_from_url(url):
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
        return True
    else:
        print 'failed', r.status_code, type(r.status_code)
        return False


for component_dn in ['a','b','c','d','e','f','g','h','i']:
    urlstring = 'http://www.corestandards.org/ELA-Literacy/W/9-10/2/' + component_dn + '.xml'
    element_found = get_statement_from_url(urlstring)
    if not element_found:
        break

from django_ccss.models import *
standards = Standard.objects.all()
for standard in standards:
    print '\n\npk, standard:', standard.pk, standard


print '\n\nFinished.\n\n'
