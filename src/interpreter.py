from lark import Lark, Transformer, v_args


@v_args(inline=True)
class QueryTransformer(Transformer):
    pass


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
    print(parsed_query.pretty())
