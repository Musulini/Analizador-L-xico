from dataclasses import dataclass

# ====== Token ======
@dataclass(frozen=True)
class Token:
    type: str
    lexeme: str
    line: int
    col: int

    def __str__(self):
        return f"Token({self.type}, '{self.lexeme}', line={self.line}, col={self.col})"


# ====== Lexer ======
class LexerError(Exception):
    pass


class Lexer:
    # Palabras reservadas del lenguaje :contentReference[oaicite:1]{index=1}
    KEYWORDS = {"START", "END", "INTEGER", "DECIMAL", "READ", "PRINT"}

    # Símbolos aceptados :contentReference[oaicite:2]{index=2}
    SYMBOLS = {"{", "}", "(", ")", ";", ",", ".", "=", "+", "-", "*", "/"}

    def __init__(self, text: str):
        self.text = text
        self.i = 0
        self.line = 1
        self.col = 1

    # ---------- Helpers de posición ----------
    def _current(self):
        if self.i >= len(self.text):
            return None
        return self.text[self.i]

    def _peek(self, k=1):
        j = self.i + k
        if j >= len(self.text):
            return None
        return self.text[j]

    def _advance(self):
        c = self._current()
        if c is None:
            return None

        self.i += 1
        if c == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return c

    def _skip_whitespace(self):
        while True:
            c = self._current()
            if c is None:
                return
            if c in (" ", "\t", "\r", "\n"):
                self._advance()
            else:
                return

    # ---------- Scanners ----------
    def _scan_keyword_or_id_or_error(self):
        """
        Reglas:
        - Palabras reservadas: solo letras (START, END, ...)
        - Identificador: 1 letra + 1 a 3 dígitos :contentReference[oaicite:3]{index=3}
        """
        start_line, start_col = self.line, self.col

        first = self._current()
        if first is None or not first.isalpha():
            raise LexerError("Interno: _scan_keyword_or_id_or_error llamado sin letra")

        # Tomamos la primera letra
        lex = self._advance()

        # Si vienen más letras -> puede ser keyword (ej. INTEGER)
        if self._current() is not None and self._current().isalpha():
            while self._current() is not None and self._current().isalpha():
                lex += self._advance()

            # Si coincide con keyword, perfecto
            if lex in self.KEYWORDS:
                return Token("KEYWORD", lex, start_line, start_col)

            # Si no coincide con keyword, es inválido (no existe ID con varias letras)
            raise LexerError(
                f"Palabra no reconocida '{lex}' en line={start_line}, col={start_col}. "
                f"Solo se aceptan keywords o identificadores de 1 letra + 1-3 dígitos."
            )

        # Si NO vienen letras, entonces debe ser identificador: necesita 1-3 dígitos
        if self._current() is None or not self._current().isdigit():
            raise LexerError(
                f"Identificador inválido en line={start_line}, col={start_col}: "
                f"después de la letra se esperaba al menos 1 dígito (ej: a1, B23)."
            )

        # Consumimos 1 a 3 dígitos
        digits = 0
        while self._current() is not None and self._current().isdigit():
            if digits >= 3:
                raise LexerError(
                    f"Identificador inválido '{lex + self._current()}' en line={start_line}, col={start_col}: "
                    f"máximo 3 dígitos después de la letra."
                )
            lex += self._advance()
            digits += 1

        # Si después aparece otra letra pegada, también es inválido
        if self._current() is not None and self._current().isalpha():
            raise LexerError(
                f"Identificador inválido '{lex + self._current()}' en line={start_line}, col={start_col}: "
                f"un ID no puede tener letras después de los dígitos."
            )

        return Token("ID", lex, start_line, start_col)

    def _scan_number(self):
        """
        Reglas:
        - Entero: 1 a 6 dígitos :contentReference[oaicite:4]{index=4}
        - Decimal: entero + '.' + 1 a 3 dígitos :contentReference[oaicite:5]{index=5}
        """
        start_line, start_col = self.line, self.col

        # Parte entera
        int_part = ""
        count = 0
        while self._current() is not None and self._current().isdigit():
            if count >= 6:
                raise LexerError(
                    f"Número entero demasiado largo en line={start_line}, col={start_col}: "
                    f"máximo 6 dígitos."
                )
            int_part += self._advance()
            count += 1

        # ¿Decimal?
        if self._current() == "." and (self._peek() is not None and self._peek().isdigit()):
            dot = self._advance()  # consume '.'
            frac = ""
            frac_count = 0

            while self._current() is not None and self._current().isdigit():
                if frac_count >= 3:
                    raise LexerError(
                        f"Decimal inválido en line={start_line}, col={start_col}: "
                        f"máximo 3 decimales."
                    )
                frac += self._advance()
                frac_count += 1

            if frac_count == 0:
                # En teoría no pasa por el peek, pero por seguridad:
                raise LexerError(
                    f"Decimal inválido en line={start_line}, col={start_col}: faltan decimales después del punto."
                )

            return Token("DECIMAL", int_part + dot + frac, start_line, start_col)

        # Si no es decimal, es entero
        return Token("INTEGER", int_part, start_line, start_col)

    # ---------- API ----------
    def next_token(self):
        self._skip_whitespace()
        c = self._current()

        if c is None:
            return Token("EOF", "", self.line, self.col)

        # Símbolos
        if c in self.SYMBOLS:
            start_line, start_col = self.line, self.col
            lex = self._advance()
            return Token("SYMBOL", lex, start_line, start_col)

        # Letras: keyword o ID (o error)
        if c.isalpha():
            return self._scan_keyword_or_id_or_error()

        # Dígitos: entero o decimal
        if c.isdigit():
            return self._scan_number()

        # Cualquier otra cosa es inválida
        raise LexerError(f"Carácter no válido '{c}' en line={self.line}, col={self.col}")

    def scan_all(self):
        tokens = []
        while True:
            t = self.next_token()
            tokens.append(t)
            if t.type == "EOF":
                break
        return tokens