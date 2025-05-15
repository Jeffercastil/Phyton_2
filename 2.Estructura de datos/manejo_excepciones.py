try:
    # Ingresar un número entero
    edad = int(input("Ingrese su edad (número entero): "))
    print(f"Tienes {edad} años")
    
    # Ingresar un número decimal
    altura = float(input("Ingrese su altura en metros (ej. 1.75): "))
    print(f"Mides {altura} metros")
    
    # Dividir para demostrar excepción
    resultado = 100 / edad
    print(f"100 dividido entre tu edad es: {resultado:.2f}")

except ValueError:
    print("¡Error! Debes ingresar un número válido")
except ZeroDivisionError:
    print("¡Error! No se puede dividir entre cero")
except Exception as e:
    print(f"Ocurrió un error inesperado: {type(e).__name__}")