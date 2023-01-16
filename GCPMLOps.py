#DataScience DataSource
import pandas as pd
import numpy as np
import uuid

class SimpleTimer():
    def __init__(self, name):
        self.name = name
        self.start = pd.Timestamp.now()
        print("Starting " + self.name + " at " + str(self.start))

    def Stop(self):
        self.end = pd.Timestamp.now()
        print("Stopping " + self.name + " at " + str(self.end))
        print("Elapsed time for " + self.name + " is " + str(self.end - self.start))
    
    def GetElalpsed(self):
        return self.end - self.start

class DataSource():

    def __init__(self,ProjectID,filetype,sourceEnvironment,ExtractQuery):
        self.guid = str(uuid.uuid4())
        self.filetype = filetype
        self.ProjectID = ProjectID
        self.sourceEnvironment = sourceEnvironment
        self.ExtractQuery = ExtractQuery
        self.loadedDate = pd.Timestamp.now()
        self.TargetTable =filetype + "_" + self.loadedDate.strftime("%Y_%m_%d") + "_" + self.guid
        
    def WriteEntry(self):
        print("Writing Entry")
        self.WriteToBQ()

    def WriteToBQ(self):        
        frame=[{"Filetype":self.filetype,
            "LoadedDate":self.loadedDate,
            "SourceEnvironment":self.sourceEnvironment,
            "ExtractQuery":self.ExtractQuery,
            "TargetTable":self.TargetTable,
            "GUID":self.guid}]
        #print(frame)
        df = pd.DataFrame(frame)
        df.to_gbq("DATASCIENCE_SOURCEDATA._datasources", project_id=self.ProjectID, if_exists='append')

    @staticmethod    
    def GetLatest(ProjectID,fileType):
        query="""SELECT * FROM `datawx.DATASCIENCE_SOURCEDATA._datasources`
            where Filetype="{0}"
            order by LoadedDate desc
            limit 1""".format(fileType)

        #Get first row
        df = pd.read_gbq(query, project_id=ProjectID)
        row = df.iloc[0]
        source=DataSource(ProjectID,row["Filetype"],row["SourceEnvironment"],row["ExtractQuery"])
        source.loadedDate=row["LoadedDate"]
        source.TargetTable=row["TargetTable"]
        return source

# class TrainingMetrics():

    # @staticmethod
    # def SaveMetrics(self,ExperimentName,ModelName,ModelVersion,ModelType,trainingTime:SimpleTimer):
    #     frame=[{"ExperimentName":ExperimentName,
    #         "ModelName":ModelName,
    #         "ModelVersion":ModelVersion,
    #         "ModelType":ModelType,
    #         "TrainingTime":trainingTime.GetElalpsed().total_seconds()}]
    #     print(frame)
    #     df = pd.DataFrame(frame)
    #     df.to_gbq("DATASCIENCE_MODELS._trainingmetrics", project_id=ProjectID, if_exists='append')


