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

def main():
    # wb = xw.Book.caller()
    # sheet = wb.sheets[0]
    # if sheet["A1"].value == "Hello xlwings!":
    #     sheet["A1"].value = "Bye xlwings!"
    # else:
    #     sheet["A1"].value = "Hello xlwings!"
    print("Hello world")


@xw.func
def hello(name):
    os.environ['CURL_CA_BUNDLE'] = ''
    return f"Hello fucken {name}!"

@xw.func
def InferAdjustmentName(name):
    
    os.environ['CURL_CA_BUNDLE'] = ''

#Load Embeddings model

    # Load the pre-trained BERT model and tokenizer
    model_name = "cross-encoder/ms-marco-TinyBERT-L-2-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    embeddingsmodel = AutoModel.from_pretrained(model_name)

    # Check if a GPU is available and move the model to the GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    embeddingsmodel.to(device)    

    #Test functionaliy
    # Tokenize the text field and create a tensor with the token IDs
    text_field = "This is an example text field."
    inputs = tokenizer(text_field, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Obtain the embeddings
    with torch.no_grad():
        outputs = embeddingsmodel(**inputs)
        embeddings = outputs.last_hidden_state

    # Calculate the average embedding
    avg_embedding = embeddings.mean(dim=1).squeeze().cpu().numpy()
    return(str(avg_embedding))


if __name__ == "__main__":
    xw.Book("AdjustmentTemplate.xslm.xslm").set_mock_caller()
    main()

