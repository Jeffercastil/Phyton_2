# Solicitar cantidad de reseñas a analizar
n = int(input("¿Cuántas reseñas deseas analizar? "))
reseñas = []

# Ingresar cada reseña
for i in range(n):
    reseña = input(f"Ingresa la reseña {i+1}: ")
    reseñas.append(reseña)

# Definir palabras positivas (podría pedirse al usuario también)
palabras_positivas = {'excelente', 'buen', 'recomendado', 'satisfecho', 'genial'}
positivas = 0

for reseña in reseñas:
    if any(palabra in reseña.lower() for palabra in palabras_positivas):
        positivas += 1

print("\nAnálisis de sentimiento:")
print(f"Total reseñas: {len(reseñas)}")
print(f"Reseñas positivas: {positivas} ({positivas/len(reseñas):.1%})")