class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    RESERVED = {
        "START", "END", "INTEGER", "DECIMAL",
        "READ", "PRINT"
    }

    SYMBOLS = {
        '{', '}', '(', ')', ';', ',', '.', '=', '+', '-', '*', '/'
    }

    def __init__(self, text):
        self.text = text
        self.i = 0
        self.length = len(text)

    def current_char(self):
        if self.i < self.length:
            return self.text[self.i]
        return None

    def advance(self):
        self.i += 1

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

# SPECIAL CHARS AUTOMATA
    def scan_identifier_or_reserved(self):
        c = self.current_char()
        if not c.isalpha():
            raise Exception(f"Error: Expected letter at position {self.i}")

        lexeme = c
        self.advance()

        while self.current_char() is not None and self.current_char().isalpha():
            lexeme += self.current_char()
            self.advance()

        if lexeme in self.RESERVED:
            return Token("RESERVED", lexeme)

        digits = ""
        state = 1

        while True:
            c = self.current_char()
            if c is None or not c.isdigit():
                break

            if state == 1:
                digits += c
                self.advance()
                state = 2
            elif state == 2:
                digits += c
                self.advance()
                state = 3
            elif state == 3:
                digits += c
                self.advance()
                state = 4
            else:
                raise Exception(f"Error: Identifier '{lexeme + digits}' exceeds max 3 digits")

        if len(digits) == 0:
            raise Exception(f"Error: Identifier '{lexeme}' needs at least 1 digit")

        return Token("IDENTIFIER", lexeme + digits)


# NUMBER AUTOMATAS
    def scan_number(self):
        digits = ""
        state = 0

        while True:
            c = self.current_char()
            if c is None or not c.isdigit():
                break

            if state <= 5:
                digits += c
                state += 1
                self.advance()
            else:
                raise Exception("Error: Integer length exceeds 6 digits")

        if len(digits) == 0:
            raise Exception("Error: Invalid number")

        if self.current_char() == '.':
            self.advance()

            frac = ""
            dstate = 1

            c = self.current_char()
            if c is None or not c.isdigit():
                raise Exception("Error: Invalid decimal, must have digits after '.'")

            while True:
                c = self.current_char()
                if c is None or not c.isdigit():
                    break

                if dstate == 1:
                    frac += c
                    self.advance()
                    dstate = 2
                elif dstate == 2:
                    frac += c
                    self.advance()
                    dstate = 3
                elif dstate == 3:
                    frac += c
                    self.advance()
                    dstate = 4
                else:
                    raise Exception("Error: Decimal part exceeds 3 digits")

            return Token("FLOAT", digits + "." + frac)

        return Token("INT", digits)

    def scan_symbol(self):
        c = self.current_char()
        if c in self.SYMBOLS:
            self.advance()
            return Token("SYMBOL", c)

        raise Exception(f"Unknown symbol '{c}'")

    def next_token(self):
        self.skip_whitespace()

        if self.current_char() is None:
            return Token("EOF", None)

        c = self.current_char()

        if c.isalpha():
            return self.scan_identifier_or_reserved()

        if c.isdigit():
            return self.scan_number()

        if c in self.SYMBOLS:
            return self.scan_symbol()

        raise Exception(f"Unknown character '{c}' at index {self.i}")

    def scan_all(self):
        tokens = []
        tok = self.next_token()

        while tok.type != "EOF":
            tokens.append(tok)
            tok = self.next_token()

        tokens.append(tok)
        return tokens
