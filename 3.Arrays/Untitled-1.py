class libro:
    def __init__(self, titulo, autor, ano_publicacion):
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacion = ano_publicacion
        self.disponible = True
        

    def prestar (self):
        if self.disponible:
            self.disponible = False
            print("El libro ha sido prestado")
        else:
            print("El libro ya no está disponible")

    def devolver (self):
        if not self.disponible:
            self.disponible = True
            print("El libro ha sido devuelto")
        else:
            print("El libro ya no está disponible")

    def imprimir (self):
        print("Titulo: ", self.titulo)
        print("Autor: ", self.autor)
        print("Año de publicación: ", self.ano_publicacion)
        print("Disponible: ", self.disponible)

libro1 = libro("El libro de la vida", "Antonio Machado", 1984)