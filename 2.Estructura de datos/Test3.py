# Solicitar cantidad de clientes a registrar
n = int(input("¿Cuántos clientes deseas registrar? "))
clientes = []

# Ingresar datos de cada cliente
for i in range(n):
    print(f"\nIngresa datos del cliente {i+1}:")
    nombre = input("Nombre: ")
    compras = int(input("Número de compras: "))
    gasto_total = float(input("Gasto total: $"))
    
    clientes.append({
        "id": i+1,
        "nombre": nombre,
        "compras": compras,
        "gasto_total": gasto_total
    })

# Calcular gasto promedio por compra
print("\nResumen de clientes:")
for cliente in clientes:
    gasto_promedio = cliente['gasto_total'] / cliente['compras']
    print(f"{cliente['nombre']}: {cliente['compras']} compras, "
          f"Gasto total: ${cliente['gasto_total']:.2f}, "
          f"Promedio: ${gasto_promedio:.2f} por compra")