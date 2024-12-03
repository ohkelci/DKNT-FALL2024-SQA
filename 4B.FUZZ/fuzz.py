'''
Author: Akond Rahman
'''
from main import giveTimeStamp, getCSVData, getAllPythonFilesinRepo, runFameML

import random
import numpy as np
import pandas as pd



def divide(v1, v2):
    v1 = float(v1)
    v2 = float(v2)
    if v2 != 0:
        return v1 / v2
    else:
        return "Division by zero error."


def fuzzMethod(method, *args):
    try:
        result = method(*args)
        print(f"Method: {method.__name__}, Input: {args} => Output: {result}")
    except Exception as e:
        print(f"Method: {method.__name__}, Input: {args} => Exception: {e}")

def simpleFuzzer():
    naughty_strings = [
        "",  
        "null",  
        "undefined",  
        "\n", 
        "\x00", 
        "🧙‍♂️",  
        "1E2",  
        "-1E2",  
        "NaN",  
        "Infinity",  
        "0xDEADBEEF",  
        "1,000",  
        "1.0.0", 
        "<script>alert('XSS')</script>",  
        "1234567890123456789012345678901234567890",  
        "😉", 
        "-0",  
        "0.0",  
        " ",  
        "\t",  
        "0/0",  
        "13/03/1992",  
        "?",  
        "!",  
        "\\",  
    ]

    
    for _ in range(10):
        val1 = random.choice(naughty_strings)
        val2 = random.choice(naughty_strings)
        fuzzMethod(divide, val1, val2)

    
    fuzzMethod(giveTimeStamp)

    
    dummy_dict = {"script1.py": "sample_script_path"}
    dummy_dir = random.choice(naughty_strings)
    fuzzMethod(getCSVData, dummy_dict, dummy_dir)

   
    dummy_path = random.choice(naughty_strings)
    fuzzMethod(getAllPythonFilesinRepo, dummy_path)

    
    dummy_inp_dir = random.choice(naughty_strings)
    dummy_csv = random.choice(naughty_strings)
    fuzzMethod(runFameML, dummy_inp_dir, dummy_csv)

if __name__ == '__main__':
    simpleFuzzer()
