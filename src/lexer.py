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

    # ==========================================
    # Palabras reservadas o Identificadores
    # ==========================================
    def scan_identifier_or_reserved(self):
        c = self.current_char()

        if not c.isalpha():
            raise Exception(f"Error: Expected letter at position {self.i}")

        lexeme = c
        self.advance()

        # Primera bifurcación del autómata:
        # ¿si la siguiente es letra → palabra reservada?
        if self.current_char() is not None and self.current_char().isalpha():
            # entonces debe ser palabra reservada O error
            while self.current_char() is not None and self.current_char().isalpha():
                lexeme += self.current_char()
                self.advance()

            if lexeme in self.RESERVED:
                return Token("RESERVED", lexeme)

            raise Exception(f"Error: Invalid identifier '{lexeme}'. Only 1 letter allowed.")

        # Si no hay más letras, ahora deben venir dígitos
        digits = ""

        while (self.current_char() is not None
               and self.current_char().isdigit()
               and len(digits) < 3):
            digits += self.current_char()
            self.advance()

        if len(digits) == 0:
            raise Exception(f"Error: Identifier '{lexeme}' missing digits (1–3 required)")

        return Token("IDENTIFIER", lexeme + digits)

    # ==========================================
    # Números Enteros o Decimales
    # ==========================================
    def scan_number(self):
        digits = ""

        # Parte entera (máximo 6 dígitos)
        while (self.current_char() is not None
               and self.current_char().isdigit()
               and len(digits) < 6):
            digits += self.current_char()
            self.advance()

        # Si no recogió nada
        if len(digits) == 0:
            raise Exception("Error: Invalid number")

        # Si se pasaron de 6 dígitos
        if self.current_char() is not None and self.current_char().isdigit():
            raise Exception("Error: Integer length exceeds 6 digits")

        # Decimal
        if self.current_char() == '.':
            self.advance()
            frac = ""

            if not self.current_char() or not self.current_char().isdigit():
                raise Exception("Error: Invalid decimal, must have digits after '.'")

            while (self.current_char() is not None
                   and self.current_char().isdigit()
                   and len(frac) < 3):
                frac += self.current_char()
                self.advance()

            # demasiados decimales
            if self.current_char() is not None and self.current_char().isdigit():
                raise Exception("Error: Decimal part exceeds 3 digits")

            return Token("FLOAT", digits + "." + frac)

        return Token("INT", digits)

    # ==========================================
    # Símbolo
    # ==========================================
    def scan_symbol(self):
        c = self.current_char()
        if c in self.SYMBOLS:
            self.advance()
            return Token("SYMBOL", c)

        raise Exception(f"Unknown symbol '{c}'")

    # ==========================================
    # Siguiente token
    # ==========================================
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

    # ==========================================
    # Escanear todo
    # ==========================================
    def scan_all(self):
        tokens = []
        tok = self.next_token()

        while tok.type != "EOF":
            tokens.append(tok)
            tok = self.next_token()

        tokens.append(tok)
        return tokens
