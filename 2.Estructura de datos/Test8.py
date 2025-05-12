texto_guardados=[]

while true:
  print("\n--Menu---")
  print(" 1. Agregar texto")
  print(" 2. Mostrar todos los textos en orden")
  print(" Salir")
  
  opcion=input ("selecione una opcion (1-3")
  
  if(opcion == "1":
    nuevo_texto=input("\n Ingresar el texto que deseas guardar: ")
    texto_guardados.append(nuevo_texto)
    print(f"texto guardado correctamente".Total:{len(texto_guardados)})
    )
    elif opcion =="2":
      if not texto_guardados:
        print ("\n No hay textos guardados aun")
        else:
          print("\n Texto guardado")
          for i,texto in enumerate(texto_guardados,1):
            print(f"{i}.{texto}")
            
    elif opcion == "3":
      print("\n Saliendo del programa ")
      break
    else:
      print("\n Opcion no valida intenta otra vez")
        
  