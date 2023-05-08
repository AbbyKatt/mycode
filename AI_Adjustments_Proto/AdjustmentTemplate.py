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

def main():
    print("Hello world")

@xw.func
def LoadModels():
    global modelsLoaded
    global embeddingsmodel
    global tokenizer
    global device
    global adjLabelModel
    global adjLabelsInvDict

    if modelsLoaded:
        print("***Models already loaded***")
        return True

    print("--------------------Loading Models---------------------")
    os.environ['CURL_CA_BUNDLE'] = ''
    # Load the pre-trained BERT model and tokenizer
    model_name = "cross-encoder/ms-marco-TinyBERT-L-2-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    embeddingsmodel = AutoModel.from_pretrained(model_name)

    # Check if a GPU is available and move the model to the GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    embeddingsmodel.to(device)
    
    #Load adjLabelModel 
    modelPath="""C:\code\HSBCDataScience\AI_Adjustments_Proto\Models\AdjustmentNameNLP\model.h5"""
    adjLabelModel = tf.keras.models.load_model(modelPath)

    #Load adjLabelsInvDict
    adjLabelsInvDictPath="""C:\code\HSBCDataScience\AI_Adjustments_Proto\Models\AdjustmentNameNLP\softmaxlkp.json"""
    with open(adjLabelsInvDictPath) as json_file:
        adjLabelsInvDict = json.load(json_file)

    modelsLoaded=True
    print("--------------------Models Loaded---------------------")
    return True


@xw.func
def hello(name):
    os.environ['CURL_CA_BUNDLE'] = ''
    return f"Hello fucken {name}!"

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

if __name__ == "__main__":
    xw.Book("AdjustmentTemplate.xslm.xslm").set_mock_caller()
    main()

