import os
import time
import sys
from tabulate import tabulate

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

  if operacion == 1:
    operacion = "Suma"
  elif operacion == 2:
    operacion = "Resta"
  elif operacion == 3:
    operacion = "Multiplicacion"
  elif operacion == 4:
    operacion = "Division"
  elif operacion == 5:
    operacion = "Residuo"

  # *Guarda todo en un diccionario y lo agrega a la lista de procesos
  auxLote.append({
    "nombre": nombre,
    "id": idUser,
    "operacion": operacion,
    "fNum": fNum,
    "sNum": sNum,
    "tiempo": tiempo,
    "resultado": 0
  })

  # *Comprueba con multiplos de 4 para agregar a la lista de procesos cada lote
  if (i+1) % 4 == 0:
    procesos.append(auxLote)
    auxLote = []
  
  # *En caso de que no se llegue ni a un lote o no se termine uno, guarda en automatico el ultimo lote que se estaba creando
  if i == numProcesos - 1:
    procesos.append(auxLote)
    auxLote = []

columnas = ["Datos Generales:", "Lote en ejecucion:", "Proceso ejecutando:", "Procesos terminados:"]
# !Bucle para imprimir los procesos
contadorGlobal = 0
for lote in procesos:
  # *Lista que guarda los procesos terminados
  procesosTerminadosList = []
  for index, proceso in enumerate(lote):
    # *Contador que lleva el numero de segundos del proceso
    contadorProceso = 0
    for i in range(0, proceso["tiempo"]):
      
      contadorGlobal += 1
      #*Se declaran todas las lineas a mostrar en la tabla
      noLotes = len(procesos) - 1
      datosGenerales = f"No. lotes pendientes: {noLotes}\nContador global: {contadorGlobal}"
      #*Se crea un string uniendose cada proceso del lote por un salto de linea, con el fin de imprimir todo el lote en una sola linea
      loteEjecucion = "\n".join([f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}" for proceso in lote])

      procesoEjecutando = f"ID: {proceso['id']}\nNombre: {proceso['nombre']}\nOperacion: {proceso['operacion']}\nTiempo estimado: {proceso['tiempo']}\nNo. proceso: {index+1}\nTiempo: {contadorProceso}\nTiempo restante: {proceso['tiempo'] - contadorProceso}"
      contadorProceso += 1

      # *Linea para mostrar todos los procesos terminados
      if not procesosTerminadosList:
        procesosTerminados = "No hay procesos\nterminados"
      else:
        procesosTerminados = "\n".join([f"Programa: {ind + 1}\nOperacion: {proceso['operacion']}\nDatos: {proceso['fNum']} {proceso['sNum']}\nResultado: {proceso['resultado']}\n" for ind, proceso in enumerate(procesosTerminadosList)])
      
      # !Se crea la tabla con los datos
      fila = [datosGenerales, loteEjecucion, procesoEjecutando, procesosTerminados]
      # *Se mueve el cursor al principio de la consola
      sys.stdout.write('\033[H')
      #* Se imprime la tabla
      sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))
      #* Se limpia la consola
      sys.stdout.flush()

      #*Se agrega a la lista de procesos terminados
      if proceso["tiempo"] - contadorProceso == 1:
        # *Se realiza la operacion correspondiente
        if proceso["operacion"] == "Suma":
          proceso["resultado"] = suma(proceso["fNum"], proceso["sNum"])
        elif proceso["operacion"] == "Resta":
          proceso["resultado"] = resta(proceso["fNum"], proceso["sNum"])
        elif proceso["operacion"] == "Multiplicacion":
          proceso["resultado"] = multiplicacion(proceso["fNum"], proceso["sNum"])
        elif proceso["operacion"] == "Division":
          proceso["resultado"] = division(proceso["fNum"], proceso["sNum"])
        elif proceso["operacion"] == "Residuo":
          proceso["resultado"] = residuo(proceso["fNum"], proceso["sNum"])

        procesosTerminadosList.append(proceso)

      #* Se detiene el programa por un segundo
      time.sleep(1)
  
  # *Justo antes de seguir con el siguiente lote, hace una pausa al programa con un input
  input()
  #* Se limpia la consola
  sys.stdout.flush()
  os.system("cls")
    