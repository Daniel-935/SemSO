import os

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
  for proceso in procesos:
    if proceso["id"] == id:
      return True
  return False

# *Lista para guardar los procesos agregados
procesos = []

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

for i in range(0, numProcesos):
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
      break
    except ValueError:
      print("Ingrese un numero valido")
      input()
      os.system("cls")
      continue

  # *Guarda todo en un diccionario y lo agrega a la lista de procesos
  procesos.append({
    "nombre": nombre,
    "id": idUser,
    "operacion": operacion,
    "tiempo": tiempo,
    "resultado": 0
  })

print(procesos)

