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
    # For testing -> c996eaea0be0a848fa9c2587ae099a5b6822e239cc1c586bb289d166f8c0ecaa
    tx_hash = "0ed06d5b56f6ad8501fd336f7c78c9b66763201b2f152424404aa8d12787d2b7"
    tx_data = api.get_transaction(tx_hash)

    for i in tx_data.get("inputs"):
        input_data = i.get("prev_out")

        satoshi = input_data.get("value")
        btc = float(satoshi / 10**8)
        pprint(f"Input: {btc}₿")

    # PoC conditions

    # Transaction has one input and two outputs
    has_TX_one_I_and_two_O = (
        len(tx_data.get("inputs")) == 1 and len(tx_data.get("out")) == 2
    )

    # Normalized outputs similar to a 'train' value
    if len(tx_data.get("out")) >= 2:
        out0, out1 = tx_data.get("out")[0].get("value"), tx_data.get("out")[1].get("value")
        norm_delta = max(out0, out1) / (out0 + out1)
        z_score = (norm_delta - 0.9821) / 0.0356
    # Transaction with two outputs has one output greater than the other plus a threshold
    """ out_value_threshold = 5 * 10**8  # 5 BTC
    has_TX_one_O_higher = (
        (
            tx_data.get("out")[0].get("value")
            > tx_data.get("out")[1].get("value") + out_value_threshold
        ) or (
            tx_data.get("out")[1].get("value")
            > tx_data.get("out")[0].get("value") + out_value_threshold
        )
    ) if len(tx_data.get("out")) >= 2 else False """

    # Address is "disposable"
    # TODO: Refine condition.
    is_addr_disposable = (
        (
            api.get_address(tx_data.get("inputs")[0].get("prev_out").get("addr")).get(
                "final_balance"
            )
            == 0
        )
    ) if len(tx_data.get("out")) >= 1 else False

    # Check if conditions are met
    if all([has_TX_one_I_and_two_O, has_TX_one_O_higher, is_addr_disposable]):
        print("Conditions are met.")
    else:
        print("Conditions are not met.")


if __name__ == "__main__":
    main()