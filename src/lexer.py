# lexer.py
import re

TOKEN_SPEC = [
    ("RESERVED",    r"\b(START|END|INTEGER|DECIMAL|READ|PRINT)\b"),
    ("DECIMAL_NUM", r"\b[0-9]{1,6}\.[0-9]{1,3}\b"),
    ("INTEGER_NUM", r"\b[0-9]{1,6}\b"),
    ("ID",          r"\b[A-Za-z][0-9]{1,4}\b"),

    ("LBRACE",      r"\{"),
    ("RBRACE",      r"\}"),
    ("LPAREN",      r"\("),
    ("RPAREN",      r"\)"),
    ("SEMICOLON",   r";"),
    ("COMMA",       r","),
    ("DOT",         r"\."),
    ("ASSIGN",      r"="),
    ("PLUS",        r"\+"),
    ("MINUS",       r"-"),
    ("MULT",        r"\*"),
    ("DIV",         r"/"),

    ("NEWLINE",     r"\n"),
    ("SKIP",        r"[ \t]+"),
    ("MISMATCH",    r"."),
]

TOK_REGEX = "|".join(f"(?P<{name}>{regex})" for name, regex in TOKEN_SPEC)


def lex(code):
    tokens = []
    symbols = set()  # tabla de símbolos (IDs únicos)

    for match in re.finditer(TOK_REGEX, code):
        kind = match.lastgroup
        value = match.group()

        if kind in ("SKIP", "NEWLINE"):
            continue
        if kind == "MISMATCH":
            raise SyntaxError(f"Token inválido: {value}")

        # guardar tokens
        tokens.append((kind, value))

        # agregar identificadores a la tabla de símbolos
        if kind == "ID":
            symbols.add(value)

    return tokens, sorted(list(symbols))
