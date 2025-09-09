from .mascota import Mascotas

class refugio:
  def __init__(self):
    self.__Mascotas =[]
  
  def   registrar_mascotas(self,mascota:Mascotas):
    """"Agregar nueva mascota al refugio"""
    self.__Mascotas.append(mascota)
    
  def listar_disponibles(self):
    """Retorna lista de mascotas no adoptados """
    return [m  for m in self.__Mascotas if not m.adoptado]