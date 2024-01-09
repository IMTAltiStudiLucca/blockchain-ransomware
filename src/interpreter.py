from lark import Lark, Transformer, v_args
from blockchaininfo_API_PoC import StrategyChecker


@v_args(inline=True)
class QueryTransformer(Transformer):
    # First element-> Transaction attribute, second element -> Address attribute
    HEX_ATTRIBUTES = [['hash'], ['hash', 'address']] 
    INT_ATTRIBUTES = [['ver', 'vin_sz', 'vout_sz', 'size', 'weight', 'fee', 'lock_time', 'tx_index',
                       'time', 'block_index', 'block_height'],
                      ['n_tx', 'n_unredeemed', 'total_received', 'total_sent', 'final_balance']]
    BOOL_ATTRIBUTES = [['double_spend'], []]
    IP_ATTRIBUTES = [['relayed_by'], []]
    LIST_ATTRIBUTES = [['inputs', 'out'], ['txs']]
    
    
    def node_transaction(self, var):
        tx_hash = var.children[0].value
        self.tx_data = StrategyChecker.api.get_transaction(tx_hash)
        
    def node_address(self, var):
        addr_hash = var.children[0].value
        self.addr_data = StrategyChecker.api.get_address(addr_hash)

    def transaction_expression(self, *args):
        print(args)
        input()

    def transaction_atom(self, attribute):
        if not any(attribute in attr_list for attr_list in [
            self.HEX_ATTRIBUTES[0], self.INT_ATTRIBUTES[0], self.BOOL_ATTRIBUTES[0], 
            self.IP_ATTRIBUTES[0], self.LIST_ATTRIBUTES[0]]
        ):
            raise KeyError(f'{attribute} not found in valid transaction attributes')
        return attribute
    
    def address_atom(self, attribute):
        if not any(attribute in attr_list for attr_list in [
            self.HEX_ATTRIBUTES[1], self.INT_ATTRIBUTES[1], self.BOOL_ATTRIBUTES[1], 
            self.IP_ATTRIBUTES[1], self.LIST_ATTRIBUTES[1]]
        ):
            raise KeyError(f'{attribute} not found in valid address attributes')
        return attribute


with open("grammar.lark") as f:
    lark_parser = Lark(f, parser="lalr", transformer=QueryTransformer())

# Test queries
test_queries = [
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.hash = HEX 1231231a0714f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.relayed_by = IP 192.168.1.1",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.double_spend = False",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.size = 210",
    "From Address 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Address.hash = HEX 32423ad",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check (Transaction.size > 210) and (Transaction.size < 300)",
    "From Address 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check (Xtrans Transaction.lock_time > 30) and (Faddr 5 Address.hash = HEX 7a51a014)",
]
for tq in test_queries:
    parsed_query = lark_parser.parse(tq)
    #print(parsed_query.pretty())
