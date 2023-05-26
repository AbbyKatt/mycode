import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Controls and Program Flow")

#This is a demo of how a Streamlit program works
#Write Python code like you normally would - Execution runs from top to bottom
#Streamlit waits and serves as data as it's available

#Initial status message - Please wait!
stattitle=st.text("Computing Output Values 1/5")


#Simulate some "real work" by sleeping for 5 seconds
#Calculate some simple sin curves
# - Note the st.cache decorator - this will cache the output of this function
#   so that it doesn't have to be recalculated every time the page is refreshed
# use this for long running requests that remain static -> for example a database query
#@st.cache 
def GetSignal():
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.sin(x*2.5+np.pi/2)
    y3 = np.sin(x*7.5+np.pi)
    sinSet=pd.DataFrame({"x":x,"y1":y1,"y2":y2,"y3":y3})
    for i in range(1,6):
        time.sleep(1)
        stattitle.text("Computing Output Values {}/5".format(i+1))
    stattitle.text("Done")

    return sinSet

#Display the sin curves
sinSet=GetSignal()
st.line_chart(sinSet[["y1","y2","y3"]])

#build an fft histogram
st.text("FFT of y1+y2+y3")
st.bar_chart(np.abs(np.fft.fft(sinSet["y1"]+sinSet["y2"]+sinSet["y3"])))

#Display a simple dataframe
if st.checkbox('Show raw dataframe'):
    st.dataframe(sinSet)






