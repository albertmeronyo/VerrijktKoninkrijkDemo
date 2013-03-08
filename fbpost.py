#!/usr/bin/env python
from pyfb import Pyfb
from SPARQLWrapper import SPARQLWrapper, JSON, POST
from rdflib import URIRef
import urllib
from xml.dom import minidom

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

#Your APP ID. It Needs to register your application on facebook
#http://developers.facebook.com/
FACEBOOK_APP_ID = '305584816233697'
token = 'AAAEV7YJrnOEBALvQ9i82Ev9zI7ZB3BIuZB5Lw3CDw9ozaH2HrQyRryShd5s2iIYXssjHmXGNEnT1fQ9TH458vAgXvxSg0pHIgXqq2ZCTgZDZD'

facebook = Pyfb(FACEBOOK_APP_ID)

#Opens a new browser tab instance and authenticates with the facebook API
#It redirects to an url like http://www.facebook.com/connect/login_success.html#access_token=[access_token]&expires_in=0
#facebook.authenticate()

#Copy the [access_token] and enter it below
#token = raw_input("Enter the access_token\n")

#Sets the authentication token
facebook.set_access_token(token)

#Gets info about myself
me = facebook.get_myself()

print "-" * 40
print "Name: %s" % me.name
print "From: %s" % me.hometown.name
print

print "Speaks:"
for language in me.languages:
    print "- %s" % language.name

print
print "Worked at:"
for work in me.work:
    print "- %s" % work.employer.name

print "-" * 40

#msg = raw_input("Enter message to post\n")

# Get data from SPARQL endpoint
sparql = SPARQLWrapper('http://alberts-macbook-pro-3.local:3020/sparql/')

query = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX niod: <http://purl.org/collections/nl/niod/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dbp-prop: <http://nl.dbpedia.org/property/>
PREFIX dbp-res: <http://nl.dbpedia.org/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?pref WHERE {
    ?entity niod:nerClass niod:nerclass-per;
        owl:sameAs <http://dbpedia.org/resource/Benito_Mussolini>;
    niod:pRef ?pref.
}
LIMIT 100
    """

sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    xmldoc = urllib.urlopen(result["pref"]["value"])
    msg = ''.join(xmldoc.readlines()[1:])
    dom = minidom.parseString(msg)
    quotes = dom.getElementsByTagName('quote')
    for q in quotes:
        facebook.publish(getText(q.childNodes))
    #print msg
    # facebook.publish(msg)
    
    
print "Done."