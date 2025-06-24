# Creamos una lista vacía llamada Mis_datos para almacenar los valores ingresados por el usuario
Mis_datos = []

# Solicitamos al usuario cuántos valores desea agregar y lo convertimos a entero
valor = int(input("¿Cuántos valores deseas agregar? "))

# Usamos un ciclo for para pedir cada valor y agregarlo a la lista
for i in range(valor):
    # Solicitamos cada valor individual y lo convertimos a entero
    # Usamos f-string para mostrar el número de valor que se está ingresando (i+1 porque empezamos desde 0)
    va = int(input(f"Ingresa el valor {i+1}: "))
    # Agregamos el valor a la lista Mis_datos
    Mis_datos.append(va)

# Definimos la clase DataSet para realizar operaciones estadísticas
class DataSet:
    def __init__(self, data):
        # Constructor de la clase que recibe una lista de datos
        self.data = data  # Almacena los datos como atributo de la instancia
  
    def media(self):
        # Método para calcular la media (promedio) de los datos
        return sum(self.data) / len(self.data)  # Suma todos los elementos y divide por la cantidad
    
    def mediana(self):
        # Método para calcular la mediana de los datos
        sorted_data = sorted(self.data)  # Ordenamos los datos primero
        n = len(sorted_data)  # Obtenemos la cantidad de elementos
        midpoint = n // 2  # Calculamos el punto medio (división entera)
        
        # Si la cantidad de elementos es par
        if n % 2 == 0:
            # La mediana es el promedio de los dos valores centrales
            return (sorted_data[midpoint - 1] + sorted_data[midpoint]) / 2
        else:
            # Si es impar, la mediana es el valor central
            return sorted_data[midpoint]
      
    def anadir_datos(self, nuevo_dato):
        # Método para añadir nuevos datos al conjunto
        self.data.append(nuevo_dato)

# CORRECCIÓN IMPORTANTE: 
# Primero debemos crear una instancia de DataSet con nuestros datos antes de usar sus métodos
dataset = DataSet(Mis_datos)

# Ahora podemos llamar a los métodos de la instancia creada
print("Media:", dataset.media())  # Imprimimos la media
print("Mediana:", dataset.mediana())  # Imprimimos la mediana
print("Datos:", dataset.data)  # Imprimimos todos los datos (sin paréntesis porque data es un atributo, no un método)