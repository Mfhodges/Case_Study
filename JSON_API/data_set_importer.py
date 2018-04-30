#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Provide routines to import DPLA project data set into list of lists format.
& do a query & filter by one of the 4 fields

Fields wanted:
 1. Search Term
 2. ID
 3. Ingest Date
 4. Data Provider

PARAMETERS
 &fields=id,dataProvider,ingestDate # there is an issue with ingestDate and it does not work like this
 &sort_order= 'asc' or 'desc'
 # SORT ON BY ID
 &sort_by= 'id' or 'dataProvider' or 'ingestDate'
 &api_key

things to consider:
how to handle an error when reading a file ?

For each item, the parent object docs contains information about how that item was imported into the database: for example, ingestDate and other context about the record (see @context).
Down in the sourceResource object, there’s information about the title and subject of the work. Here, the enumerated subject name: "Weasels" probably accounts for this being the first result.

"""


import json
import csv
import urllib.request
import argparse
from operator import itemgetter


parser = argparse.ArgumentParser(description='DPLA api call')
#make the below necessary
#type check!
parser.add_argument('-f', required=True,action='store',help='filename of input')
parser.add_argument('-o', action='store',help='filename of output')
parser.add_argument('--resource',required=True,action='store',help='the resource_type',choices=['items','collections'])
parser.add_argument('-s',action='store',required=True,help='the field to sort on', choices=['id','dataProvider','ingestDate'])
parser.add_argument('--asc',action="store_true",help='sort by the specified field, smallest to largest')
parser.add_argument('--desc',action="store_true",help='sort by the specified field, largest to smallest')
args = vars(parser.parse_args())

# change these for other api calls
base_URL = 'https://api.dp.la/v2/'
api_key = 'bd42082e8bd7b7eedf534a0256da1b6d'
fields = ['id','dataProvider','ingestDate']
stringfields = ','.join(fields)

class get_json:
    def __init__(self, url, api_key):
        self.url = url
        self.key = '&api_key='+api_key  # i would like to make this individual to me
        ## need to be set ##
        self.qterm = ''
        self.resource =None
        ## not required ##
        self.sort_by= ''         #'&sort_by=' #single field
        self.sort_order = ''     #'&sort_order=' #asecending or descending
        ## assumed ##
        self.fields = '&fields=' + stringfields # hard-coded - not ideal

    # Method for setting query
    def set_query(self,query=None):
        if not query:
            raise NameError('Provide a term to query for the API!')
        else:
            self.qterm=query

    # Method for setting query
    def set_resource(self,resource=None):
        if not resource:
            raise NameError('Provide a term to resource for the API!')
        else:
            self.resource =  resource

    def set_sort(self, sort_by=None, sort_order='asc'):
        #ascending or descending ?
        if not sort_by:
            raise NameError('Provide a field to sort by : search_term, ID, ingest_date, data_provider')
        elif sort_by not in fields:
            raise NameError('Provide a proper field to sort by : search_term, ID, ingest_date, data_provider')
        else:
            #typecheck that its in the fields !
            self.sort_by = sort_by
            if sort_order == 'desc':
                self.sort_order ='desc'
            else:
                self.sort_order ='asc'

    # Extract data from json api
    def get_data(self):
        if self.resource == None or self.qterm == 'q=': # must have self.resource .qterm and key filled out.
            raise( 'set a qterm and resource before you call the api')
        else: #+ ' &fields='+self.fields +'&sort_by=' +self.sort_by + '&sort_order='+self.sort_order
            url = self.url + self.resource +'?'+ 'q='+self.qterm + self.key
            ## ideally url would = self.url + self.resource +'?'+ self.qterm  + self.fields + self.sort_by + self.sort_order+ self.key
            ## however, i was having an issue with ingestDate as a field so i am pulling the full query and then
        print(url)
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
        count = data['count'] # total number of items that match that query
        #max number of objects returned per page is 500. if not specified 10 are given.
        #url = self.url + self.resource +'?'+ 'q='+self.qterm +page_size=500 + self.key
        if count > 500:
            pages = count // 500
            if count % 500 != 0 : pages +=1
        else: #otherwise we have less than 500 objects so one page will suffice
            pages = 1
        print("pages",pages,"count",count)
        final_data = []
        for i in range(1,pages+1):# now pull for each page.
            url = self.url + self.resource +'?'+ 'q='+self.qterm +'&page_size=500&page='+str(i) + self.key
            print(url,"\n")
            with urllib.request.urlopen(url) as url:
                data = json.loads(url.read().decode())
                dataset = data['docs']
                keys = {'id','dataProvider','ingestDate'}
                filtered_data= list(map(lambda x: {k:v for k, v in x.items() if k in keys}, dataset)) # reduces to the 3 fields we want
                filtered_data = [dict(item, **{'query':self.qterm}) for item in filtered_data] # adds the query as a field
                final_data += filtered_data
        print("did we get all objects?: ", count==len(final_data)) # just to check we have everything

        # sorting if specified - reverse=True is descending
        if self.sort_by:
            if self.sort_order == 'desc':
                final_data = sorted(final_data, key=itemgetter(self.sort_by), reverse=True)
            else: #defaults to ascending
                final_data = sorted(final_data, key=itemgetter(self.sort_by))
        return final_data

    def write_to_csv(self,data,file_name):
        #file_name must be a string
        if file_name == None:
            file_name = 'results'
        with open( file_name +'.csv', 'w', newline='') as csvfile:
            header = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            for i in range(0,len(data)):
                writer.writerow(data[i])


if __name__ == '__main__':
    # dpla = get_json(base_URL)
    print(args,"\n") # example = {'f': 'sample_input.txt', 'o': 'results', 'resource': 'items', 's': 'id', 'asc': True, 'desc': False}
    with open(args['f']) as f:
        queries = f.read().splitlines()
    dpla = get_json(base_URL,api_key)
    dpla.set_resource(args['resource'])
    if args['desc'] == False:
        dpla.set_sort(args['s'],'asc')
    else:
        dpla.set_sort(args['s'],'desc')
    results = []
    for q in queries:
        dpla.set_query(q) # this will be varied
        dataset = dpla.get_data()#['docs']
        results += dataset
    dpla.write_to_csv(results,args['o'])


    ##### HARD CODED EXAMPLE #####
    #queries = ['kittens','kitten','cat']
    #dpla = get_json(base_URL,api_key)
    #dpla.set_resource('items')
    #dpla.set_sort('id','asc')
    #results = []
    #for q in queries:
    #    dpla.set_query('kittens') # this will be varied
    #    dataset = dpla.get_data()#['docs']
    #    results += dataset
    #dpla.write_to_csv(results,'kittens')
