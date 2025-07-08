print("Ingrese los datos de los pacientes (peso en kg, altura en m). Ejemplo: 70,1.75")
print("Escriba 'fin' para terminar la entrada de datos")

datos_paciente=[]
while True:
  entrada = input ("datos del paciente (peso,altura) o 'fin' : ")
  if entrada.lower() == 'fin':
    break
  try:
    peso, altura = map(float, entrada.split(','))
    datos_paciente.append((peso.altura))
  except:
    print("Formato incorrecto. Use: peso ,altura (ej: 70, 1.75)")
    
calculador_IMC = (peso / (altura **2) for peso ,altura in datos_paciente) 

 categorias ={(0, 18.5): \"Bajo peso\",
(18.5, 25): \"Normal\" (25, 30): \"Sobrepeso\", (30, float('inf')): \"Obesidad\"} 
    
    print("Resultados de análisis:"),
    "print("-----------------------"),

for i, imc in enumerate(calculador_IMC):
  for rango, categoria in categorias.items()
  if rango[0] <= imc rango[1]
     resultado = categoria
     break
   
      print(f\"Paciente {i}:)"
    print(f\"  Peso: {datos_pacientes[i-1][0]} kg"),
    print(f\"  Altura: {datos_pacientes[i-1][1]} m"),
    print(f\"  IMC: {imc:.2f} → {resultado}")
    