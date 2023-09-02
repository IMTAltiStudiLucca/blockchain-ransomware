from glob import glob
import json
import re

PATH = './Ransomchats'
CRYPTO_PATTERN = r"\b\w{21,}\b"

files = glob(f'{PATH}/**/*.json', recursive=True)

traces = []

for file in files:
    with open(file) as f_in:
        print(file)
        chat = json.load(f_in)
        messages = chat['messages']
        for msg in messages:
            addr = re.findall(CRYPTO_PATTERN, msg['content'])
            if addr != []:
                trace = {
                    'file': file,
                    'addr': addr, 
                    'content': msg['content'], 
                    'ts': msg['timestamp'],
                    'sender': msg['party']
                }
                traces.append(trace)

with open('ransomchats_traces.json', 'w') as f_out:
    json.dump(traces, f_out, indent=4)
print(f'Found {len(traces)} possible addresses')