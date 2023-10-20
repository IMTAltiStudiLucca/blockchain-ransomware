from pprint import pprint
import requests


class BlockchainDataAPI:
    @staticmethod
    def get_block(block_hash):
        url = f"https://blockchain.info/rawblock/{block_hash}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for block with hash {block_hash}")
            return None

    @staticmethod
    def get_address(addr_hash):
        url = f"https://blockchain.info/rawaddr/{addr_hash}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for block with hash {addr_hash}")
            return None

    @staticmethod
    def get_transaction(tx_hash):
        url = f"https://blockchain.info/rawtx/{tx_hash}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for transaction with hash {tx_hash}")
            return None


def main():
    api = BlockchainDataAPI()
    tx_hash = "0ed06d5b56f6ad8501fd336f7c78c9b66763201b2f152424404aa8d12787d2b7"
    tx_data = api.get_transaction(tx_hash)

    for i in tx_data.get("inputs"):
        input_data = i.get("prev_out")

        satoshi = input_data.get("value")
        btc = float(satoshi / 10**8)
        pprint(f"Input: {btc}₿")

        addr_hash = input_data.get("addr")
        addr_data = api.get_address(addr_hash)
        pprint(f'Input balance: {addr_data.get("final_balance")}₿')

    # PoC conditions
    has_one_I_and_two_O = (
        len(tx_data.get("inputs")) == 1 and len(tx_data.get("out")) == 2
    )
    out_value_threshold = 5 * 10**8  # 5 BTC
    is_one_O_higher = (
        tx_data.get("out")[0].get("value")
        > tx_data.get("out")[1].get("value") + out_value_threshold
    ) or (
        tx_data.get("out")[1].get("value")
        > tx_data.get("out")[0].get("value") + out_value_threshold
    )

    # Check if conditions are met
    if all([has_one_I_and_two_O, is_one_O_higher]):
        print("Conditions are met.")


if __name__ == "__main__":
    main()
