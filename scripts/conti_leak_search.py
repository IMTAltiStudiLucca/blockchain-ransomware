import pandas as pd
import re
import json

CSV_FILE = 'conti_leak_21_22.csv'
CRYPTO_PATTERN = r"\b(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[ac-hj-np-z02-9]{8,87})\b"
# CRYPTO_PATTERN = r"\b\w{21,}\b"

traces = []

def match_pattern(row):
    addr = re.findall(CRYPTO_PATTERN, row['body_en'])
    if addr != []:
        trace = {
            'addr': addr, 
            'content': row['body_en'], 
            'ts': row['ts'],
            'sender': row['from'],
            'receiver': row['to'],
            'index': row.name
        }
        traces.append(trace)

df = pd.read_csv(CSV_FILE)
df.apply(match_pattern, axis=1)

with open('conti_leak_21_22_traces.json', 'w') as f_out:
    json.dump(traces, f_out, indent=4)
print(f'Found {len(traces)} possible addresses')

