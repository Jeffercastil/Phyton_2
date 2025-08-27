
# Pequeño programa de análisis de datos en Python
import pandas as pd

print("Bienvenido al mini-análisis de datos en Python!")

# Ingresar datos manualmente
datos = []
while True:
    valor = input("Ingresa un número (o escribe 'fin' para terminar): ")
    if valor.lower() == 'fin':
        break
    try:
        datos.append(float(valor))
    except ValueError:
        print("Por favor, ingresa un número válido.")

if datos:
    df = pd.DataFrame(datos, columns=["Valores"])
    print("\nDatos ingresados:")
    print(df)
    print("\nEstadísticas básicas:")
    print(df.describe())
else:
    print("No se ingresaron datos.")
