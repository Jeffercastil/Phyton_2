from models.mascota import Mascotas
from models.persona import Personas
from models.refugio import refugio


refugio =refugio()
cantidad = int(input("¿Cuántas mascotas deseas registrar? "))
for i in range cantidad:
  print(f"Mascotas N{i+1}")
  nombre=input("Nombre:")
  especie=input("Especie:")
  edad=int(input("Edad: "))