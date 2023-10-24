import streamlit as st
import math
import decimal
from decimal import Decimal


value1, value2 = "", ""
with st.form("Calculator"):
    num1 = st.text_area(label='First number', placeholder='Enter first number', value=value1)
    option = st.selectbox(label='Operation', options=['+', '-', '*', '/'])
    num2 = st.text_area(label='Second number', placeholder='Enter second number', value=value2)
    submitted = st.form_submit_button("Calculate")
    if submitted:
        try:
            num1 = Decimal(num1.replace(',', '.').replace(' ', ''))
            num2 = Decimal(num2.replace(',', '.').replace(' ', ''))
            six_digits = Decimal('0.000001')
            if option == '+':
                res = (num1 + num2).quantize(six_digits, rounding=decimal.ROUND_HALF_UP)
            if option == '-':
                res = (num1 - num2).quantize(six_digits, rounding=decimal.ROUND_HALF_UP)
            if option == '*':
                res = (num1 * num2).quantize(six_digits, rounding=decimal.ROUND_HALF_UP)
            if option == '/':
                if num2 == 0:
                    st.write('Mistake! Dividing by zero!')
                else:
                    res = (num1 / num2).quantize(six_digits, rounding=decimal.ROUND_HALF_UP)
            res = '{:,}'.format(res).replace(',', ' ')
            res = res.rstrip("0")
            if res[-1] == '.':
                res = res[:-1]
            st.write(f'Result: {res}'.replace(',', '.'))
        except:
            st.write('Invalid values')
