from abc import ABC, abstractmethod
from lark import Token

import utils
import test_tx


class Operator(ABC):
    
    @abstractmethod
    def eval(self):
        pass
    
    
class And(Operator):
    
    def eval(self, children, interpreter):
        for _, child in enumerate(children):
            if not isinstance(child, Token):
                eval_res = utils.get_boolean(interpreter.visit(child))
                # End the visit if one child returns False                   
                if eval_res == False:
                    return False
        return True  
    
    
class Not(Operator):
    
    def eval(self, children, interpreter):
        for _, child in enumerate(children):
            if not isinstance(child, Token):
                return not utils.get_boolean(interpreter.visit(child)) 
            
            
class Xtrans(Operator):
    
    def eval(self, children, interpreter):
        interpreter.tx_data = (
            interpreter.api.get_transaction(interpreter._find_highest_out_tx())
            if not interpreter.debug_mode else test_tx.txs[0]
        )
        for _, child in enumerate(children):
            if not isinstance(child, Token):
                return utils.get_boolean(interpreter.visit(child))
    
    
class Gtrans(Operator):
    
    def eval(self, children, interpreter):
        for gtrans_iter in range(0, int(children[1].value)):
            print('='*100)
            print(f'Gtrans iteration: {gtrans_iter}')
            print(f"Current tx: {interpreter.tx_data['hash']}")
            
            for _, child in enumerate(children):
                if not isinstance(child, Token):
                    eval_res = utils.get_boolean(interpreter.visit(child))
                    # If at least one tx is false, return False 
                    # otherwise move to the next tx
                    if eval_res == False:
                        return False
            
            interpreter._move_to_next_tx(gtrans_iter)   
        return True
    
    
class Ftrans(Operator):
    
    def eval(self, children, interpreter):
        for ftrans_iter in range(0, int(children[1].value)):
            print('='*100)
            print(f'Ftrans iteration: {ftrans_iter}')
            print(f"Current tx: {interpreter.tx_data['hash']}")
            
            for _, child in enumerate(children):
                if not isinstance(child, Token):
                    eval_res = utils.get_boolean(interpreter.visit(child))
                    # If at least one tx is true, return True 
                    # otherwise move to the next tx
                    if eval_res == True:
                        return True
            
            interpreter._move_to_next_tx(ftrans_iter)   
        return False
    
    
class Gaddr(Operator):
    
    def eval(self, children, interpreter):
        for gaddr_iter in range(0, int(children[1].value)):
            print('='*100)
            print(f'Gaddr iteration: {gaddr_iter}')
            print(f"Current addr: {interpreter.addr_data['address']}")
            
            for _, child in enumerate(children):
                if not isinstance(child, Token):
                    eval_res = utils.get_boolean(interpreter.visit(child))
                    # If at least one addr is false, return False 
                    # otherwise move to the next tx
                    if eval_res == False:
                        return False
            
            interpreter._move_to_next_addr(gaddr_iter)   
        return True
    
    
class Faddr(Operator):
    
    def eval(self, children, interpreter):
        for faddr_iter in range(0, int(children[1].value)):
            print('='*100)
            print(f'Faddr iteration: {faddr_iter}')
            print(f"Current addr: {interpreter.addr_data['address']}")
            
            for _, child in enumerate(children):
                if not isinstance(child, Token):
                    eval_res = utils.get_boolean(interpreter.visit(child))
                    # If at least one addr is true, return True 
                    # otherwise move to the next tx
                    if eval_res == True:
                        return True
            
            interpreter._move_to_next_addr(faddr_iter)   
        return False
