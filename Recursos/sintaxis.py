# Consideraciones Importantes y Sintaxis en Python

# Función con Bucle For y Condicional If-Else
def imprimir_numeros_pares_hasta_n(n):
    """
    Imprime todos los números pares desde 0 hasta el número n (incluido).
    """
    for i in range(n + 1):
        if i % 2 == 0:  # Verifica si el número es par
            print(i)
        else:
            print(f"{i} (Impar)")

# Uso de la Función
limite = 10
print(f"Números pares hasta {limite}:")
imprimir_numeros_pares_hasta_n(limite)

# Consideraciones Finales
"""
En esta función, el bucle for itera sobre los números desde 0 hasta n.
El condicional if-else verifica si un número es par o impar.
La indentación define los bloques de código dentro de la función.
"""