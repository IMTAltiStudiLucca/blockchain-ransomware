from lark import Token
from lark.visitors import Interpreter

from blockchaininfo_API_PoC import StrategyChecker
import test_addr, test_tx 


class QueryInterpreter(Interpreter):
    """
    Interpreter class for querying and transforming data.
    """
    # TODO: log system for visited nodes
    
    def query(self, tree):
        """
        Process a query node.

        Args:
            tree: The tree structure for the current query starting from the current node.
            
        Returns:
            Result of visiting the children of the query node.
        """
        return self.visit_children(tree)
        
    def property(self, tree):
        """
        Process a property node.

        Args:
            tree: The tree structure for the current query starting from the current node.
            
        Returns:
            Result of visiting the children of the property node.
        """
        return self.visit_children(tree)
    
    def node_transaction(self, tree):
        """
        Process a transaction node and gather transaction data.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            The hash of the transaction.
        """
        tx_hash = tree.children[0].children[0].value
        # self.tx_data = StrategyChecker.api.get_transaction(tx_hash)
        self.tx_data = test_tx.txs[0]
        # self.tx_data = test_tx.colonial_pipeline_tx1
        
        self._add_tx_properties()
        
        return self.tx_data['hash']
            
    def node_address(self, tree):
        """
        Process an address node and gather address data.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            The address hash.
        """
        addr_hash = tree.children[0].children[0].value
        # self.addr_data = StrategyChecker.api.get_address(addr_hash)
        self.addr_data = test_addr.addresses[0]
        return self.addr_data['address']
        
    def transaction_prop(self, tree):
        """
        Process a transaction property node.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            Result of property checking.
        """
        return self._prop_checker(tree)
        
    def address_prop(self, tree):
        """
        Process an address property node.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            Result of property checking.
        """
        return self._prop_checker(tree)
        
    def transaction_expression(self, tree):
        """
        Process a transaction expression node.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            Result of expression checking.
        """
        eval_res =  self._expression_checker(tree)
        self._print_node(tree, eval_res)
        return eval_res
    
    def address_expression(self, tree):
        """
        Process an address expression node.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            Result of expression checking.
        """
        eval_res =  self._expression_checker(tree)
        self._print_node(tree, eval_res)
        return eval_res
    
    def _prop_checker(self, tree):
        """
        Check properties based on the provided tree structure.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            Boolean result based on property evaluation.
        """
        # If there is only one child left return the output value of the child
        if len(tree.children) == 1 and tree.children[0].data in ['transaction_expression', 'address_expression']:
            return self.visit_children(tree)
        
        # If the structure is a parenthesized expression (e.g., (expression)), visit the child node.
        elif tree.children[0] == '(' and tree.children[2] == ')':
            
            for i, child in enumerate(tree.children):
                if not isinstance(child, Token):
                    return self._get_boolean(self.visit(child))
                
        # If the structure is a logical 'and' operation, evaluate each child.
        elif tree.children[1] == 'and':
            
            for _, child in enumerate(tree.children):
                if not isinstance(child, Token):
                    eval_res = self._get_boolean(self.visit(child))
                    # End the visit if one child returns False                   
                    if eval_res == False:
                        return False
            return True   
        
        # If the structure has a logical 'not' operation
        elif tree.children[0] == 'not':  
            
            for i, child in enumerate(tree.children):
                if not isinstance(child, Token):
                    return not self._get_boolean(self.visit(child))
                
        # Xtrans
        elif tree.children[0] == 'Xtrans':  
            max_tx_hash = self._find_highest_out_tx()
            # self.tx_data = StrategyChecker.api.get_transaction(max_tx_hash)
            self.tx_data = test_tx.txs[0]
            for _, child in enumerate(tree.children):
                if not isinstance(child, Token):
                    return self._get_boolean(self.visit(child))
             
        # Gtrans  
        elif tree.children[0] == 'Gtrans':  
            
            for gtrans_iter in range(0, int(tree.children[1].value)):
                print('='*100)
                print(f'Gtrans iteration: {gtrans_iter}')
                print(f"Current tx: {self.tx_data['hash']}")
                
                for _, child in enumerate(tree.children):
                    if not isinstance(child, Token):
                        eval_res = self._get_boolean(self.visit(child))
                        # If at least one is tx is false, return False 
                        # otherwise move to the next tx
                        if eval_res == False:
                            return False
                
                self._move_to_next_tx(gtrans_iter)   
            return True
        
        # Ftrans  
        elif tree.children[0] == 'Ftrans':  
            
            for ftrans_iter in range(0, int(tree.children[1].value)):
                print('='*100)
                print(f'Ftrans iteration: {ftrans_iter}')
                print(f"Current tx: {self.tx_data['hash']}")
                
                for _, child in enumerate(tree.children):
                    if not isinstance(child, Token):
                        eval_res = self._get_boolean(self.visit(child))
                        # If at least one is tx is true, return True 
                        # otherwise move to the next tx
                        if eval_res == True:
                            return True
                
                self._move_to_next_tx(ftrans_iter)   
            return False
         
        else:
            raise Exception

    def _expression_checker(self, tree):  
        """
        Check expressions based on the provided tree structure.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            Result of expression evaluation.
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
        """
        Process a transaction atom node.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            The value of the transaction relative to the field specified by tx atom
        """     
        return self.tx_data[tree.children[0]]
    
    def address_atom(self, tree):
        """
        Process an address atom node.

        Args:
            tree: The tree structure for the current query starting from the current node.

        Returns:
            The value of the address relative to the field specified by addr atom
        """
        return self.addr_data[tree.children[0]]
        
    def _find_highest_out_addr(self):
        """
        Find the address with the highest output value.

        Returns:
            The hash of the address with the highest output value.
        """
        addrs = self.tx_data.get('out', [])
        max_addr = max(addrs, key=lambda addr: addr.get('value', 0), default=None)
        max_addr_hash = max_addr.get('addr') if max_addr else None
        return max_addr_hash
    
    def _find_highest_out_tx(self):
        """
        Find the transaction with the highest output value.

        Returns:
            The hash of the transaction with the highest output value.
        """
        txs = self.addr_data.get('txs', [])
        max_tx = min(txs, key=lambda tx: tx.get('result', 0), default=None)
        max_tx_hash = max_tx.get('hash') if max_tx else None
        return max_tx_hash

    def _get_boolean(self, v):
        """
        Convert a value to a boolean.

        Args:
            tree: The tree structure for the current query starting from the current node.
            v: The value to convert.

        Returns:
            The boolean representation of the value.
        """
        bv = v[0] if isinstance(v, list) else v
        if not isinstance(bv, bool):
            raise ValueError(f'Returned value -{bv}- from child is not a boolean value')
        return bv
    
    def _move_to_next_tx(self, iter):
        # Move to next tx 
        max_addr_hash = self._find_highest_out_addr()
        # self.addr_data = StrategyChecker.api.get_address(max_addr_hash)
        self.addr_data = test_addr.addresses[iter]
        max_tx_hash = self._find_highest_out_tx()
        # self.tx_data = StrategyChecker.api.get_transaction(max_tx_hash)
        self.tx_data = test_tx.txs[iter+1]
        self._add_tx_properties()
        
    def _add_tx_properties(self):
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
        
    def _print_node(self, tree, eval_res):
        """
        Print the tree node for debugging purposes.

        Args:
            tree: The tree structure for the current query starting from the current node.
        """
        s = ''
        for child in tree.children:
            if isinstance(child, Token):
                s += f'{child} '
            else:
                s += f'{child.children[0]} '
        print(f'{s}- returned: {eval_res}')