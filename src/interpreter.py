import itertools
from pprint import pprint
from lark import Lark, Transformer, v_args, Token
from lark.visitors import Interpreter

from blockchaininfo_API_PoC import StrategyChecker
import test_addr, test_tx 


# TODO: Fix docString
# @v_args(inline=True)
class QueryTransformer(Interpreter):
    """
    Transformer class for querying and transforming data.

    Attributes:
    - HEX_ATTRIBUTES: List of lists representing HEX attributes for transactions and addresses.
    - INT_ATTRIBUTES: List of lists representing NUM attributes for transactions and addresses.
    - BOOL_ATTRIBUTES: List of lists representing BOOL attributes for transactions and addresses.
    - IP_ATTRIBUTES: List of lists representing IP attributes for transactions and addresses.
    - LIST_ATTRIBUTES: List of lists representing LIST attributes for transactions and addresses.
    """
    # TODO: log system for visited nodes
    # TODO: Not used anymore, remove 
    # First element-> Transaction attribute, second element -> Address attribute
    HEX_ATTRIBUTES = [['hash'], ['hash', 'address']] 
    NUM_ATTRIBUTES = [['ver', 'vin_sz', 'vout_sz', 'size', 'weight', 'fee', 'lock_time', 'tx_index',
                       'time', 'block_index', 'block_height', 'total_rec', 'total_sent', 
                       'num_inputs', 'num_outputs'],
                      ['n_tx', 'n_unredeemed', 'total_received', 'total_sent', 'final_balance']]
    BOOL_ATTRIBUTES = [['double_spend'], []]
    IP_ATTRIBUTES = [['relayed_by'], []]
    LIST_ATTRIBUTES = [['inputs', 'out'], ['txs']]
    
    
    def query(self, tree):
        """
        Query method to retrieve the second argument.

        Args:
        - args: Variable number of arguments.

        Returns:
        - The second argument.
        """
        return self.visit_children(tree)
        
    def property(self, tree):
        """
        Property method to return the input variable unchanged.

        Args:
        - var: Input variable.

        Returns:
        - The input variable.
        """
        return self.visit_children(tree)
    
    def node_transaction(self, tree):
        """
        Node method for transactions.

        Args:
        - var: Input variable.

        Returns:
        - The hash of the transaction.
        """
        tx_hash = tree.children[0].children[0].value
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
            
    def node_address(self, tree):
        """
        Node method for addresses.

        Args:
        - var: Input variable.

        Returns:
        - The address hash.
        """
        addr_hash = tree.children[0].children[0].value
        # self.addr_data = StrategyChecker.api.get_address(addr_hash)
        self.addr_data = test_addr.addresses[0]
        return self.addr_data['address']
        
    def transaction_prop(self, tree):
        """
        Transaction property checker.

        Args:
        - args: Variable number of arguments.

        Returns:
        - Result of the property checker.
        """
        return self._prop_checker(tree)
        
    def address_prop(self, tree):
        """
        Address property checker.

        Args:
        - args: Variable number of arguments.

        Returns:
        - Result of the property checker.
        """
        return self._prop_checker(tree)
        
    def transaction_expression(self, tree):
        """
        Transaction expression checker.

        Args:
        - args: Variable number of arguments.

        Returns:
        - Result of the expression checker.
        """
        self._print_node(tree)
        return self._expression_checker(tree)
    
    def address_expression(self, tree):
        """
        Address expression checker.

        Args:
        - args: Variable number of arguments.

        Returns:
        - Result of the expression checker.
        """
        return self._expression_checker(tree)
    
    def _prop_checker(self, tree):
        """
        Internal method for property checking.

        Args:
        - args: Variable number of arguments.
        - is_tx: Boolean indicating whether it's a transaction check.

        Returns:
        - Result of the property checker.
        """
        # print(tree)
        # TODO: add comment here
        if len(tree.children) == 1 and tree.children[0].data in ['transaction_expression', 'address_expression']:
            return self.visit_children(tree)
        
        elif tree.children[0] == '(' and tree.children[2] == ')':
            
            for i, child in enumerate(tree.children):
                if not isinstance(child, Token):
                    print(f'Visiting child-{i}')
                    return self._get_boolean(self.visit(child))
                            
        elif tree.children[1] == 'and':
            
            for i, child in enumerate(tree.children):
                if not isinstance(child, Token):
                    print(f'Visiting child-{i}')
                    eval_res = self._get_boolean(self.visit(child))
                    if eval_res == False:
                        return False
             
            return True     
          
        else:
            raise Exception
                
        """ elif tree.children[0] == '(' and tree.children[2] == ')':
            return self._prop_checker(tree.children[1])
        elif tree.children[1] == 'not':
            return not self._prop_checker(args[1]) """
    
    def _expression_checker(self, tree):
        """
        Internal method for expression checking.

        Args:
        - args: Variable number of arguments.
        - is_tx: Boolean indicating whether it's a transaction check.

        Returns:
        - Result of the expression checker.
        """
                
        expression = self.visit_children(tree)[0]

        operator = tree.children[1]
        
        if operator == '=':
            # TODO: add comment here
            right_value = tree.children[3] if tree.children[2] in ['HEX', 'IP'] else tree.children[2]
            return str(expression) == right_value.value
        elif operator == '<':
            return expression < float(tree.children[2].value)
        elif operator == '>':
            return expression > float(tree.children[2].value)
        else:
            raise Exception
        
    def transaction_atom(self, tree):        
        return self.tx_data[tree.children[0]]
    
    def address_atom(self, tree):
        return self.addr_data[tree.children[0]]
        
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

    def _get_boolean(self, v):
        bv = v[0] if isinstance(v, list) else v
        if not isinstance(bv, bool):
            raise ValueError(f'Returned value -{bv}- from child is not a boolean value')
        return bv
    
    def _print_node(self, tree):
        s = ''
        for child in tree.children:
            if isinstance(child, Token):
                s += f'{child} '
            else:
                s += f'{child.children[0]} '
        print(s)

with open("grammar.lark") as f:
    lark_parser = Lark(f, parser="lalr") # , transformer=QueryTransformer())

# Test queries
test_queries = [
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.num_outputs = 2",
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.size = 225",
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.size = 225 and Transaction.num_outputs = 2 and Transaction.time > 1664289786 and Transaction.lock_time = 755925",
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check (Transaction.size = 225 and (Transaction.time > 1664289786 and Transaction.num_outputs = 2))",
    # "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Gtrans 3 Transaction.size = 225"
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check (Transaction.size > 220 and Transaction.size < 280) and (Transaction.num_outputs = 2)",
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
    node, query_result = QueryTransformer().visit(parsed_query)
    # query_result = list(itertools.chain(*query_result))[0] #TODO: return only a boolean value
    print(f'Query result for node {node}:\n {query_result}') # .pretty()
    # NOTE: To print the AST, we need to import "from lark import tree" and do this step without a transformer class.
    # tree.pydot__tree_to_png(lark_parser.parse(tq), f"query_{i}.png")