# Vigenère 37 - Cifrador Moderno con Alfabeto Extendido 🔐

Este es un codificador y decodificador basado en el **Cifrado de Vigenère**, adaptado específicamente para el idioma español y entornos modernos. A diferencia del algoritmo tradicional de 26 caracteres, este sistema utiliza un alfabeto extendido de **37 elementos**.

## 🚀 Características Principales

- **Alfabeto Extendido (37 caracteres):** Incluye la letra `Ñ` y los números del `0-9`.
- **Normalización Estricta:** - Convierte todo automáticamente a MAYÚSCULAS.
    - Elimina tildes (Á -> A, etc.).
    - Remueve espacios y caracteres especiales para máxima seguridad criptográfica.
- **Interfaz Moderna:** Desarrollada con `CustomTkinter` para un diseño oscuro, intuitivo y profesional.
- **Gestión Rápida:** Botones dedicados para Copiar, Pegar y Eliminar en cada campo.

## 🧮 Lógica del Algoritmo

El sistema asigna un índice numérico a cada carácter:
`A=0, B=1, ..., N=13, Ñ=14, O=15, ..., Z=26, 0=27, 1=28, ..., 9=36`

### Fórmulas Matemáticas
- **Cifrado:** $C_i = (M_i + K_i) \pmod{37}$
- **Descifrado:** $M_i = (C_i - K_i + 37) \pmod{37}$

*Donde $M$ es el mensaje y $K$ es la clave.*

