import os
import time

# *Seccion de funciones de operaciones basicas
def suma(a ,b):
  return a + b

def resta(a, b):
  return a - b

def multiplicacion(a, b):
  return a * b

def division(a, b):
  return a / b

def residuo(a, b):
  return a % b

# *Funcion para buscar el id dentro de la lista de procesos
def buscarId(id):
  for proceso in auxLote:
    if proceso["id"] == id:
      return True
  return False

# *Lista para guardar los procesos agregados, esta lista guarda cada lote de procesos, la otra guarda los procesos de dicho lote
procesos = []
auxLote = []
tiempoMax = 0

numProcesos = 0

while(True):
  try:
    numProcesos = int(input("Ingrese el numero de procesos a realizar: "))
    if numProcesos < 0:
      print("Ingrese un numero mayor a 0")
      input()
      os.system("cls")
      continue
    break
  except ValueError:
    print("Ingrese un numero valido")
    input()
    os.system("cls")
    continue

# *Se obtiene el numero de lotes a realizar
numLotes = numProcesos // 4

for i in range(0, numProcesos):
  
  # *Comprueba con multiplos de 4 para agregar a la lista de procesos cada lote
  if i % 4 == 0 and i != 0:
    procesos.append(auxLote)
    auxLote = []
  
  # *En caso de que no se llegue ni a un lote o no se termine uno, guarda en automatico el ultimo lote que se estaba creando
  if i == numProcesos - 1:
    procesos.append(auxLote)
    auxLote = []

  os.system("cls")
  nombre = input("Ingrese un nombre: ")

  while(True):
    idUser = input("Ingrese un ID: ")
    # *Verifica que el ID no este en la lista
    if procesos:
      if buscarId(idUser):
        print("El ID ya existe")
        input()
        os.system("cls")
        continue
    break

  while(True):
    try:
      fNum, sNum = map(int, input("Ingrese dos numeros separados por un espacio: ").split())
      break
    except ValueError:
      print("Ingrese dos numeros validos separados por un espacio")
      input()
      os.system("cls")
      continue

  # *Bucle en caso de que una operacion sea invalida con los numeros ingresados
  while(True):
    try:
      operacion = int(input("1.- +\n2.- -\n3.- *\n4.- / \n5.- %\nIngrese la operacion a realizar: "))
      if operacion <= 0 or operacion > 5:
        print("Ingrese una opcion valida")
        # *Regresa al inicio del bucle
        input()
        os.system("cls")
        continue

      if (operacion == 4 or operacion == 5) and sNum == 0:
        print("Operacion invalida para los numeros ingresados")
        input()
        os.system("cls")
        continue
      break
    except ValueError:
      print("Ingrese una opcion valida")
      input()
      os.system("cls")
      continue

  while(True):
    try:
      tiempo = int(input("Ingrese el tiempo de ejecucion en segundos: "))
      if tiempo < 0:
        print("El tiempo debe ser mayor a 0")
        input()
        os.system("cls")
        continue
      tiempoMax += tiempo
      break
    except ValueError:
      print("Ingrese un numero valido")
      input()
      os.system("cls")
      continue

  # *Guarda todo en un diccionario y lo agrega a la lista de procesos
  auxLote.append({
    "nombre": nombre,
    "id": idUser,
    "operacion": operacion,
    "tiempo": tiempo,
    "resultado": 0
  })


# !Bucle para imprimir los procesos
contadorGlob = 0
# for i in range(0, len(procesos)):
#   for j in range(0, len(procesos[i])):
#     print("------------------------------------")
#     print(f"| Lote en ejecucion: {i + 1}        Contador global(seg.):{contadorGlob}", end="\r")
#     print(f"------------------------------------")

#     contadorGlob+=1
#     # *Detiene el programa cada segundo
#     time.sleep(1)

for i in range(0, tiempoMax):
  print("\033[K", end="")
  print(f"------------------------------------")
  print(f"| Lote en ejecucion: {i + 1}        Contador global(seg.):{contadorGlob}")
  print(f"------------------------------------")
  contadorGlob+=1
  time.sleep(1)
  