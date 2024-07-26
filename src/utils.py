from lark import Token


def get_boolean(v):
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

def cast_for_eval(op_list):
        if all(not isinstance(op, Token) for op in op_list):
            # No op is a Token
            return op_list

        if type(op_list[0]) != type(op_list[1]):
            if isinstance(op_list[0], Token):
                op_list[0] = type(op_list[1])(op_list[0])
            else:
                # FIXME: Bug when casting Token to bool 
                op_list[1] = type(op_list[0])(op_list[1])
        return op_list
    
def print_node(descriptor, tree, eval_res):
    """
    Prints the tree node for debugging purposes.

    Args:
        descriptor: A descriptor for the current node.
        tree: The tree structure for the current query starting from the current node.
        eval_res: The evaluation result of the current node.
    """
    s = f'{descriptor} '
    for child in tree.children:
        if isinstance(child, Token):
            s += f'{child} '
        else:
            s += f'{child.children[0]} '
    print(f'{s}- returned: {eval_res}')
    