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
def buscarId(id, lote):
  #*Primero busca en todos los lotes, si es que existen
  if procesos:
    for lote in procesos:
      for proceso in lote:
        if proceso["id"] == id:
          return True
  #*Si se envia el loteAux, se analiza tambien ya que aun no se agrega a la lista de procesos
  if lote:
    for proceso in lote:
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
    if numProcesos <= 0:
      print("Ingrese un numero mayor a 0")
      input("Presione <enter> para continuar")
      os.system("cls")
      continue
    break
  except ValueError:
    print("Ingrese un numero valido")
    input("Presione <enter> para continuar")
    os.system("cls")
    continue

# *Se obtiene el numero de lotes a realizar
numLotes = numProcesos // 4

for i in range(0, numProcesos):

  while(True):
    os.system("cls")
    nombre = input("Ingrese un nombre: ")
    # *Si el nombre esta vacio o contiene numeros, se vuelve a pedir
    if nombre == "" or not nombre.strip() or not nombre.isalpha():
      print("Ingrese un nombre valido")
      input("Presione <enter> para continuar")
      os.system("cls")
      continue
    break

  while(True):
    idUser = input("Ingrese un ID: ")
    # *Verifica que el ID no este en la lista
    if idUser == "" or not idUser.strip() or buscarId(idUser, auxLote):
      print("Ingrese un ID valido o que no este repetido")
      input("Presione <enter> para continuar")
      os.system("cls")
      continue
    break

  while(True):
    try:
      fNum, sNum = map(int, input("Ingrese dos numeros separados por un espacio: ").split())
      break
    except ValueError:
      print("Ingrese dos numeros validos separados por un espacio")
      input("Presione <enter> para continuar")
      os.system("cls")
      continue

  # *Bucle en caso de que una operacion sea invalida con los numeros ingresados
  while(True):
    try:
      operacion = int(input("1.- +\n2.- -\n3.- *\n4.- / \n5.- %\nIngrese la operacion a realizar: "))
      if operacion <= 0 or operacion > 5:
        print("Ingrese una opcion valida")
        # *Regresa al inicio del bucle
        input("Presione <enter> para continuar")
        os.system("cls")
        continue

      if (operacion == 4 or operacion == 5) and sNum == 0:
        print("Operacion invalida para los numeros ingresados")
        input("Presione <enter> para continuar")
        os.system("cls")
        continue
      break
    except ValueError:
      print("Ingrese una opcion valida")
      input("Presione <enter> para continuar")
      os.system("cls")
      continue

  while(True):
    try:
      tiempo = int(input("Ingrese el tiempo de ejecucion en segundos: "))
      if tiempo <= 0:
        print("El tiempo debe ser mayor a 0")
        input("Presione <enter> para continuar")
        os.system("cls")
        continue
      tiempoMax += tiempo
      break
    except ValueError:
      print("Ingrese un numero valido")
      input("Presione <enter> para continuar")
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
# *Lista que guarda los procesos terminados
procesosTerminadosList = []
for indexLote, lote in enumerate(procesos):
  for numProceso in range(0, len(lote)):
    #*Saca el proceso del lote y comienza a mostrarlo
    popProceso = lote.pop(0)
    contadorProceso = 0
    for i in range(0, popProceso["tiempo"]):
      contadorGlobal += 1
      #*Se declaran todas las lineas a mostrar en la tabla
      noLotes = max(0, len(procesos) - indexLote - 1)
      datosGenerales = f"No. lotes pendientes: {noLotes}\nContador global: {contadorGlobal}"
      #*Se crea un string uniendose cada proceso del lote por un salto de linea, con el fin de imprimir todo el lote en una sola linea
      loteEjecucion = "\n".join([f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']}" for proceso in lote])

      procesoEjecutando = f"ID: {popProceso['id']}\nNombre: {popProceso['nombre']}\nOperacion: {popProceso['operacion']}\nTiempo estimado: {popProceso['tiempo']}\nNo. Proceso: {numProceso+1}\nTiempo: {contadorProceso}\nTiempo restante: {popProceso['tiempo'] - contadorProceso}"
      contadorProceso += 1

      # *Linea para mostrar todos los procesos terminados
      if not procesosTerminadosList:
        procesosTerminados = "No hay procesos\nterminados"
      else:
        procesosTerminados = "\n".join([f"Programa: {ind + 1} | Operacion: {proceso['operacion']} | Datos: {proceso['fNum']} {proceso['sNum']} | Resultado: {proceso['resultado']}" for ind, proceso in enumerate(procesosTerminadosList)])

      # !Se crea la tabla con los datos
      fila = [datosGenerales, loteEjecucion, procesoEjecutando, procesosTerminados]
      # *Se mueve el cursor al principio de la consola
      sys.stdout.write('\033[H')
      #* Se imprime la tabla
      sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))
      #* Se limpia la consola
      sys.stdout.flush()
      #* Se detiene el programa por un segundo
      time.sleep(1)

    #*Se agrega a la lista de procesos terminados
    # *Se realiza la operacion correspondiente
    if popProceso["operacion"] == "Suma":
      popProceso["resultado"] = suma(popProceso["fNum"], popProceso["sNum"])
    elif popProceso["operacion"] == "Resta":
      popProceso["resultado"] = resta(popProceso["fNum"], popProceso["sNum"])
    elif popProceso["operacion"] == "Multiplicacion":
      popProceso["resultado"] = multiplicacion(popProceso["fNum"], popProceso["sNum"])
    elif popProceso["operacion"] == "Division":
      popProceso["resultado"] = division(popProceso["fNum"], popProceso["sNum"])
    elif popProceso["operacion"] == "Residuo":
      popProceso["resultado"] = residuo(popProceso["fNum"], popProceso["sNum"])

    procesosTerminadosList.append(popProceso)

  # *Justo antes de seguir con el siguiente lote, imprime la tabla por ultima vez
  datosGenerales = f"No. lotes pendientes: {noLotes}\nContador global: {contadorGlobal}"
  loteEjecucion = " "
  procesoEjecutando = " "
  procesosTerminados = "\n".join([f"Programa: {ind + 1} | Operacion: {proceso['operacion']} | Datos: {proceso['fNum']} {proceso['sNum']} | Resultado: {proceso['resultado']}" for ind, proceso in enumerate(procesosTerminadosList)])

  fila = [datosGenerales, loteEjecucion, procesoEjecutando, procesosTerminados]

  sys.stdout.write('\033[H')
  sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))

  #* Se limpia la consola
  sys.stdout.flush()
  os.system("cls")

#*Al final, imprime la tabla con todos los elementos terminados y el ultimo proceso ejecutado
datosGenerales = f"No. lotes pendientes: {noLotes}\nContador global: {contadorGlobal}"
loteEjecucion = " "
procesoEjecutando = " "
procesosTerminados = "\n".join([f"Programa: {ind + 1} | Operacion: {proceso['operacion']} | Datos: {proceso['fNum']} {proceso['sNum']} | Resultado: {proceso['resultado']}" for ind, proceso in enumerate(procesosTerminadosList)])

fila = [datosGenerales, loteEjecucion, procesoEjecutando, procesosTerminados]

sys.stdout.write('\033[H')
sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))
sys.stdout.flush()
input()