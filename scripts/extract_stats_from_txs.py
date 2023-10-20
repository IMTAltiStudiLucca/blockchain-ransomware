import json
import numpy as np

deltas = []

with open('lazy_peel_chain_txs.json') as f:
    lazy_peel_chain_txs = json.load(f)
    
for tx in lazy_peel_chain_txs:
    outs = tx['outs']
    if len(outs) != 2:
        raise Exception('TX must have 2 outs')
    
    deltas.append(abs(outs[0]['amount'] - outs[1]['amount'])/10**8)
    
deltas = np.array(deltas)
print(deltas.mean(), deltas.std())

print(deltas)