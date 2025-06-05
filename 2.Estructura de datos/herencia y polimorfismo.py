class DataSet:
  def __init__(self,data):
    self.data = data
    self.tamanho = len(data)
    
  def media(self):
    return sum(self.data) / len(self.data)
  
class DataSetPlus(DataSet):
  def desviacion_estandar(self):
    nu = self(media)
    return(sum (x - nu ) ** 2 for x in self.data) / self.tamanho ) ** 0.5
    
    
datos=[]
datosplus=[]

ta=int(input("cuantos valores desea ingresar en datos"))

for i in range(ta):
  va =float(input(f"Ingresar valores de datos :{i+1}"))
  datos.append(va)
  
tb=int(input("Cuantos valores desea ingresar en dataplus"))

for i in range(tb):
  vb=float(input(f"Ingresar valores de dataplus : {i+1}"))
  datosplus.append(vb)
  
print(f"los valores de datos  es: {datos} ,Los valores de dataplus:{datosplus}")
  