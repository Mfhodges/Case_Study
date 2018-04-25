# Welcome

**Task:** "Provide routines to import DPLA project data set into list of lists format by do a query with the api and filter by one of the 4 fields"



< Brief how to run goes here >  
reminder it defaults to python3

**Input:**
 "Your program should accept a file containing a list of item terms (one term per line) to search for via the DPLA API and should provide a way to specify which report field(s) to sort on."


**Output:**
Report in a format of your choosing (CSV, HTML, Excel,etc )



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
 4. Data Provider `provider`  
 Service or content hub providing access to the Data Provider’s content. May contain the same value as Data Provider. (literal value in this version) (EDM)

Example:
	https://api.dp.la/v2/items?q=kittens&api_key=XXXXX

Semantic URL Units
 1. base_URL: https://api.dp.la/v2/
 2. Resource_type: items or collections ( path )  

 **( Parameters )**  
 3. query_Indicator: '?q'  (FIND BETTER WORD FOR THIS )  
 4. query_term: 'kittens'  
 5. api_part: 'api_key'  
 6. my_api_key: XXXXXXX     

Within a URL, parameters follow the '?'. They are specified by '<parameter>=<user_input>' are separated by '&'.




"""
