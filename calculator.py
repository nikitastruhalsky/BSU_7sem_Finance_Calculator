import streamlit as st
from decimal import Decimal


value1, value2 = "", ""
with st.form("Calculator"):
    num1 = st.text_area(label='First number', placeholder='Enter first number', value=value1)
    option = st.selectbox(label='Operation', options=["+", "-"])
    num2 = st.text_area(label='Second number', placeholder='Enter second number', value=value2)
    submitted = st.form_submit_button("Calculate")
    if submitted:
        try:
            num1 = Decimal(num1.replace(',', '.').replace(' ', ''))
            num2 = Decimal(num2.replace(',', '.').replace(' ', ''))
            if option == '+':
                st.write(f'Result: {(num1 + num2):.20f}')
            elif option == '-':
                st.write(f'Result: {(num1 - num2):.20f}')
        except:
            st.write('Invalid values')