import streamlit as st
import decimal
from decimal import Decimal


def operation(n1: Decimal, n2: Decimal, op):
    if op == '+':
        return n1 + n2
    elif op == '-':
        return n1 - n2
    elif op == '*':
        return n1 * n2
    elif op == '/':
        return n1 / n2


st.header("Стругальский Никита Борисович, 4 курс, 4 группа, 2023")

terms_number = 4
with st.form("Finance Calculator"):
    nums = []
    options = []
    for i in range(terms_number):
        nums.append(st.text_area(label=f'Number {i + 1}', placeholder=f'Number {i + 1}', value=0))
        if i == terms_number - 1:
            continue
        options.append(st.selectbox(label=f'Operation {i + 1}', options=["+", "-", "*", "/"]))
    round_options = {"Math": decimal.ROUND_HALF_UP,
                     "Accountant": decimal.ROUND_HALF_EVEN,
                     "Floor": decimal.ROUND_FLOOR}
    selected_round_option = round_options[st.selectbox(label="Choose rounding type", options=round_options.keys())]
    submitted = st.form_submit_button("Calculate")
    if submitted:
        try:

            # Checking for 'e' or wrong spaces presence
            for num in nums:
                if 'e' in num:
                    raise Exception
                num = num.rstrip(' ')
                if ' ' in num:
                    splitted_num = num.split(' ')
                    if len(splitted_num[0]) > 3:
                        raise Exception
                    for i, num_part in enumerate(splitted_num[1:]):
                        if len(num_part) != 3 and '.' not in num_part and ',' not in num_part:
                            raise Exception
                        elif '.' in num_part and i != len(splitted_num) - 2 or ',' in num_part and i != len(splitted_num) - 2:
                             raise Exception
                        elif num_part[0] == ',' or num_part[0] == '.':
                            raise Exception

            nums = [Decimal(x.replace(',', '.').replace(' ', '')) for x in nums]
            zero_division = False
            for i, oper in enumerate(options):
                if oper == '/' and nums[i + 1] == 0:
                    zero_division = True
            if zero_division:
                st.write("Mistake! Division by zero!")
            else:
                ten_digits = Decimal('0.0000000001')
                temp = operation(nums[1], nums[2], options[1]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                if options[0] == '*' or options[0] == '/':
                    temp = operation(nums[0], temp, options[0]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                    temp = operation(temp, nums[3], options[2]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                else:
                    temp = operation(temp, nums[3], options[2]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                    temp = operation(nums[0], temp, options[0]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                six_digits = Decimal('0.000001')
                no_digits_after_comma = Decimal('1')
                full_res = temp.quantize(six_digits, rounding=decimal.ROUND_HALF_UP)

                # Checking for leading zeros presence
                leading_zeros_num = 0
                for i in str(full_res)[::-1]:
                    if i == '0':
                        leading_zeros_num += 1
                    else:
                        break
                if leading_zeros_num != 0:
                    full_res = str(full_res)[:-leading_zeros_num]
                if str(full_res)[-1] == '.':
                    full_res = full_res[:-1]

                rounded_res = temp.quantize(no_digits_after_comma, rounding=selected_round_option)
                st.write(f'Answer: {full_res}'.replace(',', '.'))
                st.write(f'Rounded Answer: {rounded_res}'.replace(',', '.'))
        except:
            st.write('Invalid values')