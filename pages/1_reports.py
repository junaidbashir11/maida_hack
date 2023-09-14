import streamlit as st
import time
import pandas as pd
import os
import matplotlib.pyplot as plt
st.set_page_config(page_title="Automated Report generation", page_icon="")


st.sidebar.header("Automated Report generation")
st.write(
    """This is the Automated  report generation !"""
)

df = pd.read_csv('D:\\upskill\\maida2\\DatabaseLayer\\mockdb.csv')

output_directory = 'reports'
os.makedirs(output_directory, exist_ok=True)

selected_user = st.sidebar.selectbox("Select User:", df['user_id'].unique())

user_data = df[df['user_id'] == selected_user]

report_type = st.sidebar.selectbox("Select Report Type:", ["Full Report", "Transaction Summary"])



if report_type == "Full Report":
    st.write("Full Report:")
    st.dataframe(user_data)

elif report_type == "Transaction Summary":

    st.write("Transaction Summary Report:")
    #user_transaction_summary =pd.DataFrame({
        #"User ID":[selected_user],
        #"transactions":df[df['user_id'] == selected_user]['amount'].sum()
    #})
    user_data = df[df['user_id'] == selected_user]
    st.dataframe(user_data[['transaction_date', 'description', 'amount']])
    #st.dataframe(user_transaction_summary)
    
    if st.button("Generate Transaction Categories Pie Chart"):
        user_data = df[df['user_id'] == selected_user]
        transaction_categories = user_data['description'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(transaction_categories, labels=transaction_categories.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
        #Display the pie chart in Streamlit
        st.pyplot(fig)





    


