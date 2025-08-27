class persona:
    def __init__(self, nombre, apellido, edad, sexo, telefono, email, direccion, ciudad, pais):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.sexo = sexo
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.ciudad = ciudad
        self.pais = pais

    def Presentarse(self):
        print(f"Nombre: {self.nombre}\nApellido: {self.apellido}\nEdad: {self.edad}\nSexo: {self.sexo}\nTelefono: {self.telefono}\nEmail: {self.email}\nDireccion: {self.direccion}\nCiudad: {self.ciudad}\nPais: {self.pais}")