class persona:
    def __init__(self, nombre: str, edad:int):
        self.nombre = nombre
        self.edad = edad


    def Presentarse(self):
        print(f"Hola soy {self.nombre} y tengo {self.edad} anhos.")

class adoptante(persona):
  def __init__(self,nombre:str,edad:int):
    super().__init__(nombre,edad)
    self.mascotas_adoptadas=[]
  
  def adoptar(self,mascota:Mascota):
    if mascota.adoptado:
      return f"La mascota {mascota.nombre} ya fue adoptado"
    mascota.adoptado =True
    self.mascotas_adoptadas.append(mascota)
    return f"{self.nombre} ha adoptado a {mascota.nombre}."
    
  
    