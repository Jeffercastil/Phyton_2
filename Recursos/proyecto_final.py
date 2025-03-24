def obtener_notas():
    # Función para obtener las notas del usuario
    notas = []
    for i in range(3):
        nota = float(input(f"Ingrese la nota de la asignatura {i + 1}: "))
        notas.append(nota)
    return notas

def calcular_promedio(notas):
    # Función para calcular el promedio de las notas
    return sum(notas)/len(notas)

def determinar_situacion_academica(promedio):
    # Función para determinar la situación académica del estudiante
    if promedio >= 6:
        return "Aprobado"
    else:
        return "Reprobado"

print("Bienvenido a la Evaluación Estudiantil")
notas_estudiante = obtener_notas()
promedio_estudiante = calcular_promedio(notas_estudiante)
situacion_academica = determinar_situacion_academica(promedio_estudiante)

print(f"Tu promedio es {promedio_estudiante:.2f}. Estás {situacion_academica}.")