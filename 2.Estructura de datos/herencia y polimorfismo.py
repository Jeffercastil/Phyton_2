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
  