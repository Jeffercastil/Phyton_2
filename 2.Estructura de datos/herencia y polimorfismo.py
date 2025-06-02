class DataSet:
  def __init__(self,data):
    self.data = data
    self.tamanho = len(data)
    
  def media(self):
    return sum(self.data) / len(self.data)
  