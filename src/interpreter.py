from pprint import pprint
from lark import Lark, Transformer, Visitor, v_args

from blockchaininfo_API_PoC import StrategyChecker
import test_addr, test_tx 


@v_args(inline=True)
class QueryTransformer(Visitor):
    """
    Transformer class for querying and transforming data.

    Attributes:
    - HEX_ATTRIBUTES: List of lists representing HEX attributes for transactions and addresses.
    - INT_ATTRIBUTES: List of lists representing NUM attributes for transactions and addresses.
    - BOOL_ATTRIBUTES: List of lists representing BOOL attributes for transactions and addresses.
    - IP_ATTRIBUTES: List of lists representing IP attributes for transactions and addresses.
    - LIST_ATTRIBUTES: List of lists representing LIST attributes for transactions and addresses.
    """
    # First element-> Transaction attribute, second element -> Address attribute
    HEX_ATTRIBUTES = [['hash'], ['hash', 'address']] 
    NUM_ATTRIBUTES = [['ver', 'vin_sz', 'vout_sz', 'size', 'weight', 'fee', 'lock_time', 'tx_index',
                       'time', 'block_index', 'block_height', 'total_rec', 'total_sent', 
                       'num_inputs', 'num_outputs'],
                      ['n_tx', 'n_unredeemed', 'total_received', 'total_sent', 'final_balance']]
    BOOL_ATTRIBUTES = [['double_spend'], []]
    IP_ATTRIBUTES = [['relayed_by'], []]
    LIST_ATTRIBUTES = [['inputs', 'out'], ['txs']]
    
    
    def query(self, *args):
        """
        Query method to retrieve the second argument.

        Args:
        - args: Variable number of arguments.

        Returns:
        - The second argument.
        """
        return args[1]
        
    def property(self, var):
        """
        Property method to return the input variable unchanged.

        Args:
        - var: Input variable.

        Returns:
        - The input variable.
        """
        return var
    
    def node_transaction(self, var):
        """
        Node method for transactions.

        Args:
        - var: Input variable.

        Returns:
        - The hash of the transaction.
        """
        tx_hash = var.children[0].value
        # self.tx_data = StrategyChecker.api.get_transaction(tx_hash)
        self.tx_data = test_tx.txs[0]
        # self.tx_data = test_tx.colonial_pipeline_tx1
        
        # Add num inputs and output
        self.tx_data['num_inputs'] = len(self.tx_data.get('inputs'))
        self.tx_data['num_outputs'] = len(self.tx_data.get('out'))
        
        # TODO: return 0 BTC if len(inputs) and len(outs) is 0
        # Add total BTC received and sent to the tx
        self.tx_data['total_rec'] = sum(
            [i.get('prev_out').get('value') for i in self.tx_data.get('inputs')]
        ) / 1e8 
        self.tx_data['total_sent'] = sum(
            [o.get('value') for o in self.tx_data.get('out')]
        ) / 1e8 
        
        return self.tx_data['hash']
            
    def node_address(self, var):
        """
        Node method for addresses.

        Args:
        - var: Input variable.

        Returns:
        - The address hash.
        """
        addr_hash = var.children[0].value
        # self.addr_data = StrategyChecker.api.get_address(addr_hash)
        self.addr_data = test_addr.addresses[0]
        return self.addr_data['address']
        
    def transaction_prop(self, *args):
        """
        Transaction property checker.

        Args:
        - args: Variable number of arguments.

        Returns:
        - Result of the property checker.
        """
        return self._prop_checker(*args, is_tx=True)
        
    def address_prop(self, *args):
        """
        Address property checker.

        Args:
        - args: Variable number of arguments.

        Returns:
        - Result of the property checker.
        """
        return self._prop_checker(*args, is_tx=False)
        
    def transaction_expression(self, *args):
        """
        Transaction expression checker.

        Args:
        - args: Variable number of arguments.

        Returns:
        - Result of the expression checker.
        """
        return self._expression_checker(*args, is_tx=True)
    
    def address_expression(self, *args):
        """
        Address expression checker.

        Args:
        - args: Variable number of arguments.

        Returns:
        - Result of the expression checker.
        """
        return self._expression_checker(*args, is_tx=False)

    def transaction_atom(self, tree):
        """
        Transaction atom method.

        Args:
        - attribute: Attribute to check.

        Returns:
        - The input attribute if found in valid transaction attributes.

        Raises:
        - KeyError: If the attribute is not found in valid transaction attributes.
        """
        attribute = tree.children[0]
        
        if not any(attribute in attr_list for attr_list in [
            self.HEX_ATTRIBUTES[0], self.NUM_ATTRIBUTES[0], self.BOOL_ATTRIBUTES[0], 
            self.IP_ATTRIBUTES[0], self.LIST_ATTRIBUTES[0]]
        ):
            raise KeyError(f'{attribute} not found in valid transaction attributes')
        return attribute
    
    def address_atom(self, attribute):
        """
        Address atom method.

        Args:
        - attribute: Attribute to check.

        Returns:
        - The input attribute if found in valid address attributes.

        Raises:
        - KeyError: If the attribute is not found in valid address attributes.
        """
       
        if not any(attribute in attr_list for attr_list in [
            self.HEX_ATTRIBUTES[1], self.NUM_ATTRIBUTES[1], self.BOOL_ATTRIBUTES[1], 
            self.IP_ATTRIBUTES[1], self.LIST_ATTRIBUTES[1]]
        ):
            raise KeyError(f'{attribute} not found in valid address attributes')
        return attribute
    
    def _prop_checker(self, *args, is_tx):
        """
        Internal method for property checking.

        Args:
        - args: Variable number of arguments.
        - is_tx: Boolean indicating whether it's a transaction check.

        Returns:
        - Result of the property checker.
        """
        
        if len(args) == 1:
            """ print('end recursion', args)
            input() """
            return args[0]
        elif args[0] == '(' and args[2] == ')':
            """ print('()', args)
            input() """
            return self._prop_checker(args[1], is_tx=is_tx)
        elif args[1] == 'not':
            """ print('not', args)
            input() """
            return not self._prop_checker(args[1], is_tx=is_tx)
        elif args[1] == 'and':
            """ print('and', args)
            input() """
            return self._prop_checker(args[0], is_tx=is_tx) and self._prop_checker(args[2], is_tx=is_tx)
        elif args[0] == 'Maxaddr':
            return False
        elif args[0] == 'Gtrans':
 
            g_trans = []
            txs_to_check = int(args[1].value)
            
            for i in range(txs_to_check):
                print(f'LOOP {i}')
                max_addr_hash = self._find_highest_out_addr()
                # self.addr_data = StrategyChecker.api.get_address(max_addr_hash)
                self.addr_data = test_addr.addresses[i]
                max_tx_hash = self._find_highest_out_tx()
                # self.tx_data = StrategyChecker.api.get_transaction(max_tx_hash)
                self.tx_data = test_tx.txs[i+1]
                print(args[2])
                g_trans.append(self._prop_checker(args[2], is_tx=is_tx))
                """ print(g_trans)
                input() """
                
            return all(g_trans)
        
        elif args[0] == 'Faddr':
            return False   
        elif args[0] == 'Xtrans':
            return False 
        else:
            raise Exception      
    
    def _expression_checker(self, *args, is_tx):
        """
        Internal method for expression checking.

        Args:
        - args: Variable number of arguments.
        - is_tx: Boolean indicating whether it's a transaction check.

        Returns:
        - Result of the expression checker.
        """
        data = self.tx_data if is_tx else self.addr_data

        if args[0] == 'HEX':
            return args[1] in data[args[3]]

        operator = args[1]
        tx_atom = args[0]

        """ print(tx_atom)
        input() """
        
        expression = data[tx_atom]
        
        if operator == '=':
            right_value = args[3] if args[2] in ['HEX', 'IP'] else args[2]
            return str(expression) == right_value.value
        elif operator == '<':
            return expression < float(args[2].value)
        elif operator == '>':
            return expression > float(args[2].value)
        else:
            raise Exception
        
    def _find_highest_out_addr(self):
        """
        Find the address with the highest btc output from a txs
        """
        addrs = self.tx_data.get('out', [])
        max_addr = max(addrs, key=lambda addr: addr.get('value', 0), default=None)
        max_addr_hash = max_addr.get('addr') if max_addr else None
        return max_addr_hash
    
    def _find_highest_out_tx(self):
        """
        Find the output transaction with the highest btc amount
        """
        txs = self.addr_data.get('txs', [])
        max_tx = min(txs, key=lambda tx: tx.get('result', 0), default=None)
        max_tx_hash = max_tx.get('hash') if max_tx else None
        return max_tx_hash


with open("grammar.lark") as f:
    lark_parser = Lark(f, parser="lalr") # , transformer=QueryTransformer())

# Test queries
test_queries = [
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.num_outputs = 2",
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.size = 225",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Gtrans 3 Transaction.size = 225"
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check (Transaction.size > 230 and Transaction.size < 280) and (Transaction.size < 300)",
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.hash = HEX 1231231a0714f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f",
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.relayed_by = IP 0.0.0.0",
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.double_spend = False",
    # "From Address bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40 Check Address.address = HEX bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40",
    # "From Address bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40 Check (Xtrans Transaction.lock_time > 30) and (Faddr 5 Address.address = HEX 7a51a014)",
]


""" # after 8/5/2021 00:00:00 -> 1620432000
# Colonial Pipeline
test_queries = [
    "From Transaction 6a798026d44af27dbacd28ea21462808df8deca51794cec80c1b59e07ef924a2 Check Transaction.num_inputs = 2 and Transaction.total_rec > 170 and Transaction.time > 1620432000"
] """
    
for tq in test_queries:
    parsed_query = lark_parser.parse(tq)
    QueryTransformer().visit(parsed_query)
    print(f'Query result: {parsed_query}') # .pretty()
    # NOTE: To print the AST, we need to import "from lark import tree" and do this step without a transformer class.
    # tree.pydot__tree_to_png(lark_parser.parse(tq), f"query_{i}.png")