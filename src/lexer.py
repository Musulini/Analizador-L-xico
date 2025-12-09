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

    # ============================================================
    # IDENTIFIER / RESERVED DFA
    # ============================================================
    def scan_identifier_or_reserved(self):
        # Estado 0: debe iniciar con letra
        c = self.current_char()
        if not c.isalpha():
            raise Exception(f"Error: Expected letter at position {self.i}")

        lexeme = ""
        state = 0

        # Estado 0 → letras
        while True:
            c = self.current_char()
            if c is not None and c.isalpha():
                lexeme += c
                self.advance()
                state = 0  # sigue en letras
            else:
                break

        # Si es reservada → token
        if lexeme in self.RESERVED:
            return Token("RESERVED", lexeme)

        # DFA para 1 a 3 dígitos
        digits = ""
        state = 1  # estado inicial esperando primer dígito

        while True:
            c = self.current_char()
            if c is None or not c.isdigit():
                break

            if state == 1:  # primer dígito
                digits += c
                self.advance()
                state = 2
            elif state == 2:  # segundo dígito
                digits += c
                self.advance()
                state = 3
            elif state == 3:  # tercer dígito
                digits += c
                self.advance()
                state = 4
            else:
                raise Exception(f"Error: Identifier '{lexeme + digits}' exceeds max digits")

        # Debe tener al menos 1 dígito
        if digits == "":
            raise Exception(f"Error: Identifier '{lexeme}' must have 1-3 digits")

        return Token("IDENTIFIER", lexeme + digits)

    # ============================================================
    # NUMBER DFA (enteros y decimales)
    # ============================================================
    def scan_number(self):
        digits = ""
        state = 0  # estados S0..S6 (esto controla máximo 6 dígitos)

        # Entero: S0 → S1 → S2 → ... → S6
        while True:
            c = self.current_char()
            if c is None or not c.isdigit():
                break

            if state <= 5:  # S0..S5 aceptan un dígito más
                digits += c
                self.advance()
                state += 1
            else:
                raise Exception("Error: Integer exceeds 6 digits")

        if digits == "":
            raise Exception("Error: Invalid number")

        # DECIMAL DFA
        if self.current_char() == '.':
            self.advance()

            frac = ""
            dstate = 1  # 1er dígito decimal requerido

            c = self.current_char()
            if c is None or not c.isdigit():
                raise Exception("Error: decimal must have digits after '.'")

            # DFA: máximo 3 dígitos decimales
            while True:
                c = self.current_char()
                if c is None or not c.isdigit():
                    break

                if dstate == 1:  # primer decimal
                    frac += c
                    self.advance()
                    dstate = 2
                elif dstate == 2:  # segundo decimal
                    frac += c
                    self.advance()
                    dstate = 3
                elif dstate == 3:  # tercer decimal
                    frac += c
                    self.advance()
                    dstate = 4
                else:
                    raise Exception("Error: decimal exceeds 3 digits")

            return Token("FLOAT", digits + "." + frac)

        return Token("INT", digits)

    # ============================================================
    # SYMBOL DFA
    # ============================================================
    def scan_symbol(self):
        c = self.current_char()
        if c in self.SYMBOLS:
            self.advance()
            return Token("SYMBOL", c)

        raise Exception(f"Unknown symbol '{c}'")

    # ============================================================
    # DRIVER
    # ============================================================
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
