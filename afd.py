#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Scripts to convert project data from the French AFD website to the 
# IATI-XML format.

# Copyright 2013 contributors.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License v3.0 as 
# published by the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

from lxml import etree
from lxml.etree import *
#from xml.etree.cElementTree import Element, ElementTree
import urllib2
import os
import unicodecsv
from datetime import datetime
from lib import afdhelpers
import iatisegmenter

URL = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=afd_1&query=select+*+from+%60swdata%60&apikey="
countries_csv = 'lib/french_country_codes.csv'

# Basic data setup
reporting_org = u'Agence Fran\xe7aise de D\xe9veloppement'
reporting_org_id = u"FR-3"
reporting_org_type = u"10"

def download_data():
    regions = {'MULTI-PAYS': '998'}

    def getCountries():
        countries = []
        countries_file = open(countries_csv)
        countries_data = unicodecsv.DictReader(countries_file)
        for country in countries_data:
            countries.append((
                country['country_name'], country['country_code']
            ))
        return dict(countries)

    countries = getCountries()

    def correctCountry(name):
        countries = afdhelpers.AFD_COUNTRIES
        return countries[name]

    def getCountryCode(country_name):
        try:
            return countries[country_name]
        except Exception:
            return countries[correctCountry(country_name)]

    def checkIfRegion(name):
        if name in regions:
            return True
        return False

    def makeISO(date):
        if len(date)<10:
            return ""
        return date[6:10]+"-"+date[3:5]+"-"+date[0:2]

    def getStatus(status, type):
        status=status.encode('utf-8')
        mappings = afdhelpers.AFD_STATUSES
        statuses = afdhelpers.STATUSCODES
        if type =='code':
            return mappings[status]
        else:
            return statuses[mappings[status]]

    def getFinanceType(name, type):
        financetypes = afdhelpers.FINANCETYPES
        return financetypes[name][type]

    def getSector(status, type):
        status=status.encode('utf-8')
        mappings = afdhelpers.AFD_SECTORS
        statuses = afdhelpers.SECTORS
        if type =='code':
            return mappings[status]
        else:
            return statuses[mappings[status]]

    def removeDuplicates(doc):

        def f7(seq):
            seen = set()
            seen_add = seen.add
            # adds all elements it doesn't know yet to seen and all other to seen_twice
            seen_twice = set( str(x) for x in seq if x in seen or seen_add(x) )
            # turn the set into a list (as requested)
            return list( seen_twice )

        #doc = etree.tostring(doc)
        iati_identifiers = doc.xpath('//iati-identifier/text()')
        duplicates = f7(iati_identifiers)

        for did in duplicates:
            print "Removing all activities with duplicated identifier", did
            for duplicate in (doc.xpath("//iati-identifier[text()='%s']" % did)):
                duplicate.getparent().remove(duplicate)
        return doc
        
    def write_project(doc, row):
        #FIXME: currently excludes all activities with no project ID
        if row["id"] == "":
            return
        
        activity = Element("iati-activity")
        activity.set("default-currency", "EUR")
        activity.set("last-updated-datetime", makeISO(row["date_updated"])+"T00:00:00")
        doc.append(activity)

        rep_org = Element("reporting-org")
        rep_org.set("ref", reporting_org_id)
        rep_org.set("type", reporting_org_type)
        rep_org.text = reporting_org
        activity.append(rep_org)

        title = Element("title")
        title.text = row["name"]
        activity.append(title)

        description = Element("description")
        description.text = row["description"]
        activity.append(description)

        iati_identifier = Element("iati-identifier")
        iati_identifier.text = reporting_org_id+"-"+row["id"]
        activity.append(iati_identifier)

        activity_status = Element("activity-status")
        activity_status.set('code', getStatus(row["status"], 'code'))
        activity_status.text = getStatus(row["status"], 'text')
        activity.append(activity_status)

        start_date = Element("activity-date")
        start_date.set('type', 'start-planned')
        start_date.set('iso-date', makeISO(row["date_funded"]))
        activity.append(start_date)

        end_date = Element("activity-date")
        end_date.set('type', 'end-planned')
        end_date.set('iso-date', makeISO(row["date_funded"]))
        activity.append(end_date)

        if not checkIfRegion(row["country"]):
            recipient_country = Element("recipient-country")
            recipient_country.set('code', getCountryCode(row["country"]))
            recipient_country.text = row["country"]
            activity.append(recipient_country)
        else:
            recipient_region = Element("recipient-region")
            recipient_region.set('code', regions[row["country"]])
            recipient_region.text=row["country"]
            activity.append(recipient_region)

        funding_org = Element("participating-org")
        funding_org.set("role", "Funding")
        funding_org.set("ref", "FR")
        funding_org.set("type", "10")
        funding_org.text = "France"
        activity.append(funding_org)

        extending_org = Element("participating-org")
        extending_org.set("role", "Extending")
        extending_org.set("ref", reporting_org_id)
        extending_org.set("type", "10")
        extending_org.text = reporting_org
        activity.append(extending_org)

        implementing_org = Element("participating-org")
        implementing_org.set("role", "Implementing")
        implementing_org.text = row["beneficiary"]
        activity.append(implementing_org)

        finance_type = Element("default-finance-type")
        finance_type.set("code", getFinanceType(row["funding_type"], 'code'))
        finance_type.text = getFinanceType(row["funding_type"], 'text')
        activity.append(finance_type)

        sector = Element("sector")
        sector.set("code", getSector(row["aim"], 'code'))
        sector.set("vocabulary", "DAC")
        sector.text = getSector(row["aim"], 'text')
        activity.append(sector)

        activity_website = Element("activity-website")
        activity_website.text = "http://www.afd.fr/base-projets/consulterProjet.action?idProjet="+row["id"]
        activity.append(activity_website)

        if row["document_url"] != "":
            document_link = Element("document-link")
            document_link.set("url", row["document_url"])
            document_link.set("format", "application/pdf")
            document_title = Element("title")
            document_title.text = row["document_name"]
            document_link.append(document_title)
            document_category = Element("category")
            document_category.set("code", "A02")
            document_category.text = "Objectives / Purpose of activity"
            document_link.append(document_category)
            activity.append(document_link)

        transaction = Element("transaction")
        activity.append(transaction)
        ttype = Element("transaction-type")
        ttype.set("code", "C")
        ttype.text = "Commitment"
        transaction.append(ttype)

        tvalue = Element("value")
        tvalue.set('value-date', makeISO(row["date_funded"]))
        tvalue.text = row["funding_from_afd_euros"]
        transaction.append(tvalue)

        tdate = Element("transaction-date")
        tdate.set("iso-date", makeISO(row["date_funded"]))
        tdate.text=makeISO(row["date_funded"])
        transaction.append(tdate)

    try:
        print "Starting up ..."
        the_url = URL
        print "Attempting to retrieve data from", the_url

        csv_file = urllib2.urlopen(the_url, timeout=5)

        print "Got data from URL, generating activities..."
        csv_data = unicodecsv.DictReader(csv_file)

        doc = Element('iati-activities')
        doc.set("version", "1.02")
        current_datetime = datetime.now().replace(microsecond=0).isoformat()
        doc.set("generated-datetime",current_datetime)

        for row in csv_data:
            write_project(doc, row)

        XMLfilename = 'afd.xml'
        print "Writing activities..."

        # TODO: Allow this to be an option on the command line.
        doc=removeDuplicates(doc)
        doc = ElementTree(doc)
        doc.write(XMLfilename,encoding='utf-8', xml_declaration=True)
        print "Segmenting files..."
        prefix = 'afd'
        output_directory = os.path.realpath('afd')+'/'
        iatisegmenter.segment_file(prefix, XMLfilename, output_directory)
        print "Done"

    except urllib2.HTTPError, e:
        print "Error %s" % str(e)

download_data()
