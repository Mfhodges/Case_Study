#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Provide routines to import DPLA project data set into list of lists format.
& do a query & filter by one of the 4 fields

Fields wanted:
 1. Search Term ??
 2. ID
 3. Ingest Date
 4. Data Provider

PARAMETERS
 &fields=id,dataProvider,ingestDate
 &sort_order= 'asc' or 'desc'
 # SORT ON BY ID?
 &sort_by= 'id' or 'dataProvider' or 'ingestDate'
 &api_key
Request only the title and id fields
http://api.dp.la/dev/items?q=town&fields=aggregatedCHO.title,id


https://github.com/dpla/platform/wiki/Code4Lib-API-Documentation


things to consider:
how to handle an error when reading a file ?
API call limits?

For each item, the parent object docs contains information about how that item was imported into the database: for example, ingestDate and other context about the record (see @context).
Down in the sourceResource object, there’s information about the title and subject of the work. Here, the enumerated subject name: "Weasels" probably accounts for this being the first result.

"""


import json
import csv
import urllib.request
import argparse

#parser = argparse.ArgumentParser(description='DPLA api call')

#make the below necessary
#add filter on field and to make ascending or descending
#type check!

#parser.add_argument('-q', '--q',
#                    help='the term to query  ___')
#parser.add_argument('-resource',
#                    help='the resource_type')

#args = vars(parser.parse_args())
# change these for other api calls
base_URL = 'https://api.dp.la/v2/'
api_key = 'bd42082e8bd7b7eedf534a0256da1b6d'
fields = ['id','dataProvider']#,'ingestDate']
stringfields = ','.join(fields)

class get_json:
    def __init__(self, url, api_key):
        self.url = url
        self.key = '&api_key='+api_key  # i would like to make this individual to me
        ## need to be set ##
        self.qterm = 'q=' # this could be a list?
        self.resource =None
        ## not required ##
        self.sort_by= '&sort_by=' #single field
        self.sort_order ='&sort_order=' #asecending or descending
        ## assumed ##
        self.fields = '&fields=' + stringfields # hard-coded - not ideal

        #self.parameters = make this a list of the parameters !

    # Method for setting query
    def set_query(self,query=None):
        if not query:
            raise NameError('Provide a term to query for the API!')
        else:
            self.qterm+=query

    # Method for setting query
    def set_resource(self,resource=None):
        if not resource:
            raise NameError('Provide a term to resource for the API!')
        else:
            self.resource =  resource

    def set_sort(self, sort_by=None, sort_order='asc'):
        #ascending or descending ?

        if not sort_by:
            raise NameError('Provide a field to seach by : search_term, ID, ingest_date, data_provider')
        elif sort_by not in fields:
            raise NameError('Provide a proper field to seach by : search_term, ID, ingest_date, data_provider')
        else:
            #typecheck that its in the fields !
            self.sort_by += sort_by
            if sort_order == 'desc':
                self.sort_order +='desc'
            else:
                self.sort_order +='asc'

    # Extract data from json api
    # EDIT THIS TO BE ABLE TO QUERY
    def get_data(self, write_to_csv=False):
        # must have self.resource .qterm and key filled out.
        if self.resource == None or self.qterm == 'q=':
            raise( 'set a qterm and resource before you call the api')
        else:
            url = self.url + self.resource +'?'+ self.qterm + self.fields + self.sort_by + self.sort_order + self.key
        return url
            #with urllib.request.urlopen(self.url) as url:
            #    data = json.loads(url.read().decode())


if __name__ == '__main__':

    # add stuff here !
    # dpla = get_json(base_URL)
    #print(args,"\n")
    dpla = get_json(base_URL,api_key)
    dpla.set_query('kittens')
    dpla.set_resource('items')
    dpla.set_sort('id','asc')
    print(dpla.get_data())


        # data = dpla.get_data()
        # print (data[0]['text'])
