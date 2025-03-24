#IMPORTANTE SIEMPRE DARLES ESPACIOS A LAS FORMULAS, FOR, WHILE debido a que si no se realiza ordenado bota error

def obtener_notas():
    notas=[]
    pesos =[]
    Asignaturas =["Matematicas", "Sociales","Biologia","Tecnologia", "Español","Ingles","Etica","Musica","Educacion"]
    Peso_asignaturas =[10,10,10,10,10,10,10,10,10,10]

#len() es una función muy útil para obtener el tamaño o la cantidad de elementos en un objeto iterable en Python.
#Este bucle for itera sobre un rango de números desde 0 hasta len(Asignaturas) - 1.
#len(Asignaturas) devuelve la cantidad de elementos en la lista Asignaturas.
#i toma valores desde 0 hasta len(Asignaturas) - 1, lo que permite acceder a cada elemento de la lista Asignaturas usando su índice."""

    for i in range (len(Asignaturas)):

#Este bucle while se ejecuta indefinidamente hasta que se encuentra una instrucción break.
#Se utiliza para asegurarse de que el usuario ingrese una nota válida antes de continuar."""

        while True:
#Inicia un bloque de código donde se intenta ejecutar una operación que podría generar un error.
#Si ocurre un error dentro del bloque try, se captura en el bloque except."""

            try:
#Solicita al usuario que ingrese una nota para la asignatura actual (Asignaturas[i]).
#input() recibe la entrada del usuario como una cadena de texto.
#float() convierte la entrada en un número decimal (flotante).
#Si el usuario ingresa algo que no es un número, se generará un error ValueError."""

                nota = float(input(f"Ingrese la nota de {Asignaturas[i]}: (1-5):"))

#Verifica si la nota ingresada está fuera del rango permitido (menor que 1 o mayor que 10).
#Si la nota está fuera de rango, se ejecuta el bloque de código dentro del if"""

                if nota <1 or nota >5:

#Muestra un mensaje al usuario indicando que la nota ingresada no es válida.
#El bucle while True continúa, solicitando nuevamente la nota."""

                    print("Nota fuera de rango, por favor ingrese una nota entre 1 a 5")

                else:
#Si la nota está dentro del rango válido (entre 1 y 10), se ejecuta este bloque.
#Agrega la nota válida a la lista notas.
#Agrega el peso correspondiente a la asignatura actual (Pesos_asignaturas[i]) a la lista pesos.
                    notas.append(nota)
                    pesos.append(Peso_asignaturas[i])
                    break
#Sale del bucle while True porque se ha ingresado una nota válida.
#El programa continúa con la siguiente asignatura en el bucle for.

            except ValueError:
#Captura el error ValueError, que ocurre si el usuario ingresa algo que no es un número (por ejemplo, texto).
                print("Entrada invalida. por favor, ingrese un número.")
#El bucle while True continúa, solicitando nuevamente la nota.
    return notas,pesos

def calcular_promedio_ponderado(notas,pesos):
    if len(notas)== 0 or len(pesos)==0:
#Verifica si alguna de las listas (notas o pesos) está vacía.
#len(notas) == 0 devuelve True si la lista notas no tiene elementos.
#len(pesos) == 0 devuelve True si la lista pesos no tiene elementos.
#Si alguna de las listas está vacía, la función retorna 0 para evitar errores. return 0
        return 0
    #Calcula la suma ponderada de las notas.
    suma_ponderada= sum(nota * peso for nota, peso in zip (notas,pesos))
#zip(notas, pesos) combina las dos listas (notas y pesos) en pares de elementos. Por ejemplo, si notas = [7, 8] y pesos = [50, 30], 
# zip(notas, pesos) genera los pares (7, 50) y (8, 30).
#nota * peso for nota, peso in zip(notas, pesos) es una expresión generadora que multiplica cada nota por su peso correspondiente.
#Calcula la suma total de los pesos.
    suma_pesos = sum(pesos)
#El promedio ponderado se obtiene dividiendo la suma ponderada (suma_ponderada) por la suma de los pesos (suma_pesos).
    return  suma_ponderada/ suma_pesos

def determinar_situacion_academica(promedio):
    if promedio >= 4.0:
        return "Aprobado"
    else:
        return "Reprobado"
    
"""notas = [7, 8, 9]
pesos = [50, 30, 20]

suma_ponderada = 7*50 + 8*30 + 9*20 = 350 + 240 + 180 = 770
suma_pesos = 50 + 30 + 20 = 100
promedio_ponderado = 770 / 100 = 7.7
Como 7.7 >= 6, la función retorna "Aprobado".
"""

print("Bienvenido a la entrega de notas")
notas_estudiante,pesos_estudiante=obtener_notas()
promedio_estudiante=calcular_promedio_ponderado(notas_estudiante,pesos_estudiante)
situacion_academica= determinar_situacion_academica(promedio_estudiante)
print(f"El promedio ponderado del estudiante es {promedio_estudiante:.2f}. Esta {situacion_academica}")