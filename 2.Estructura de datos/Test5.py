# Solicitar cantidad de registros de ventas
n = int(input("¿Cuántos registros de ventas deseas ingresar? "))
ventas_categorias = []

# Ingresar cada registro
for i in range(n):
    print(f"\nRegistro {i+1}:")
    categoria = input("Categoría (Electrónicos/Ropa/Alimentos/Otros): ").capitalize()
    monto = float(input("Monto de venta: $"))
    ventas_categorias.append([categoria, monto])

# Sumar ventas por categoría
total_por_categoria = {}

for categoria, monto in ventas_categorias:
    if categoria in total_por_categoria:
        total_por_categoria[categoria] += monto
    else:
        total_por_categoria[categoria] = monto

# Mostrar resultados
print("\nVentas totales por categoría:")
for categoria, total in total_por_categoria.items():
    print(f"{categoria}: ${total:.2f}")
 
