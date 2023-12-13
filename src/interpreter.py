from lark import Lark, Transformer, v_args

@v_args(inline=True)
class QueryTransformer(Transformer):
    pass

with open('grammar.lark') as f:
     lark_parser = Lark(f, parser="lalr", transformer=QueryTransformer())
     
query_str = 'From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.size > 100'
parsed_query = lark_parser.parse(query_str)
print(parsed_query.pretty())
