import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Widgets and Controls Demo')
#Read this for a simple explanation: https://docs.streamlit.io/library/get-started/main-concepts

st.text("Streamlit makes it super easy to add UI elements to your code without massive\nrestructuring or complex callbacks.\nSimply add a line of code to read a value from a widget and you're done!")
st.text("The program will automatically rerun when you change a value in a widget")
st.text("Lets have some fun adding widgets and controls to our previous examples")


def GetSignal(xS,yS,zS):
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x*xS)
    y2 = np.sin(x*yS+np.pi/2)
    y3 = np.sin(x*zS+np.pi)
    sinSet=pd.DataFrame({"x":x,"y1":y1,"y2":y2,"y3":y3})
    return sinSet

#Simply read a value from a widget into a variable -> the program will restart with new value when the widget is changed
xS=st.slider("X Scale",0.0,10.0,1.0)
yS=st.slider("Y Scale",0.0,10.0,2.5)
zS=st.slider("Z Scale",0.0,10.0,7.5)

sinSet=GetSignal(xS,yS,zS)
st.line_chart(sinSet[["y1","y2","y3"]])

st.text("FFT of y1+y2+y3")
st.bar_chart(np.abs(np.fft.fft(sinSet["y1"]+sinSet["y2"]+sinSet["y3"])))

#Display a simple dataframe
if st.checkbox('Show raw dataframe CHECKBOX example'):
    st.dataframe(sinSet)

st.text("There are also a whole range of other controls - for example a dropdown list")
listItems=["Item 1","Item 2","Item 3","Item 4"]
listSelect=st.selectbox("Select an item",listItems)
st.text("You selected: {}".format(listSelect))

#input example
st.text("You can also get text input from the user")
inputText=st.text_input("Enter some text")
st.text("You entered: {}".format(inputText))

#Get user names
st.text("You can also get user names")
userName=st.text_input("Enter your name")

#Get users address
st.text("You can also get user address")
userAddress=st.text_input("Enter your address")

#Get users phone number
st.text("You can also get user phone number")
userPhone=st.text_input("Enter your phone number")

#Put into dataframe
userDetails=pd.DataFrame({"Name":[userName],"Address":[userAddress],"Phone":[userPhone]})
st.dataframe(userDetails)

#Write to GBQ
if st.button("Write to BigQuery"):
    st.text("Lets write the user details to a BigQuery table")
    userDetails.to_gbq("streamlit_demo.user_details",project_id="datawx",if_exists="replace")










