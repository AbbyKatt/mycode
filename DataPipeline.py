#--------------------------------------------------------------------------------------------------------------------------------------------------
# Semi-Automated Data Conveyor
# Purpose: This script is used to automate the process of copying data from a source to a target.  It is intended to be used as a semi-automated process
#--------------------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
from GCPMLOps import DataSource 
import sys
from google.cloud import bigquery
from google.oauth2 import service_account

#Get command line parameters
if len(sys.argv) > 5:
    ProjectID=sys.argv[1]
    queryFile=sys.argv[2]
    targetDataset=sys.argv[3]
    serviceAcct=sys.argv[4]
    FileType=sys.argv[5]
else:
    print("Usage: DataPipeline.py <ProjectID> <QueryFile> <TargetDataset> <ServiceAccount> <FileType>")
    sys.exit(1)

#Load SQL from file
try:
    print("Reading query from:" + queryFile)
    with open(queryFile, 'r') as myfile:
        query=myfile.read()

    #Create Data Source Entry
    print("Creating Data Source Entry")
    source=DataSource(ProjectID,FileType,"DEV",query)

    #Set up query to transfer data from source to target
    print("Copying data from source to target")
    credentials = service_account.Credentials.from_service_account_file(serviceAcct)
    job_config = bigquery.QueryJobConfig()
    job_config.destination = ProjectID + "." + targetDataset + "." + source.TargetTable
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job_config.use_legacy_sql = False

    #Run Query
    client = bigquery.Client(credentials= credentials,project=ProjectID)
    query_job = client.query(query, job_config=job_config)

    #Finalize Data Source Entry only if we succeded
    source.WriteEntry()

    #Get latest feed for testing
    src=DataSource.GetLatest(ProjectID,FileType)
    print("Target Table:" + src.TargetTable)

    #Future release -> Use Great-Expectations to validate data
    #https://docs.greatexpectations.io/en/latest/guides/how_to_guides/creating_and_editing_expectations/how_to_create_an_expectation_suite_without_a_sample_batch.html
    #GE.Validate()

except Exception as e:
    print("Error Copying Sample data:" + str(e))
    #Dump full stack trace exception
    import traceback
    traceback.print_exc()
    sys.exit(2)

finally:
    print("Done")
    sys.exit(0)


