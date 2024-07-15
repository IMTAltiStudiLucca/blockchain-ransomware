# CryptoQuery (temp name) 

CryptoQuery is a project that allows executing queries on blockchain data using a custom query language. It utilizes Lark for parsing the query grammar and NetworkX (TODO) for creating graphs of transactions and addresses.

## Project Structure

The project consists of the following main files:

- `interpreter.py`: Contains the `QueryInterpreter` class that implements the query interpreter.
- `main.py`: Main script that runs some test queries using `QueryInterpreter`.
- `blockchain_data_API.py`: Class that interacts with the Blockchain.info API to retrieve data about transactions and addresses.
- `grammar.lark`: Defines the grammar for the custom query language.

## Requirements

- Python 3.6 or higher
- Python libraries: `lark-parser`, `requests`, `networkx` (TODO)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/query-interpreter.git
    ```
2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Define your query following the grammar specified in `grammar.lark`.
2. Run the `main.py` script to execute the query:
    ```sh
    python main.py
    ```

## Query Examples

Some examples of queries you can run:

- Check if a transaction has a specific number of outputs:
    ```txt
    From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.num_outputs = 2
    ```

- Verify if an address has a certain total amount sent:
    ```txt
    From Address bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40 Check Address.total_sent > 10000
    ```

- Check if a transaction contains a certain address among the outputs:
    ```txt
    From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check HEX 1KeNiiR3BZT8GPqQ61ihmvwRMsCQtcXNYC in Transaction.out_addresses
    ```

## Contributions

Contributions are welcome! Feel free to open issues or pull requests.

## Citation

If you use CryptoQuery in your research, please cite the following paper:

[Supporting Criminal Investigations on the Blockchain: A Temporal Logic-based Approach](https://www.researchgate.net/publication/379927973_Supporting_Criminal_Investigations_on_the_Blockchain_A_Temporal_Logic-based_Approach)

```
@article{blanchini2022supporting,
title={Supporting Criminal Investigations on the Blockchain: A Temporal Logic-based Approach},
author={Blanchini, Marco and Cerreta, Michele and Di Monda, Davide and Fabbri, Matteo and Raciti, Mario and Ahmad, Hamza Sajjad and Costa, Gabriele},
year={2024}
}
```

## License

This project is released under the MIT license.
