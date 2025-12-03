# Analizador Léxico en Python con Flet

Este proyecto implementa un **analizador léxico** desarrollado en **Python**, utilizando **expresiones regulares** para el reconocimiento de patrones y **Flet** para la construcción de la interfaz gráfica.  
El sistema permite ingresar código fuente y genera automáticamente:

- Tabla de **tokens**
- Tabla de **símbolos**
- Visualización estructurada dentro de una **interfaz Flet**

---

## Características principales

- Analizador léxico implementado mediante **expresiones regulares**.
- Detección de:
  - Identificadores
  - Números
  - Operadores
  - Palabras reservadas
  - Delimitadores
  - Caracteres no válidos
- Generación dinámica de:
  - **Tabla de tokens**  
  - **Tabla de símbolos**
- Interfaz gráfica responsiva desarrollada con **Flet**.
- Arquitectura modular organizada dentro de la carpeta `src/`.

---

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.10 o superior  
- pip  
- Entorno virtual (recomendado)

Instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
