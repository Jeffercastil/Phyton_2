def obtener_notas():
    notas =[]
    pesos =[]
    Asignaturas=["Matematicas", "Ciencias","Sociales","Etica"]
    Pesos_asignaturas=[50,30,20,10]

    for i in range(len(Asignaturas)):
        while True:
            try:
                nota =float (int(input(f"Ingrese las asignaturas: {Asignaturas[i]} : [1-5]")))
                if nota < 1 or nota >5:
                    print("Nota fuera de rango, por favor ingrese una nota entre 1 a 5")
                else:
                    notas.append[nota]
                    pesos.append(Pesos_asignaturas[i])
                    break
            except ValueError:
                print("Entrada invalidada ingrese de nuevo")
    return notas, pesos


def calcular_promedio(notas,pesos):
    if len(notas) == 0 or len(pesos)== 0:
        return 0
    
    suma_ponderado(nota * peso for nota, peso in zip(notas,pesos))
    suma_pesos=sum(pesos)
    return suma_ponderado / sum_pesos

def estado(promedio):
    if promedio >= 4.0:
        return "Aprobado"
    else:
        return "Desaprobo"
    
print("Bienvenido al visualizador de notas")
notas_estudiante,promedio_estudiante =obtener_notas()
promedio_estudiante =calcular_promedio(notas_estudiante,promedio_estudiante)
situacion_academica = estado(promedio_estudiante)
print(f"Promedio: {promedio_estudiante:.2f} Estado {estado}")   



