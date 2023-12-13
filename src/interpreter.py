from lark import Lark, Transformer, v_args

grammar = r"""
    ?start: Query
    
    Query : "From" Node "Check" Property

    Node : "Transaction" ID | "Address" ID

    ID : String

    Property : TransactionProp | AddressProp

    TransactionProp : TransactionExpression | "not" TransactionProp | TransactionProp "and" TransactionProp | "Maxaddr" AddressAtom AddressProp | "Gtrans" Int TransactionProp | "Ftrans" Int TransactionProp

    AddressProp : AddressExpression | "not" AddressProp | AddressProp "and" AddressProp| "Xtrans" TransactionProp | "Gaddr" Int AddressProp | "Faddr" Int AddressProp

    TransactionExpression :  TransactionAtom ">" TransactionAtom | TransactionAtom "=" TransactionAtom | TransactionAtom "<" TransactionAtom

    AddressExpression :  AddressAtom ">" AddressAtom | AddressAtom "=" AddressAtom | AddressAtom "<" AddressAtom

    TransactionAtom : "Transaction." TransactionAttribute | Constant

    AddressAtom : "Address." AddressAttribute | Constant

    TransactionAttribute : hash | ver | vin_sz | vout_sz | size | weight | fee | relayed_by | lock_time | tx_index | double_spend | time | block_index | block_height | inputs | out

    AddressAttribute : hash | address | n_tx | n_unredeemed | total_received | total_sent | final_balance | txs

    hash : String
    address : String
    n_tx : String
    n_unredeemed : String
    total_received : String
    total_sent : String
    final_balance : String
    txs : String

    ver : String
    vin_sz : String
    vout_sz : String
    size : String
    weight : String
    fee : String
    relayed_by : String
    lock_time : String
    tx_index : String
    double_spend : String
    time : String
    block_index : String
    block_height : String
    inputs : String
    out : String

    Int : INT
    String : ESCAPED_STRING
    %import common.INT
    %import common.ESCAPED_STRING
"""

@v_args(inline=True)
class QueryTransformer(Transformer):
    def query(self, args):
        return {'Query': args}

    # Implement similar methods for other rules if necessary

# Example usage:
lark_parser = Lark(grammar, parser='lalr', transformer=QueryTransformer())
query_str = 'From Address 1234 Check transactionProp { [ Xtrans Transaction.amount > 100$ ] }'
parsed_query = lark_parser.parse(query_str)
print(parsed_query)
