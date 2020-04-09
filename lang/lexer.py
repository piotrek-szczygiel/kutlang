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
            # ("LBRACE", r"\{"),
            # ("RBRACE", r"\}"),
            # ("DEFINE_ASSIGN", r":="),
            # ("RETURNS_ARROW", r"->"),
            ("COMMA", r","),
            # ("COLON", r":"),
            ("SEMICOLON", r";"),
            # ("EQUAL", r"=="),
            # ("ASSIGN", r"="),
            # ("LOWER_EQUAL", r"<="),
            # ("GREATER_EQUAL", r">="),
            # ("LOWER", r"<"),
            # ("GREATER", r">"),
            ("ADD", r"\+"),
            ("SUB", r"-"),
            ("MUL", r"\*"),
            ("DIV", r"/"),
            ("POW", r"\^"),
            ("VALUE_FLOAT", r"\d+\.\d+|\d+\.|\.\d+"),
            ("VALUE_INT", r"\d+"),
            ("VALUE_STRING", r"\"(.*?)\""),
            # ("IF", r"if"),
            # ("ELSE", r"else"),
            # ("FN", r"fn"),
            # ("FOR", r"for"),
            # ("WHILE", r"while"),
            # ("RETURN", r"return"),
            ("INT", r"int"),
            ("FLOAT", r"float"),
            ("STRING", r"string"),
            ("CAST", r"cast"),
            ("PRINT", r"print"),
            # ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ]

        token_names = []

        for name, pattern in tokens:
            lg.add(name, pattern)
            token_names.append(name)

        return lg.build(), token_names
