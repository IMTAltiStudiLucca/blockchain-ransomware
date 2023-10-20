import pprint
import requests

tx = f"0ED06D5B56F6AD8501FD336F7C78C9B66763201B2F152424404AA8D12787D2B7"
res = requests.get(f"https://blockchain.info/rawtx/{tx}")
red_dict = res.json()

inputs = [i for i in red_dict.get("inputs")]
for i in inputs:
    satoshi = i.get("prev_out").get("value")
    btc = float(satoshi / 10**8)
    pprint.pprint(f"{btc}₿")


edges_count = len(red_dict.get("inputs")) == 1 and len(red_dict.get("out")) == 2


if all([edges_count]):
    print("Ok")
