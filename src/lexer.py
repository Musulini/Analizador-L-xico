import re


class Token:
    def __init__(self, type_, lexeme, line, column):
        self.type = type_
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.type}('{self.lexeme}') at ({self.line},{self.column})"


class Lexer:
    KEYWORDS = {"START", "END", "INTEGER", "DECIMAL", "READ", "PRINT"}
    SYMBOLS = {"{", "}", "(", ")", ";", ",", ".", "=", "+", "-", "*", "/"}

    def __init__(self, text: str):
        self.text = text
        self.i = 0
        self.line = 1
        self.col = 1

        self.tokens = []
        self.symbol_table = {}
        self.errors = []

        # Precompile regex
        self.regex_decimal = re.compile(r"[0-9]{1,6}\.[0-9]{1,3}")
        self.regex_integer = re.compile(r"[0-9]{1,6}")
        self.regex_id = re.compile(r"[A-Za-z][0-9]{1,3}")
        self.regex_letters = re.compile(r"[A-Za-z]+")

    # ========================
    # UTILIDADES BÁSICAS
    # ========================

    def _current(self):
        if self.i >= len(self.text):
            return None
        return self.text[self.i]

    def _advance(self, steps=1):
        for _ in range(steps):
            if self.i >= len(self.text):
                return
            if self.text[self.i] == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.i += 1

    def _skip_whitespace(self):
        while self._current() is not None and self._current() in (" ", "\t", "\r", "\n"):
            self._advance()

    # ========================
    # ANALIZADOR PRINCIPAL
    # ========================

    def next_token(self):
        self._skip_whitespace()

        if self._current() is None:
            return Token("EOF", "", self.line, self.col)

        start_line = self.line
        start_col = self.col
        remaining = self.text[self.i:]

        current = self._current()

        # ========================
        # IDENTIFICADORES / KEYWORDS
        # ========================
        if re.match(r"[A-Za-z]",current):
            letters_match = self.regex_letters.match(remaining)
            lexeme = letters_match.group()

            # Palabra reservada exacta
            if lexeme in self.KEYWORDS:
                self._advance(len(lexeme))
                return Token("KEYWORD", lexeme, start_line, start_col)

            # Intentar identificador
            id_match = self.regex_id.match(remaining)
            if id_match:
                lexeme = id_match.group()

                # Validar que no continúe con más dígitos
                next_char = self.text[self.i + len(lexeme)] if self.i + len(lexeme) < len(self.text) else None
                if next_char and next_char.isdigit():
                    self.errors.append(f"Invalid identifier '{lexeme + next_char}' at {start_line},{start_col}")
                    self._advance(len(lexeme) + 1)
                    return self.next_token()

                self._advance(len(lexeme))

                if lexeme not in self.symbol_table:
                    self.symbol_table[lexeme] = None

                return Token("ID", lexeme, start_line, start_col)

            else:
                self.errors.append(f"Invalid identifier '{lexeme}' at {start_line},{start_col}")
                self._advance(len(lexeme))
                return self.next_token()

        # ========================
        # NÚMEROS
        # ========================
        if current.isdigit():

            # Intentar decimal primero
            decimal_match = self.regex_decimal.match(remaining)
            if decimal_match:
                lexeme = decimal_match.group()
                self._advance(len(lexeme))
                return Token("DECIMAL", lexeme, start_line, start_col)

            # Intentar entero
            integer_match = self.regex_integer.match(remaining)
            if integer_match:
                lexeme = integer_match.group()

                # Validar longitud real
                if len(lexeme) > 6:
                    self.errors.append(f"Integer too long '{lexeme}' at {start_line},{start_col}")

                self._advance(len(lexeme))
                return Token("INTEGER", lexeme, start_line, start_col)

            self.errors.append(f"Invalid number at {start_line},{start_col}")
            self._advance()
            return self.next_token()

        # ========================
        # SÍMBOLOS
        # ========================
        if current in self.SYMBOLS:
            self._advance()
            return Token("SYMBOL", current, start_line, start_col)

        # ========================
        # ERROR LÉXICO
        # ========================
        self.errors.append(f"Unknown symbol '{current}' at {start_line},{start_col}")
        self._advance()
        return self.next_token()

    # ========================
    # EJECUCIÓN COMPLETA
    # ========================

    def scan_all(self):
        while True:
            token = self.next_token()
            self.tokens.append(token)
            if token.type == "EOF":
                break
        return self.tokens, self.symbol_table, self.errors