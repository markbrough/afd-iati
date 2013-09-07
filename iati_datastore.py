from lxml import etree
import urllib2
import os

URL = "http://iati-datastore.herokuapp.com/api/1/access/activity.xml?recipient-country=ML&limit=100"
URL_OFFSET = "http://iati-datastore.herokuapp.com/api/1/access/activity.xml?recipient-country=ML&limit=100&offset=%s"

def download_data():
    def write_data(doc, offset):
        path = os.path.join("iati_data_" + str(offset/100) + '.xml')
        iati_activities = etree.tostring(doc.find("iati-activities"))
        with file(path, 'w') as localFile:
            localFile.write(iati_activities)

    offset = 0
    while True:
        try:
            if (offset >0):
                the_url = URL_OFFSET % (offset)
                print the_url
            else:
                the_url = URL
                print the_url

            xml_data = urllib2.urlopen(the_url, timeout=60).read()
            doc = etree.fromstring(xml_data)
            write_data(doc, offset)
            offset += 100

        except urllib2.HTTPError, e:
            print "Error %s" % str(e)
            break

download_data()
