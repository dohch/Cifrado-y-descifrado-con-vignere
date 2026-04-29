# 🛡️ Cifrador por Trasposición de Ruta Pro

Un software de criptografía clásica desarrollado en Python que implementa el **Algoritmo de Trasposición por Ruta**. El programa permite transformar mensajes legibles en criptogramas complejos mediante la reordenación geométrica de sus caracteres.

## 📖 Sobre el Proyecto

Este proyecto no es solo un procesador de texto; es una implementación fiel de la **Trasposición Geométrica**. A diferencia de los cifrados de sustitución, este sistema mantiene la identidad de los caracteres pero altera su posición basándose en una matriz bidimensional y un patrón de lectura específico.

### 🧠 Bases Teóricas
El cifrado se fundamenta en la **difusión**. Al escribir el mensaje en filas y extraerlo mediante rutas complejas (como espirales o diagonales), se rompe la relación de vecindad entre las letras, dificultando el criptoanálisis estadístico.

## 🚀 Características y Reglas de Cifrado

El software aplica estrictamente las siguientes reglas de normalización antes de procesar cualquier mensaje:

* **Todo a Mayúsculas:** Estandarización para evitar pistas gramaticales.
* **Limpieza de Símbolos:** Se eliminan espacios, puntos, comas y signos de exclamación.
* **Gestión de Tildes:** Se eliminan las tildes (Á -> A), pero se **conserva la Ñ** como carácter único.
* **Preservación de Números:** Los dígitos del 0 al 9 se mantienen y ocupan su lugar en la matriz.
* **Padding (Relleno):** Uso del carácter **'X'** para completar matrices imperfectas.

## 🛠️ Rutas de Lectura Disponibles

El sistema cuenta con **8 modos de trasposición**:

1.  **Columnas (Abajo):** Lectura vertical estándar.
2.  **Columnas (Arriba):** Lectura vertical invertida.
3.  **Filas (Izq-Der):** Lectura lineal (sin trasposición real).
4.  **Filas (Der-Izq):** Lectura horizontal invertida.
5.  **Zigzag / Serpentina:** Cambio de dirección en cada fila (estilo Boustrophedon).
6.  **Espiral (Horario):** Recorrido concéntrico hacia el centro.
7.  **Espiral (Anti-horario):** Recorrido concéntrico inverso.
8.  **Diagonal:** Lectura transversal de la matriz.


