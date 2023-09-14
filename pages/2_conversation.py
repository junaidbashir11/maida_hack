import streamlit as st
import pandas as pd
import openai
import json


openai.api_key=""
data = pd.read_csv("D:\\upskill\\maida2\\DatabaseLayer\\mockdb.csv")



st.set_page_config(page_title="chatbot", page_icon="")


st.sidebar.header("chatbot")
st.write(
    """This is the conversational agent !"""
)

user_input = st.text_input("Query  > ")




functions=[


{
  "name":"_get_the_annual_turnover",
  "description":"returns the annual turnover",
  "parameters": {
    "type": "object",
    "properties": {

        "startdate": {
          "type": "string"
        },

        "enddate":{
            "type":"string"
        }

      }
    },
    "required": ["startdate","enddate"]
  },


]


def _get_the_annual_turnover(start_date,end_date):
    try:
        data['transaction_date'] = pd.to_datetime(data['transaction_date'])
        filtered_data = data[(data['transaction_date'] >= start_date) & (data['transaction_date'] <= end_date)]
        total_deposits = filtered_data[filtered_data['description'] == 'Deposit']['amount'].sum()
        total_withdrawals = filtered_data[filtered_data['description'] == 'Withdrawal']['amount'].sum()
        annual_turnover = total_deposits - total_withdrawals
        return json.dumps({
                "result":annual_turnover
                 })
    except Exception as e:
         return json.dumps({
                "result":"Give me a moment"
                 })





available_functions={
    "_get_the_annual_turnover":_get_the_annual_turnover
}


def _bot_response():

    messages=[

    {"role":"system","content":"call the appropriate  function provided based on the query"},
    {"role":"user","content":user_input}

    ]


    response=openai.ChatCompletion.create(

        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto", 

        )

    responsemessage=response["choices"][0]["message"]


    if responsemessage.get("function_call"):
    #-----------------------------------------------------------------------------------
        function_name = responsemessage["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(responsemessage["function_call"]["arguments"])
        function_response = fuction_to_call(
            start_date=function_args.get("startdate"),
            end_date=function_args.get("enddate")
            )

        messages.append(responsemessage)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            )  
        st.write(second_response["choices"][0]["message"]["content"])


    else :
        st.write("wait for a moment")



if st.button("converse"):
    _bot_response()