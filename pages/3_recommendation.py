import streamlit as st
import time
import numpy as np
import pandas as pd
import openai
openai.api_key=""

st.set_page_config(page_title="Recommendation", page_icon="")


st.sidebar.header("Recommendation")
st.write(
    """This is the recommendation engine !"""
)

data = pd.read_csv('D:\\upskill\\maida2\\DatabaseLayer\\mockdb.csv')

total_deposits = data[data['description'] == 'Deposit']['amount'].sum()
total_withdrawals = data[data['description'] == 'Withdrawal']['amount'].sum()
net_cash_flow = total_deposits - total_withdrawals

def _recommendation():

    messages=[

        {"role":"system","content":"you are a advisor to a Bank"},
        {'role':"user","content":f"given the net cash flow  for a bank to be {net_cash_flow} , recommend  best scenario for optimization in KRA achievement"},

        ]


    response=openai.ChatCompletion.create(

        model="gpt-3.5-turbo-0613",
        messages=messages

        )

    responsemessage=response["choices"][0]["message"]["content"]
    st.write(responsemessage)



if st.button("view recommendations"):
    _recommendation()
