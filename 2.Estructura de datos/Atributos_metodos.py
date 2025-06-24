Mis_datos =[]

valor=int(input("cuantos valores deseas agregar"))
for i in range (valor):
  va = int (input(f"ingresa los valores :{i+1}"))
  Mis_datos.append(va)
  
class DataSet:
  def __init__(self,data):
    self.data = data
  
  def media(self):
    return  sum (self.data) / len(self.data)
    
  def mediana(self):
    sorted_data = sorted(self.data)
    n = len(sorted_data)
    midpoint = n // 2
    if n % 2 == 0:
      return ( sorted_data [midpoint - 1 ]+ sorted_data[midpoint]) / 2
    else:
      return sorted_data[midpoint]
      
  def anadir_datos(self,nuevo_dato):
    self.data.append(nuevo_dato)
    
print(Mis_datos.media())
print(Mis_datos.mediana())
print(Mis_datos.data())
    
