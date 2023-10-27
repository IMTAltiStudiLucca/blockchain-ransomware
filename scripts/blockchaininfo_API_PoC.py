from pprint import pprint
import requests


class BlockchainDataAPI:
    def __init__(self, base_url="https://blockchain.info/"):
        """
        Initialises the BlockchainDataAPI with the base URL for blockchain data requests.
        :param base_url: The base URL for blockchain data requests (default: "https://blockchain.info/").
        """
        self.base_url = base_url

    def get_block(self, block_hash):
        """
        Retrieves data for a block from the blockchain.
        :param block_hash: The hash of the block to retrieve.
        :return: A JSON representation of the block data, or None if the request fails.
        """
        url = f"{self.base_url}rawblock/{block_hash}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for block with hash {block_hash}")
            return None

    def get_address(self, addr_hash):
        """
        Retrieves data for a Bitcoin address from the blockchain.
        :param addr_hash: The hash of the Bitcoin address to retrieve.
        :return: A JSON representation of the address data, or None if the request fails.
        """
        url = f"{self.base_url}rawaddr/{addr_hash}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for address with hash {addr_hash}")
            return None

    def get_transaction(self, tx_hash):
        """
        Retrieves data for a transaction from the blockchain.
        :param tx_hash: The hash of the transaction to retrieve.
        :return: A JSON representation of the transaction data, or None if the request fails.
        """
        url = f"{self.base_url}rawtx/{tx_hash}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for transaction with hash {tx_hash}")
            return None


class StrategyChecker:
    api = BlockchainDataAPI()
    
    MEAN_NORM_RATIO = 0.9821
    DEV_NORM_RATIO = 0.0356
    
    # TODO: patience mechanism

    @staticmethod
    def _has_tx_disposable_addresses(tx_data):
        """
        Checks whether the address associated with a transaction is disposable (final_balance == 0).
        :param tx_data: JSON representation of the transaction data.
        :return: True if the addresses are disposable, False otherwise.
        """
        if len(tx_data.get("inputs")) == 0 and len(tx_data.get("out")) == 0:
            return False
        
        inputs = [i.get("prev_out").get("addr") for i in tx_data.get("inputs")]
        outputs = [o.get("addr") for o in tx_data.get("out")]
       
        are_balances_zero = []
        for addr in inputs + outputs:
            addr_data = StrategyChecker.api.get_address(addr)
            are_balances_zero.append(addr_data.get("final_balance") == 0)
        
        return all(are_balances_zero)

    @staticmethod
    def _is_address_from_tax_haven(addr_hash):
        """
        Checks if an address is from a tax haven based on a list of known tax haven addresses.
        :param addr_hash: The hash of the Bitcoin address to check.
        :return: True if the address is from a tax haven, False otherwise.
        """
        # TODO: Can we find a list of known tax haven addresses?
        known_tax_haven_addresses = [
            "address1",
            "address2",
            "address3",
        ]  # Add known tax haven addresses

        return addr_hash in known_tax_haven_addresses

    @staticmethod
    def _has_tx_one_input_and_two_outputs(tx_data):
        """
        Checks if a transaction has one input and two outputs.
        :param tx_data: JSON representation of the transaction data.
        :return: True if the condition is met, False otherwise.
        """
        return len(tx_data.get("inputs")) == 1 and len(tx_data.get("out")) == 2

    @staticmethod
    def _has_tx_one_output_higher_than_other(tx_data, threshold=None):
        """
        Checks if a transaction has one output significantly higher than the other.
        :param tx_data: JSON representation of the transaction data.
        :param threshold: The threshold value for considering an output as significantly higher (default: None).
            If ``None``, ``DEV_NORM_RATIO`` is used.
        :return: True if the condition is met, False otherwise.
        """
        if len(tx_data.get("out")) < 2:
            return False
        
        threshold = threshold or StrategyChecker.DEV_NORM_RATIO # If threshold is None, use DEV_NORM_RATIO 
        out0, out1 = tx_data.get("out")[0].get("value"), tx_data.get("out")[1].get("value")
        norm_ratio = max(out0, out1) / (out0 + out1) # Normalized ratio between the 2 outputs
        z_score = (norm_ratio - StrategyChecker.MEAN_NORM_RATIO) / StrategyChecker.DEV_NORM_RATIO
        return z_score <= threshold

    @staticmethod
    def lazy_peel_chain_detection_strategy(tx_hash):
        """
        Implements the Lazy Peel Chain Detection Strategy to check if a transaction meets specific conditions.

        This strategy is typically employed immediately after the ransom collection, allowing the dilution of transactions
        over a longer period to avoid suspicion.

        :param tx_hash: The hash of the transaction to check.
        :return: True if all conditions are met, False otherwise.
        """
        tx_data = StrategyChecker.api.get_transaction(tx_hash)
        if StrategyChecker._has_tx_one_input_and_two_outputs(tx_data) is False:
            return False

        return all(
            [
                StrategyChecker._has_tx_one_output_higher_than_other(tx_data, threshold=0.4),
                StrategyChecker._has_tx_disposable_addresses(tx_data),
                # StrategyChecker._is_address_from_tax_haven(addr_hash),    # TODO: Uncomment this condition once it is implemented.
            ]
        )


def main():
    # For testing purposes
    tx_hash_evil = "0ed06d5b56f6ad8501fd336f7c78c9b66763201b2f152424404aa8d12787d2b7"
    tx_hash_good = "5386fab4856ce51b2005aba341aa3c267504d783d19f812ffb398b0041d26037"

    if StrategyChecker.lazy_peel_chain_detection_strategy(tx_hash_evil):
        print("Lazy Peel Chain Detection Strategy is met on tx_hash_evil. (EXPECTED)")
    else:
        print("Lazy Peel Chain Detection Strategy is NOT met on tx_hash_evil.")

    if StrategyChecker.lazy_peel_chain_detection_strategy(tx_hash_good):
        print("Lazy Peel Chain Detection Strategy is met on tx_hash_good.")
    else:
        print(
            "Lazy Peel Chain Detection Strategy is NOT met on tx_hash_good. (EXPECTED)"
        )


if __name__ == "__main__":
    main()
