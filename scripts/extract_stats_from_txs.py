import json
import numpy as np

deltas = []
ratios = []

with open('lazy_peel_chain_txs.json') as f:
    lazy_peel_chain_txs = json.load(f)
    
for tx in lazy_peel_chain_txs:
    outs = tx['outs']
    if len(outs) != 2:
        raise Exception('TX must have 2 outs')
    
    out0 = outs[0]['amount'] / 10**8
    out1 = outs[1]['amount'] / 10**8
    
    deltas.append(abs(out0 - out1)) 
    
    max_out = max(out0, out1)
    ratios.append(max_out/(out0 + out1))
    
deltas = np.array(deltas)
ratios = np.array(ratios)
print(deltas.mean(), deltas.std())
print(ratios.mean(), ratios.std())

print(ratios)