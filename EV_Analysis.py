import pandas as pd
import numpy as np
import plotly.express as px
import datetime as dt
import streamlit as st


st.set_page_config(page_title='EV Analysis')
st.title("ELECTRIC VEHICLE ANALYSIS")
st.header("2017-2022")

# READ FILE WITH FUNCTION TO OMPTIMIZING COMPUTATION
@st.experimental_memo(ttl=60,max_entries=10)
@st.cache(suppress_st_warning=True)  # 👈 Added this

def read_masDat(): 
    return pd.read_csv("https://drive.google.com/uc?export=download&id=1FEodh3Mxo-tEG65rlQr9BNukNdvHJfEA",
                         sep=";")
evMasDat=read_masDat()

evMasDat=evMasDat.astype({"Date":"datetime64[ns]"})
evMasDat['Year']=evMasDat['Date'].dt.year
evMasDat['Month']=evMasDat['Date'].dt.month

# DESCRIBE
evDesc=evMasDat.describe()

# SIDEBAR SETUP
st.sidebar.title("CONTROL PAGE")
selectDashboard = st.sidebar.selectbox(
    "CHOOSE DASHBOARD :",
    ("DESCRIPTIVE ANALYTICS", "PREDICTIVE ANALYTICS","PROFILE"))

selectDate = st.sidebar.date_input(
     "CHOOSE DATA RANGE :",
     value=(dt.date(2017, 1, 31),dt.date(2022, 5, 31)))
st.sidebar.write("Select Date temporarely not running for a while..")

selectValue = st.sidebar.radio(
     "SELECT VALUE :",
     ('PHEV-EV TOTAL', 'EV-NON EV TOTAL'))

if selectValue == 'PHEV-EV TOTAL':
    stVal,endVal=0,2
else:
    stVal,endVal=2,4


# LIST SELECTION
listVPU=evMasDat['Vehicle Primary Use'].sort_values(ascending=True).unique().tolist()
listState=evMasDat['State'].sort_values(ascending=True).unique().tolist() ; listState.insert(0,"ALL")
listCountry=evMasDat['County'].sort_values(ascending=True).unique().tolist(); listCountry.insert(0,"ALL")

# DATA PREP
listValue=evMasDat[['Plug-In Hybrid Electric Vehicles (PHEVs)',
                   'Battery Electric Vehicles (BEVs)',
                   'Electric Vehicle (EV) Total',
                   'Non-Electric Vehicle Total',
                   'Total Vehicles']].columns.values.tolist()

# WIDGET
vpuSelection = st.multiselect('Vehicle Primary Use : ',
                              listVPU,
                              default=listVPU)

stateSelection = st.selectbox('State : ',
                              listState)

if stateSelection != "ALL":
    lsevMasDat=evMasDat[evMasDat['State']==stateSelection]
    listCountry=lsevMasDat['County'].sort_values(ascending=True).unique().tolist()
    countrySelection = st.selectbox('Country : ',
                                  listCountry)
else: 
    countrySelection = st.selectbox('Country : ',
                                  listCountry)

# FILTER DATAFRAME
if stateSelection == "ALL" and countrySelection == "ALL" :
    evMasDatFil=evMasDat[(evMasDat['Vehicle Primary Use'].isin(vpuSelection))]

elif stateSelection != "ALL" and countrySelection == "ALL" :    
    evMasDatFil=evMasDat[(evMasDat['Vehicle Primary Use'].isin(vpuSelection)) &
                     (evMasDat['State']==stateSelection)& (evMasDat['County'].notnull())]
    
elif stateSelection == "ALL" and countrySelection != "ALL" :
    evMasDatFil=evMasDat[(evMasDat['Vehicle Primary Use'].isin(vpuSelection)) &
                     (evMasDat['State'].notnull())& (evMasDat['County']==countrySelection)]

elif stateSelection != "ALL" and countrySelection != "ALL" :
    evMasDatFil=evMasDat[(evMasDat['Vehicle Primary Use'].isin(vpuSelection)) &
                     (evMasDat['State']==stateSelection)& (evMasDat['County']==countrySelection)]

    
    
gbVchTotal=evMasDatFil.groupby(['Year','Month'])[listValue].sum().reset_index()

#PLOTING TOTAL VEHICLE
vhcTotal=px.bar(gbVchTotal,x="Year",
               y=listValue[4],
               title="AMERICANS VEHICLE TRENDS 2017-2022",
               color="Month",
               height=500,
               text_auto=".3s")

# PLOTING TOTAL EV
vhcEVTotal=px.bar(gbVchTotal,x="Year",
               y=listValue[stVal:endVal],
               title="AMERICANS ELECTRIC VEHICLE TRENDS 2017-2022 - " + selectValue,
               height=500,
               barmode="group")

@st.cache(suppress_st_warning=True)
def stat_year(): 
    return evMasDat.groupby(['Year','State'])[listValue].sum().reset_index()
gbStateTotal=stat_year()

vhcStateYr=px.line(gbStateTotal,x="Year",
               y=listValue[0:3],
               title="AMREICANS ELECTRIC VEHICLE TRENDS BY STATE 2017-2022",
               height=500,
               color='State')

# SHOW VISUALIZATION
if selectDashboard ==  "DESCRIPTIVE ANALYTICS" :
    st.header("DESCRIPTIVE ANALYTICS PAGES")
    st.plotly_chart(vhcTotal)
    st.plotly_chart(vhcEVTotal)
    st.write("DETAILS ELECTRIC VEHICLE 2017-2022")
    st.dataframe(evMasDatFil)
    st.write("DESCRIBE ELECTRIC VEHICLE 2017-2022")
    st.dataframe(evDesc)
    st.plotly_chart(vhcStateYr)
elif selectDashboard ==  "PREDICTIVE ANALYTICS" :
    st.header("PREDICTIVE ANALYTICS PAGES - IN PROGRESS MODELING")
else:
    st.header("PROFILE PAGES")
    st.write("visit my github repository at : https://github.com/dickysepta")


# CLEAR EXPERIMENTAL MEMOS
st.experimental_memo.clear()
