#Project Description: 
# This python program generates unique access tokens for Flask services; including FlaskPrint and FlaskTV
#========================================================================================================#

import random
import string
import json
from datetime import date

def get_random_alphaNumeric_string(stringLength):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

def write_json(data, filename='access_token.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

def generate_json(no_tokens):
    for k in range(no_tokens):
        new_data = {
            'id': k,
            'tkn': get_random_alphaNumeric_string(4).upper(),
            'date': str(date.today().strftime("%b-%d-%Y"))
        }
        with open('access_token.json') as json_file: 
            data = json.load(json_file)
            j_data = data['tokens']
            j_data.append(new_data)

        write_json(data)

generate_json(100)
