from lark import Lark, Transformer, v_args


@v_args(inline=True)
class QueryTransformer(Transformer):
    pass


with open("grammar.lark") as f:
    lark_parser = Lark(f, parser="lalr", transformer=QueryTransformer())

# Test queries
test_queries = [
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.hash = HEX 1231231a0714f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Transaction.size = 210",
    "From Address 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check Address.final_balance = 1000",
    "From Transaction 7a51a014f6bd3ccad3a403a99ad525f1aff310fbffe904bada56440d4abeba7f Check (Transaction.size > 210) and (Transaction.size < 300)",
]
for tq in test_queries:
    parsed_query = lark_parser.parse(tq)
    print(parsed_query.pretty())
