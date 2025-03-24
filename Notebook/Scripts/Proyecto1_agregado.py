def obtener_notas():
    notas = []
    pesos = []
    Asignaturas =["Matematicas", " Ciencias ", "Sociales" "Etica"]
    Pesos_asignaturas =[50, 30, 20, 10]

    for i in range(len(Asignaturas)):
        while True:
            try:
                nota = float(input(f"Introduce la nota de {Asignaturas[i]} (1-10):"))
                if nota <1 or nota >10:
                    print("Nota fuera de rango, intente de nuevo")
                else:
                    notas.append(nota)
                    pesos.append(Pesos_asignaturas[i])
                    break
            except ValueError:
                print("Entrada invalida. por favor, ingrese un número.")
    return notas, pesos
        
def calcular_promedio_ponderado(notas,pesos):
    if len(notas) == 0 or len (pesos) == 0:
        return 0
    suma_ponderada = sum(nota * peso for nota, peso in  zip(notas, pesos))
    suma_pesos=sum(pesos)
    return suma_ponderada / suma_pesos

def determinar_situacion_academica(promedio):
    if promedio >= 6:
        return "Aprobado"
    else:
        return "Desaprobado"

print("Bienvenido a la entrega de notas")
notas_estudiante, pesos_estudiante = obtener_notas()
promedio_estudiante = calcular_promedio_ponderado(notas_estudiante, pesos_estudiante)
situacion_academica = determinar_situacion_academica(promedio_estudiante)
print(f"Tu promedio ponderado es {promedio_estudiante:.2f} . Esta {situacion_academica}")