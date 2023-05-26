import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Database Demo')
st.text("Since Streamlit is based around Pandas dataframes\nit makes it super easy to connect to a database and display the results")

st.text("Simple Query and Dataframe Display (cached for your temporal pleasure)")
#Best of all we can cache long running results queries!
@st.cache 
def GetSimpleSql():
    query="""SELECT * FROM `bigquery-public-data.samples.shakespeare` where word_count>100 LIMIT 10"""
    df=pd.read_gbq(query,project_id="datawx")
    return df

df=GetSimpleSql()
df


# #get list of fields from dataframe
fieldList=list(df.columns)

# #Check if "flag" exists in fieldname
selectedFields=[]
for field in fieldList:
    if "flag" in field:
        selectedFields.append(field)

#Join all selected fields into string, trim remaining comma
selectedFields=",".join(selectedFields).rstrip(",")


# #let user select field for report
st.text("Select a field to display")
fieldSelect=st.selectbox("Select a field",fieldList)
st.text("You selected: {}".format(fieldSelect))

# #copy fieldlist
# fieldList2=fieldList.copy()

# #remove fist index
# fieldList2.pop(0)

# #let user choose which fields to report on
# st.text("Select fields to display")
# fieldSelect=st.multiselect("Select fields",fieldList)
# st.text("You selected: {}".format(fieldSelect))

# df


# #display chart of selected fields only
# st.text("Lets draw a bar chart of that")
# st.line_chart(df[fieldSelect],x=df["word"])

#Build new frame using first column from df
# df2=pd.DataFrame({"word":df["word"]})

# #mormalize second column
# for field in fieldSelect:
#     df2[field]=df[field]/df[field].max()

# #Make a subtitle
# st.subheader("Lets normalize the data")

# #line break
# st.text("")


# #Read CYCODE
# ccyCodes=pd.read_csv("../CCYCODE.csv")

# #for each row in ccyCode
# mappng={}
# for index, row in ccyCodes.iterrows():
#     CCY=row["CCYCpd"]
#     #Add to mapping
#     mappng.update({CCY:row["CCYHome"]})


# derps=[]
# #Append tow to dataframe
# df2["CCYHome"]=df2["word"].map(mappng)


# df2

# #Lets draw a bar chart of that
# st.text("Lets draw a bar chart of that")
# st.bar_chart(df2[["word_count"]])

# #Create some map data with lat/long
# st.text("First we need to get the lat/long of the locations")
# testData=[{"location":"London","lat":51.5074,"lon":0.1278},
#         {"location":"New York","lat":40.7128,"lon":-74.0060},
#         {"location":"Paris","lat":48.8566,"lon":2.3522},
#         {"location":"Rome","lat":41.9028,"lon":12.4964},
#         {"location":"Venice","lat":45.4408,"lon":12.3155},
#         {"location":"Dublin","lat":53.3498,"lon":-6.2603}]
# testData=pd.DataFrame(testData)
# testData

# #Draw world map with data
# st.text("Its easy to do some REALLY advanced stuff")
# st.text("Here we use the backtraced home currency of the transaction currency to draw a world map")
# st.map(testData)

# #Draw map with thickness for variable
# st.text("We can also draw a map with thickness for variable")
# st.text("Here we use the backtraced home currency of the transaction currency to draw a world map")
# st.map(df,)

# #Draw a heatmap
# st.text("We can also draw a heatmap")
# st.text("Here we use the backtraced home currency of the transaction currency to draw a world map")








