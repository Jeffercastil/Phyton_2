class mascota:
    def __init__(self, nombre, especie, edad, adoptado):
        self.nombre = nombre
        self.color = especie
        self.estado = edad
        self.adoptado = adoptado

    def __str__(self):
        return f"Nombre: {self.nombre}\nEspecie: {self.color}\nEdad: {self.estado}\nAdoptado: {self.adoptado}"
