import streamlit as st
import pandas as pd
import numpy as np
import pycountry

st.title('My first app')

Loading=st.text('Loading Please wait...')

def test_TrueIsTrue():
    assert True == True

def test_FalseIsFalse():
    assert False == False

# def test_TrueIsFalse():
#     assert True == False
    

# dataframe = np.random.randn(10, 20)
# st.dataframe(dataframe, width=1000, height=500)

# # #Simple sine wave with clipping
# x = np.linspace(0, 2*np.pi, 100)
# y = np.sin(x)
# y[y<0] = 0
# st.line_chart(y)

# #BQ Test
# test=[
#     {"TestDate": "2020-01-01", "TestValue": 1, "DeltaPercent": 0.1, "CCY": "USD"},
#     {"TestDate": "2020-01-02", "TestValue": 2, "DeltaPercent": 0.2, "CCY": "GBP"},
#     {"TestDate": "2020-01-03", "TestValue": 3, "DeltaPercent": 0.3, "CCY": "GBP"},
#     {"TestDate": "2020-01-04", "TestValue": 4, "DeltaPercent": 0.4, "CCY": "EUR"},
#     {"TestDate": "2020-01-05", "TestValue": 8, "DeltaPercent": 0.1, "CCY": "USD"},
#     {"TestDate": "2020-01-06", "TestValue": 9, "DeltaPercent": 0.2, "CCY": "GBP"},
#     {"TestDate": "2020-01-07", "TestValue": 10, "DeltaPercent": 0.3, "CCY": "GBP"},
#     {"TestDate": "2020-01-08", "TestValue": 11, "DeltaPercent": 0.4, "CCY": "GBP"},
#     {"TestDate": "2020-01-09", "TestValue": 12, "DeltaPercent": 0.1, "CCY": "GBP"}
# ]
# testDF=pd.DataFrame(test)

# #Show schema for dataframe
# st.write(testDF.dtypes)

#write to csv
#testDF.to_csv('test.csv',index=False)


# st.bar_chart(testDF,x="TestDate")

# def toCountry(CCY):
#     #pycountry currency code to country name
#     currency = pycountry.currencies.get(alpha_3=CCY)
#     #Convert from currency to country name
#     country_name = pycountry.countries.get(numeric=currency.numeric)
#     if country_name==None:
#         return "Unknown"
#     else:
#         return country_name.name

# from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2

# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="AbbyKattsWebApp")
# def geolocate(country):
#     try:
#         # Geolocate the center of the country
#         loc = geolocator.geocode(country)
#         # And return latitude and longitude
#         return (loc.latitude, loc.longitude)
#     except:
#         # Return missing value
#         return np.nan

# currencies=pycountry.currencies
# CCYCode=[]
# for curr in currencies:
#     countryName=toCountry(curr.alpha_3)
#     if countryName=="Unknown":
#         lat=0
#         long=0
#     else:
#         coords=geolocate(countryName)
#         lat=coords[0]
#         long=coords[1]
#     CCYCode.append([curr.alpha_3,countryName,lat,long])
#     Loading.text('Loading Please wait...'+str(curr.alpha_3))

#     #bail after 10  
#     #if len(CCYCode)>5:
#     #    break

# df=pd.DataFrame(CCYCode,columns=['CCY','Country','Lat','Long'])
# #df.to_csv('CCYCode.csv')
# st.write(df)

# country_name = pycountry.pycountry
# #pycountry currency code to country name
# currency = pycountry.currencies.get(alpha_3=CCY)
# st.write(currency)

# #Convert from currency to country name
# country_name = pycountry.countries.get(numeric=currency.numeric)
# st.write(country_name.name)

# from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
# def get_continent(col):
#     try:
#         cn_a2_code =  country_name_to_country_alpha2(col)
#     except:
#         cn_a2_code = 'Unknown' 
#     try:
#         cn_continent = country_alpha2_to_continent_code(cn_a2_code)
#     except:
#         cn_continent = 'Unknown' 
#     return (cn_a2_code, cn_continent)

# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="AbbyKattsWebApp")
# def geolocate(country):
#     try:
#         # Geolocate the center of the country
#         loc = geolocator.geocode(country)
#         # And return latitude and longitude
#         return (loc.latitude, loc.longitude)
#     except:
#         # Return missing value
#         return np.nan
 
# conti=get_continent(country_name.name)
# st.write(conti)

# #Geolocate the center of the country
# loc = geolocator.geocode(country_name.name)
# st.write(loc.latitude, loc.longitude)








