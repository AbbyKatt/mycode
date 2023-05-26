import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


st.title('Plots and Charts Demo')

#Create a sample pie chart dataframe
st.text("Streamlit is centered around working easily with dataframes\nHere's a sample dataframe with a pie chart")
st.text("If you simply put the varuable name in a cell it will be displayed as a table")
pieData=pd.DataFrame({"Category":["Apples","Bananas","Carrots","Deltas","Epsilons"],"Value":[10,35,15,20,50]})
pieData

st.text("Also -> simply saving in the editor will cause the page to refresh.\nTry changing the data above!")

#Create a sample bar chart dataframe
st.text("Here's a sample dataframe with a bar chart")
st.bar_chart(pieData,x="Category")

#Area chart
st.text("Heres an Area Chart\nThere are MANY charts available in streamlit")
st.area_chart(pieData,x="Category")

#Display a heatmap example
st.text("You can also use Seaborn and MatplotLib plots\n Here's a heatmap example of visualizing a confusion matrix using seaborn")

#Create an example confusion matrix 
confusion=np.array([[0.5,0.3,0.4],[0.2,0.8,0.0],[0.1,0.1,0.8]])
fig, ax = plt.subplots()
sns.heatmap(confusion, ax=ax, annot=True, cmap="Blues")
st.write(fig)




