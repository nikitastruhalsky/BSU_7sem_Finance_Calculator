import streamlit as st
import math
import decimal
from decimal import Decimal


def operation(n1: Decimal, n2: Decimal, op):
    if op == '+':
        return n1 + n2
    if op == '-':
        return n1 - n2
    if op == '*':
        return n1 * n2
    if op == '/':
        return n1 / n2
    return 0


def has_zero_division(numbers: list, operator_options: list) -> bool:
    check_list = [True for num, option in zip(numbers, ["filler"] + operator_options) if num == 0 and option == "/"]
    return len(check_list) > 0


def more_priority(op1: str, op2: str) -> bool:
    if op1 == '+' or op1 == "-":
        return True
    else:
        return False


def format_spaces(num: Decimal) -> str:
    return '{:,}'.format(num).replace(',', ' ')


def format_num(num: Decimal) -> str:
    num = format_spaces(num)
    num = num.rstrip("0")
    if num[-1] == '.':
        num = num[:-1]
    return num


DEFAULT_VALUE = 0
with st.form("Finance Calculator"):
    nums = []
    options = []
    for i in range(3):
        nums.append(st.text_area(label=f'Number {i + 1}', placeholder=f'Number {i + 1}', value=DEFAULT_VALUE))
        options.append(st.selectbox(label=f'Operation {i + 1}', options=["+", "-", "*", "/"]))
    i += 1
    nums.append(st.text_area(label=f'Number {i + 1}', placeholder=f'Number {i + 1}', value=DEFAULT_VALUE))
    round_options = {"Math": decimal.ROUND_HALF_UP,
                     "Accountant": decimal.ROUND_HALF_EVEN,
                     "Floor": decimal.ROUND_HALF_DOWN}
    selected_round_option = round_options[st.selectbox(label="Choose rounding type", options=round_options.keys())]
    submitted = st.form_submit_button("Calculate")
    if submitted:
        try:
            for x in nums:
                if "e" in x:
                    raise Exception
            check_nums = nums.copy()
            nums = [Decimal(x.replace(',', '.').replace(' ', '')) for x in nums]
            for str_num, num in zip(check_nums, nums):
                if str_num.count(" ") == 0:
                    continue
                if format_spaces(num) != str_num:
                    raise Exception
            if has_zero_division(nums, options):
                st.write("Mistake! Division by zero!")
            else:
                ten_digits = Decimal('0.0000000001')
                ans = operation(nums[1], nums[2], options[1]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                if more_priority(options[0], options[2]):
                    ans = operation(ans, nums[3], options[2]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                    ans = operation(nums[0], ans, options[0]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                else:
                    ans = operation(nums[0], ans, options[0]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                    ans = operation(ans, nums[3], options[2]).quantize(ten_digits, rounding=decimal.ROUND_HALF_UP)
                six_digits = Decimal('0.000001')
                integer_num = Decimal('1')
                full_res = ans.quantize(six_digits, rounding=decimal.ROUND_HALF_UP)
                full_res = format_num(full_res)
                rounded = ans.quantize(integer_num, rounding=selected_round_option)
                st.write(f'Answer: {full_res}'.replace(',', '.'))
                st.write(f'Rounded Answer: {rounded}'.replace(',', '.'))
        except:
            st.write('Invalid values')