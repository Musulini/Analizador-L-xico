# app.py
import flet as ft
from lexer import lex

def main(page: ft.Page):
    page.title = "Analizador Léxico"
    page.scroll = "auto"

    input_code = ft.TextField(label="Código", multiline=True, min_lines=30, expand=True)

    token_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Tipo de Token")),
            ft.DataColumn(ft.Text("Valor")),
        ],
        rows=[]
    )

    symbol_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Identificador")),
        ],
        rows=[]
    )

    def mostrar_resultados(tokens, symbols):
        # limpiar tablas
        token_table.rows.clear()
        symbol_table.rows.clear()

        # llenar tabla de tokens
        for ttype, tvalue in tokens:
            token_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(ttype)),
                        ft.DataCell(ft.Text(tvalue)),
                    ]
                )
            )

        # llenar tabla de símbolos
        for sym in symbols:
            symbol_table.rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(sym))]
                )
            )

        page.update()

    def analizar(e):
        try:
            tokens, symbols = lex(input_code.value)
            mostrar_resultados(tokens, symbols)

        except Exception as ex:
            token_table.rows.clear()
            symbol_table.rows.clear()
            token_table.rows.append(
                ft.DataRow(cells=[ft.DataCell(ft.Text(f"ERROR: {ex}")), ft.DataCell(ft.Text("---"))])
            )
            page.update()

    btn = ft.ElevatedButton("Analizar", on_click=analizar)

    page.add(
        input_code,
        btn,
        ft.Text("Tabla de Tokens", size=18, weight="bold"),
        token_table,
        ft.Text("Tabla de Símbolos", size=18, weight="bold"),
        symbol_table
    )


ft.app(target=main)
