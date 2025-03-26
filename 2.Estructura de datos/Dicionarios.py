
  dicionario={}
  for i in range(5):
      palabra=input(f"ingrese palabra :{i+1}")
      dicionario[palabra]=len(palabra)
  print(f"Los valores ingresados son:{dicionario}")