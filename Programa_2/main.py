import os
from tabulate import tabulate
import time
import sys
from msvcrt import getch
from funciones import *

numProcesos = 0
while True:
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

ids = getId(numProcesos)
tiempos = getTiempos(numProcesos)
operaciones = generarOperaciones(numProcesos)

procesos = []
auxLote = []

for i in range(0, numProcesos):

  op = operaciones.pop()
  fNum = op["fNum"]
  sNum = op["sNum"]
  operacion = op["operacion"]

  auxLote.append({
    "id": ids.pop(),
    "tiempo": tiempos.pop(),
    "operacion": operacion,
    "fNum": fNum,
    "sNum": sNum,
    "resultado": 0,
    "error": False,
    "tiempoTrans": 0
  })

  if len(auxLote) == 4:
    procesos.append(auxLote)
    auxLote = []

#*Si no se llena el lote con 4 procesos, se agrega el lote incompleto
if (len(auxLote) < 4 and len(auxLote) > 0) or len(procesos) == 0:
  procesos.append(auxLote)

#*Ordena los procesos por ID
sortLotes(procesos)

columnas = ["Datos Generales:", "Lote en ejecucion:", "Proceso ejecutando:", "Procesos terminados:"]
contadorGlobal = 0
procesosTerminadosList = []
pausa = False

for indLote, lote in enumerate(procesos):
  while len(lote) > 0:
    proceso = lote.pop(0)

    while proceso["tiempo"] > 0:
      contadorGlobal += 1
      noLotes = max(0, len(procesos) - indLote)
      datosGenerales = f"No. lotes pendientes: {noLotes}\nContador global: {contadorGlobal}"

      loteEjecucion = "\n".join([f"ID: {proceso['id']} | Tiempo: {proceso['tiempo']} | Tiempo transcurrido: {proceso['tiempoTrans']}" for proceso in lote])

      procesoEjecutando = f"ID: {proceso['id']}\nOperacion: {proceso['operacion']}\nValores: {proceso['fNum']} {proceso['sNum']}\nTiempo: {proceso['tiempoTrans']}\nTiempo restante: {proceso['tiempo']}"
      proceso["tiempoTrans"] += 1
      proceso['tiempo'] -= 1

      # *Linea para mostrar todos los procesos terminados
      if not procesosTerminadosList:
        procesosTerminados = "No hay procesos\nterminados"
      else:
        procesosTerminados = "\n".join([f"Programa: {proceso['id']} | Operacion: {proceso['operacion']} | Datos: {proceso['fNum']} {proceso['sNum']} | {'Resultado: '+str(proceso['resultado']) if not proceso['error'] else 'Error'}" for ind, proceso in enumerate(procesosTerminadosList)])

      fila = [datosGenerales, loteEjecucion, procesoEjecutando, procesosTerminados]

      sys.stdout.write('\033[H')
      sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))
      sys.stdout.flush()
      time.sleep(1)
  
    if proceso["operacion"] == 1:
        proceso["resultado"] = suma(proceso["fNum"], proceso["sNum"])
    elif proceso["operacion"] == 2:
      proceso["resultado"] = resta(proceso["fNum"], proceso["sNum"])
    elif proceso["operacion"] == 3:
      proceso["resultado"] = multiplicacion(proceso["fNum"], proceso["sNum"])
    elif proceso["operacion"] == 4:
      proceso["resultado"] = division(proceso["fNum"], proceso["sNum"])
    elif proceso["operacion"] == 5:
      proceso["resultado"] = residuo(proceso["fNum"], proceso["sNum"])

    procesosTerminadosList.append(proceso)
  
  datosGenerales = f"No. lotes pendientes: {noLotes}\nContador global: {contadorGlobal}"
  loteEjecucion = " "
  procesoEjecutando = " "
  procesosTerminados = "\n".join([f"Programa: {proceso['id']} | Operacion: {proceso['operacion']} | Datos: {proceso['fNum']} {proceso['sNum']} | {'Resultado: '+str(proceso['resultado']) if not proceso['error'] else 'Error'}" for ind, proceso in enumerate(procesosTerminadosList)])

  fila = [datosGenerales, loteEjecucion, procesoEjecutando, procesosTerminados]

  sys.stdout.write('\033[H')
  sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))
  sys.stdout.flush()
  os.system("cls")

datosGenerales = f"No. lotes pendientes: {len(lote)}\nContador global: {contadorGlobal}"
loteEjecucion = " "
procesoEjecutando = " "
procesosTerminados = "\n".join([f"Programa: {proceso['id']} | Operacion: {proceso['operacion']} | Datos: {proceso['fNum']} {proceso['sNum']} | {'Resultado: '+str(proceso['resultado']) if not proceso['error'] else 'Error'}" for ind, proceso in enumerate(procesosTerminadosList)])

fila = [datosGenerales, loteEjecucion, procesoEjecutando, procesosTerminados]

sys.stdout.write('\033[H')
sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))
sys.stdout.flush()
input()