class DataSet:
    def __init__(self, data):
        self.data = data
        self.tamanho = len(data)
    
    def media(self):
        return sum(self.data) / len(self.data)
  
class DataSetPlus(DataSet):
    def desviacion_estandar(self):
        nu = self.media()  # Corregido: usar self.media() en lugar de self(media)
        return (sum((x - nu) ** 2 for x in self.data) / self.tamanho) ** 0.5
    
    
datos = []
datosplus = []

ta = int(input("¿Cuántos valores desea ingresar en datos? "))

for i in range(ta):
    va = float(input(f"Ingresar valores de datos {i+1}: "))
    datos.append(va)
  
tb = int(input("¿Cuántos valores desea ingresar en dataplus? "))

for i in range(tb):
    vb = float(input(f"Ingresar valores de dataplus {i+1}: "))
    datosplus.append(vb)
  
print(f"Los valores de datos es: {datos}, Los valores de dataplus: {datosplus}")

# Crear instancias de las clases
dataset = DataSet(datos)
dataset_plus = DataSetPlus(datosplus)

# Llamar a los métodos
print("Media:", dataset.media())
print("Desviación estándar:", dataset_plus.desviacion_estandar())