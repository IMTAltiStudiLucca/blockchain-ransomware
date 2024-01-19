from lark import Lark, Transformer, v_args
from blockchaininfo_API_PoC import StrategyChecker


@v_args(inline=True)
class QueryTransformer(Transformer):
    """
    Transformer class for querying and transforming data.

    Attributes:
    - HEX_ATTRIBUTES: List of lists representing HEX attributes for transactions and addresses.
    - INT_ATTRIBUTES: List of lists representing INT attributes for transactions and addresses.
    - BOOL_ATTRIBUTES: List of lists representing BOOL attributes for transactions and addresses.
    - IP_ATTRIBUTES: List of lists representing IP attributes for transactions and addresses.
    - LIST_ATTRIBUTES: List of lists representing LIST attributes for transactions and addresses.
    """
    # First element-> Transaction attribute, second element -> Address attribute
    HEX_ATTRIBUTES = [['hash'], ['hash', 'address']] 
    INT_ATTRIBUTES = [['ver', 'vin_sz', 'vout_sz', 'size', 'weight', 'fee', 'lock_time', 'tx_index',
                       'time', 'block_index', 'block_height'],
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
        self.tx_data = {'hash': '7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f', 'ver': 2, 'vin_sz': 1, 'vout_sz': 2, 'size': 225, 'weight': 573, 'fee': 2250, 'relayed_by': '0.0.0.0', 'lock_time': 755925, 'tx_index': 4494081061398666, 'double_spend': False, 'time': 1664289787, 'block_index': 755927, 'block_height': 755927, 'inputs': [{'sequence': 4294967293, 'witness': '0247304402205c60bbc5999064c598a9fddbd4405072c3c47e43e3c3e57eb9945904aac169ac02204d539422108b5256826fcd4fb5ebaa56dd18d702dc98f5eef4e7b4d18465fb6b0121036d40149dc2b06f6fc9cbf4665512f3bc732bb718899e9b09f05fb0ba50c8ac75', 'script': '', 'index': 0, 'prev_out': {'addr': 'bc1qyuunv9pz6f4qpgd0c0wmenu9zhr6u57yjf4afd', 'n': 0, 'script': '00142739361422d26a00a1afc3ddbccf8515c7ae53c4', 'spending_outpoints': [{'n': 0, 'tx_index': 4494081061398666}], 'spent': True, 'tx_index': 6467674833564937, 'type': 0, 'value': 5310674450}}], 'out': [{'type': 0, 'spent': True, 'value': 310657500, 'spending_outpoints': [{'tx_index': 4801429243623573, 'n': 1}], 'n': 0, 'tx_index': 4494081061398666, 'script': '76a914cc83c8f42aaf2e514f216d82957c7c20f2bac21488ac', 'addr': '1KeNiiR3BZT8GPqQ61ihmvwRMsCQtcXNYC'}, {'type': 0, 'spent': True, 'value': 5000014700, 'spending_outpoints': [{'tx_index': 5648945386042604, 'n': 0}], 'n': 1, 'tx_index': 4494081061398666, 'script': '00141f7658ae84086c56c867ed435b3d83ca1b9bcc58', 'addr': 'bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40'}]}
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
        self.addr_data = {'hash160': '1f7658ae84086c56c867ed435b3d83ca1b9bcc58', 'address': 'bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40', 'n_tx': 2, 'n_unredeemed': 0, 'total_received': 5000014700, 'total_sent': 5000014700, 'final_balance': 0, 'txs': [{'hash': '23528e9e9335fa05eee083ba326abe7058c3b489962707204162a7b9b87c8da0', 'ver': 2, 'vin_sz': 1, 'vout_sz': 2, 'size': 225, 'weight': 573, 'fee': 2160, 'relayed_by': '0.0.0.0', 'lock_time': 756230, 'tx_index': 5648945386042604, 'double_spend': False, 'time': 1664467538, 'block_index': 756231, 'block_height': 756231, 'inputs': [{'sequence': 4294967293, 'witness': '02473044022001d4631f303dc1707519dbff8bb007671597cbfc8a5c269aceb5c0a1554d3ab7022069ace0d440f44440814482def422007a3c41cac8bb733643dcf1dc250dc5efec01210245004d845d8fa423f72013e56d565e76732c5516fe8138ba923aca94a67f47bf', 'script': '', 'index': 0, 'prev_out': {'addr': 'bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40', 'n': 1, 'script': '00141f7658ae84086c56c867ed435b3d83ca1b9bcc58', 'spending_outpoints': [{'n': 0, 'tx_index': 5648945386042604}], 'spent': True, 'tx_index': 4494081061398666, 'type': 0, 'value': 5000014700}}], 'out': [{'type': 0, 'spent': True, 'value': 518065, 'spending_outpoints': [{'tx_index': 1477375041610559, 'n': 76}], 'n': 0, 'tx_index': 5648945386042604, 'script': '76a91445b82486d54c81d60b14e520a8ab07744d04e4b988ac', 'addr': '17MeDhGCZiYJxuwoZGsC1FYpbqG83TwHxR'}, {'type': 0, 'spent': True, 'value': 4999494475, 'spending_outpoints': [{'tx_index': 6810901915633533, 'n': 0}], 'n': 1, 'tx_index': 5648945386042604, 'script': '0014548625a5c866889e02edd952becd356311fb6159', 'addr': 'bc1q2jrztfwgv6yfuqhdm9ftanf4vvglkc2ectdsz6'}], 'result': -5000014700, 'balance': 0}, {'hash': '7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f', 'ver': 2, 'vin_sz': 1, 'vout_sz': 2, 'size': 225, 'weight': 573, 'fee': 2250, 'relayed_by': '0.0.0.0', 'lock_time': 755925, 'tx_index': 4494081061398666, 'double_spend': False, 'time': 1664289787, 'block_index': 755927, 'block_height': 755927, 'inputs': [{'sequence': 4294967293, 'witness': '0247304402205c60bbc5999064c598a9fddbd4405072c3c47e43e3c3e57eb9945904aac169ac02204d539422108b5256826fcd4fb5ebaa56dd18d702dc98f5eef4e7b4d18465fb6b0121036d40149dc2b06f6fc9cbf4665512f3bc732bb718899e9b09f05fb0ba50c8ac75', 'script': '', 'index': 0, 'prev_out': {'addr': 'bc1qyuunv9pz6f4qpgd0c0wmenu9zhr6u57yjf4afd', 'n': 0, 'script': '00142739361422d26a00a1afc3ddbccf8515c7ae53c4', 'spending_outpoints': [{'n': 0, 'tx_index': 4494081061398666}], 'spent': True, 'tx_index': 6467674833564937, 'type': 0, 'value': 5310674450}}], 'out': [{'type': 0, 'spent': True, 'value': 310657500, 'spending_outpoints': [{'tx_index': 4801429243623573, 'n': 1}], 'n': 0, 'tx_index': 4494081061398666, 'script': '76a914cc83c8f42aaf2e514f216d82957c7c20f2bac21488ac', 'addr': '1KeNiiR3BZT8GPqQ61ihmvwRMsCQtcXNYC'}, {'type': 0, 'spent': True, 'value': 5000014700, 'spending_outpoints': [{'tx_index': 5648945386042604, 'n': 0}], 'n': 1, 'tx_index': 4494081061398666, 'script': '00141f7658ae84086c56c867ed435b3d83ca1b9bcc58', 'addr': 'bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40'}], 'result': 5000014700, 'balance': 5000014700}]}
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

    def transaction_atom(self, attribute):
        """
        Transaction atom method.

        Args:
        - attribute: Attribute to check.

        Returns:
        - The input attribute if found in valid transaction attributes.

        Raises:
        - KeyError: If the attribute is not found in valid transaction attributes.
        """
        if not any(attribute in attr_list for attr_list in [
            self.HEX_ATTRIBUTES[0], self.INT_ATTRIBUTES[0], self.BOOL_ATTRIBUTES[0], 
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
            self.HEX_ATTRIBUTES[1], self.INT_ATTRIBUTES[1], self.BOOL_ATTRIBUTES[1], 
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
            return args[0]
        else: 
            # TODO
            return False
    
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
        if operator == '=':
            right_value = args[3] if args[2] in ['HEX', 'IP'] else args[2]
            return str(data[tx_atom]) == right_value.value
        elif operator == '<':
            return data[tx_atom] < float(args[2].value)
        elif operator == '>':
            return data[tx_atom] > float(args[2].value)
        else:
            raise Exception


with open("grammar.lark") as f:
    lark_parser = Lark(f, parser="lalr", transformer=QueryTransformer())

# Test queries
test_queries = [
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.size = 225",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.hash = HEX 1231231a0714f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.relayed_by = IP 0.0.0.0",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.double_spend = False",
    "From Address bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40 Check Address.address = HEX bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check (Transaction.size > 210) and (Transaction.size < 300)",
    "From Address bc1qram93t5yppk9djr8a4p4k0vregdehnzcvp9y40 Check (Xtrans Transaction.lock_time > 30) and (Faddr 5 Address.address = HEX 7a51a014)",
]
    
for tq in test_queries:
    parsed_query = lark_parser.parse(tq)
    print(f'Query result: {parsed_query}')
