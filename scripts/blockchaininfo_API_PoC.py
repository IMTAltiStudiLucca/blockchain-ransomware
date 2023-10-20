from pprint import pprint
import requests


def get_wallet(wallet_hash):
    url = f"https://blockchain.info/rawaddr/{wallet_hash}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for block with hash {wallet_hash}")
        return None
    
def get_transaction(tx_hash):
    url = f"https://blockchain.info/rawtx/{tx_hash}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for block with hash {block_hash}")
        return None


tx_hash = f"0ED06D5B56F6AD8501FD336F7C78C9B66763201B2F152424404AA8D12787D2B7"
tx_data = get_transaction(tx_hash)

for i in tx_data.get("inputs"):
    input_data = i.get("prev_out")
    
    satoshi = input_data.get("value")
    btc = float(satoshi / 10**8)
    pprint(f"Input: {btc}₿")
    
    wallet_hash = input_data.get("addr")
    wallet_data = get_wallet(wallet_hash)
    pprint(f'Input balance: {wallet_data.get("final_balance")}₿')


edges_count = len(tx_data.get("inputs")) == 1 and len(tx_data.get("out")) == 2

if all([edges_count]):
    print("Ok")