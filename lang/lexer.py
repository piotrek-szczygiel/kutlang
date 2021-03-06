import rply


class Lexer:
    def __init__(self):
        self.lexer, self.tokens = Lexer.create_lexer()

    def lex(self, input):
        return self.lexer.lex(input)

    @staticmethod
    def create_lexer():
        lg = rply.LexerGenerator()
        lg.ignore(r"\s+")

        tokens = [
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("LBRACE", r"\{"),
            ("RBRACE", r"\}"),
            ("EQ", r"=="),
            ("NE", r"!="),
            ("LE", r"<="),
            ("GE", r">="),
            ("LT", r"<"),
            ("GT", r">"),
            ("DEFINE", r":="),
            ("COMMA", r","),
            ("SC", r";"),
            ("COLON", r":"),
            ("ASSIGN", r"="),
            ("NOT", r"!"),
            ("AND", r"&&"),
            ("OR", r"\|\|"),
            ("ADD", r"\+"),
            ("SUB", r"-"),
            ("MUL", r"\*"),
            ("DIV", r"/"),
            ("POW", r"\^"),
            ("MOD", r"%"),
            ("VALUE_FLOAT", r"\d+\.\d+|\d+\.|\.\d+"),
            ("VALUE_INT", r"\d+"),
            ("VALUE_STR", r"\"(.*?)\""),
            ("TRUE", r"true"),
            ("FALSE", r"false"),
            ("IF", r"if"),
            ("ELSE", r"else"),
            ("FOR", r"for"),
            ("WHILE", r"while"),
            ("FN", r"fn"),
            # ("RETURN", r"return"),
            # ("BREAK", r"break"),
            ("INT", r"int"),
            ("FLOAT", r"float"),
            ("STR", r"str"),
            ("BOOL", r"bool"),
            ("CAST", r"cast"),
            ("PRINTLN", r"println"),
            ("PRINT", r"print"),
            ("SYMBOL", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ]

        token_names = []

        for name, pattern in tokens:
            lg.add(name, pattern)
            token_names.append(name)

        return lg.build(), token_names
