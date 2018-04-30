# Welcome

**Task:** "Provide routines to import DPLA project data set into list of lists format by doing a query with the api and filter by one of the 4 fields"

### How To Run
The python script `data_set_importer.py` accomplishes the task above and the parameters are set as command line arguments. An example of a command is:   
`$ python3 data_set_importer.py -f <input.txt> -o <output_file_name>  --resource <'items' or 'collections'> -s <field_to_sort_on> --asc`  

The flags '-f' and '--resource' are required . '-f' specifies the the input (defined below) and '--resource' specifies the resource type (either items or collections).  '-o' is the name of the output file and is optional (defaults to 'results').'-s' followed by one of the fields specifies to sort on that field and is optional. The sort order is set by the flag '--asc' (ascending) or '--desc' (descending). The sort order is optional and defaults to ascending if a field to sort on is provided and a sort order is not.


**Input:**
 "Your program should accept a file containing a list of item terms (one term per line) to search for via the DPLA API and should provide a way to specify which report field(s) to sort on."


**Output:**
A CSV ( name specified by '-o' flag ).


## Building the API call
Two Resource types:
 - collections
 - items

Fields wanted:
 1. Search Term  
 provided by user
 2. ID  `id`  
 DPLA ID of a SourceResource within a given context.  
 3. Ingest Date  `ingestDate`  
 Date on which the original record was imported into the DPLA database.
 4. Data Provider `Dataprovider`  
 Service or content hub providing access to the Data Provider’s content. May contain the same value as Data Provider. (literal value in this version) (EDM)

Example:
	https://api.dp.la/v2/items?q=kittens&api_key=XXXXX

URL Units (in order)
 1. base_URL: `https://api.dp.la/v2/`
 2. Resource_type: 'items' or 'collections'
 **( Parameters )**   
 4. query term: q=<term>
 5. fields: fields=id,dataProvider,ingestDate
 6. sort by: sort_by=<one of the fields>
 7. sortorder: sort_order=<asc or dec>
 8. api_key: api_key=<api_key>     

Within a URL, parameters follow the '?'. They are specified by '<parameter>=<user_input>' are separated by '&'.

## How my code works
The above describes the ideal way to build an API query however, I had an issue with ingestDate so I do not specify any of 5.-7. from the Url Units and instead use python to filter and manipulate the response as desired.


## Contributors :tada:
:octocat: [Maddy Hodges](https://github.com/Mfhodges)
