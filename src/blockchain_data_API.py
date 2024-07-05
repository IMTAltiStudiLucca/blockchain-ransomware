import requests


class BlockchainDataAPI:
    def __init__(self, base_url="https://blockchain.info/"):
        """
        Initializes the BlockchainDataAPI with the base URL for blockchain data requests.
        
        Args:
            base_url: The base URL for blockchain data requests (default: "https://blockchain.info/").
        """
        self.base_url = base_url

    def get_block(self, block_hash):
        """
        Retrieves data for a block from the blockchain.

        Args:
            block_hash: The hash of the block to retrieve.

        Returns:
            A JSON representation of the block data, or None if the request fails.
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

        Args:
            addr_hash: The hash of the Bitcoin address to retrieve.

        Returns:
            A JSON representation of the address data, or None if the request fails.
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

        Args:
            tx_hash: The hash of the transaction to retrieve.

        Returns:
            A JSON representation of the transaction data, or None if the request fails.
        """
        url = f"{self.base_url}rawtx/{tx_hash}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data for transaction with hash {tx_hash}")
            return None