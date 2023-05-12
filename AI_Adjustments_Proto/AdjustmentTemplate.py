#Python AI Adjustment XLWings template Macro
# Version 1.0

import json
import string
import xlwings as xw
import pandas as pd
import tensorflow as tf
from transformers import AutoTokenizer, AutoModel
import torch
import os
import openai


#define global variables
modelsLoaded=False
global embeddingsmodel
global tokenizer
global device
global adjLabelModel
global adjLabelsInvDict
global adjLinkagesModel
global adjLinkagesInvDict
global adjLinkagesQuery
global AdjustmentValuesModel
global adjValcolumn_names
global adjValnumeric_fields
global adjValfield_metrics
global adjValsoftmaxlkp
global adjLinkagesColumns

def main():
    print("Hello world")

@xw.func
def LoadModels():

    import json

    global modelsLoaded
    global embeddingsmodel
    global tokenizer
    global device
    global adjLabelModel
    global adjLabelsInvDict
    global adjLinkagesModel
    global adjLinkagesInvDict
    global adjLinkagesQuery
    global AdjustmentValuesModel
    global adjValcolumn_names
    global adjValnumeric_fields
    global adjValfield_metrics
    global adjValsoftmaxlkp
    global adjLinkagesColumns
    

    if modelsLoaded:
        print("***Models already loaded***")
        return True

    print("--------------------Loading Models---------------------")
    os.environ['CURL_CA_BUNDLE'] = ''
    # Load the pre-trained BERT model and tokenizer
    print("Loading BERT model and tokenizer...")
    model_name = "cross-encoder/ms-marco-TinyBERT-L-2-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    embeddingsmodel = AutoModel.from_pretrained(model_name)

    # Check if a GPU is available and move the model to the GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    embeddingsmodel.to(device)
    
    #Load adjLabelModel 
    print("Loading Adjustment Labels Model NLP...")
    modelPath="""C:\code\HSBCDataScience\AI_Adjustments_Proto\Models\AdjustmentNameNLP\model.h5"""
    adjLabelModel = tf.keras.models.load_model(modelPath)

    #Load adjLabelsInvDict
    adjLabelsInvDictPath="""C:\code\HSBCDataScience\AI_Adjustments_Proto\Models\AdjustmentNameNLP\softmaxlkp.json"""
    with open(adjLabelsInvDictPath) as json_file:
        adjLabelsInvDict = json.load(json_file)

    #Load Adjustment Linkages Model
    print("Loading Adjustment Linkages Model...")
    modelPath="""C:\code\HSBCDataScience\AI_Adjustments_Proto\Models\AdjustmentLinkages\model.h5"""
    adjLinkagesModel = tf.keras.models.load_model(modelPath)

    #Load Adjustment Linkages Query JSON
    adjLinkagesColumns="""C:\code\HSBCDataScience\AI_Adjustments_Proto\Models\AdjustmentLinkages\in_Columsn.json"""
    with open(adjLinkagesQueryPath) as json_file:
        adjLinkagesColumns = json.load(json_file)

    #Load Adjustment Linkages Query JSON
    adjLinkagesQueryPath="""C:\code\HSBCDataScience\AI_Adjustments_Proto\Models\AdjustmentLinkages\query.json"""
    with open(adjLinkagesQueryPath) as json_file:
        adjLinkagesQuery = json.load(json_file)
    
    #Load Adjustment Linkages Inverse Dictionary
    adjLinkagesInvDictPath="""C:\code\HSBCDataScience\AI_Adjustments_Proto\Models\AdjustmentLinkages\softmaxlkp.json"""
    with open(adjLinkagesInvDictPath) as json_file:
        adjLinkagesInvDict = json.load(json_file)

    print("Loading Adjustment Values Model...")
    modelPath="""C:\code\HSBCDataScience\AI_Adjustments_Proto\Models\AdjustmentValues"""
    AdjustmentValuesModel= tf.keras.models.load_model(modelPath+"\\model.h5")

    #Load column names
    print("Loading Adjustment Values Input Columns...")
    adjValcolumn_names=[]
    import json
    with open(modelPath + '\in_columnnames.json') as json_file:
        adjValcolumn_names = json.load(json_file)

    #Load numeric fields definition
    print("Loading Adjustment Values Input Numeric Fields...")
    adjValnumeric_fields=[]
    import json
    with open(modelPath + '\in_numericfield.json') as json_file:
        adjValnumeric_fields = json.load(json_file)

    #Load field metrics for scaling
    print("Loading Adjustment Values Input Field Metrics...")
    adjValfield_metrics={}
    import json
    with open(modelPath+'\in_fieldmetrics.json') as json_file:
        adjValfield_metrics = json.load(json_file)

    #Load softmaxlkp
    print("Loading Adjustment Values Output Softmax Lookup...")
    adjValsoftmaxlkp={}
    import json
    with open(modelPath+'\softmaxlkp.json') as json_file:
        adjValsoftmaxlkp = json.load(json_file)        


    modelsLoaded=True
    print("--------------------Models Loaded---------------------")
    return True

#NLP Adjustment Base Name Inference-----------------------------------------------------------------------------------------------------------------

#Uses NLP embeddings to get back to base adjustment name
@xw.func
def InferAdjustmentName(name):
    global modelsLoaded
    global embeddingsmodel
    global tokenizer
    global device
    global adjLabelModel
    global adjLabelsInvDict
    LoadModels()

    text_field = name
    inputs = tokenizer(text_field, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    # Obtain the embeddings
    with torch.no_grad():
        outputs = embeddingsmodel(**inputs)
        embeddings = outputs.last_hidden_state

    # Calculate the average embedding
    avg_embedding = embeddings.mean(dim=1).squeeze().cpu().numpy()
    avg_embedding

    import numpy as np
    df_query = pd.DataFrame(avg_embedding.reshape(1, 128))
    df_query

    #Make a prediction
    ret=adjLabelModel.predict(df_query)

    #Get the index of the highest value
    ret=np.argmax(ret)
    #ret

    #print(adjLabelsInvDict)

    # #Get the AdjustmentName from the index
    return adjLabelsInvDict[str(ret)]


#Adjustment Linkages Inference----------------------------------------------------------------------------------------------------------------------



#Field Value Inference------------------------------------------------------------------------------------------------------------------------------

#Populate the dataframe in AI format with numeric values
def Normalize(col, min, max):
    return (col-min)/(max-min)*2-1

#Onehot encode known fields
def ApplyOneHotField(df,fieldName,valu):
    fieldNameOH=fieldName+'_'+str(valu)

    #Check if the field exists
    if fieldNameOH in df.columns:
        #If it does, set it to 1
        df[fieldNameOH]=1
    else:
        print("***No field found for "+fieldNameOH+" in dataframe with value "+str(valu)+" - skipping")

    return df

#Takes a whole stream of values and returns the adjustment field
@xw.func
def InferAdjustmentValue(requestJSON):
    global AdjustmentValuesModel
    global adjValcolumn_names
    global adjValnumeric_fields
    global adjValfield_metrics
    global adjValsoftmaxlkp

    import pandas as pd
    import numpy as np
    import json

    #Lazy load models
    LoadModels()

    #parse requestJSON
    requestJSON=json.loads(requestJSON)

    #Build a pandas dataframe filled with zeros
    df = pd.DataFrame(0, index=np.arange(1), columns=adjValcolumn_names)

    #Load and Normalize all numeric fields
    for field in adjValnumeric_fields:
        #Load un-normalized value
        df[field]=requestJSON[field]

        if field in adjValfield_metrics:
            #Load metrics
            min=adjValfield_metrics[field][0]
            max=adjValfield_metrics[field][1]

            #Normalize
            df[field]=Normalize(df[field], min, max)

    #Apply the strings in the rest of request as onehot encoded
    for field,valu in requestJSON.items():
        if field in adjValnumeric_fields:
            #Skip 
            continue
        else:
            df=ApplyOneHotField(df,field,valu)       

    #drop index
    df=df.drop(df.columns[0], axis=1)

    with tf.device('/gpu:0'):
        predictions = AdjustmentValuesModel.predict(df)
        print(predictions)

    #Get argmax value
    argmax = np.argmax(predictions[0])    
    print(argmax)
    result=adjValsoftmaxlkp[str(argmax)]
    print(result)
    return (result)


#Field linkage inference --------------------------------------------------------------------------------------------------------------------------




#--------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    xw.Book("AdjustmentTemplate.xslm.xslm").set_mock_caller()
    main()

