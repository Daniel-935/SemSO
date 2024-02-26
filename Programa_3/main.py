import os
from tabulate import tabulate
import time
import sys
import msvcrt
from funciones import *

pausa = False
#*Regresa el metodo para estar esperando en todo momento el input
def getWatch():
  return msvcrt.kbhit()

def cambiaPausa():
  global pausa
  if getWatch():
    char = msvcrt.getch()
    if char.lower() == b'p':
      pausa = True
    elif char.lower() == b'c':
      pausa = False

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

#*Ahora los procesos se guardan individualmente
procesos = []
#*Lista para tener control sobre la memoria principal (procesos en ejecucion)
memoriaPrincipal = []

for i in range(0, numProcesos):

  op = operaciones.pop()
  fNum = op["fNum"]
  sNum = op["sNum"]
  operacion = op["operacion"]
  operacionStr = op["operacionStr"]

  tiempo = tiempos.pop()

  #*El timeout cuando este en bloqueado es de 8 segundos
  procesos.append({
    "id": ids.pop(),
    "tiempo": tiempo,
    "tiempoEstimado": tiempo,
    "operacion": operacion,
    "operacionStr": operacionStr,
    "fNum": fNum,
    "sNum": sNum,
    "resultado": 0,
    "error": False,
    "tiempoTrans": 0,
    "tiempoLlegada": 0,
    "tiempoFinalizacion": 0,
    "tiempoRetorno": 0,
    "tiempoEspera": 0,
    "tiempoRespuesta": 0,
    "tiempoServicio": 0,
    "timeOut": 0,
    "banderaRespuesta": False
  })

#*Asigna los cuatro primeros procesos a la memoria principal
for i in range(0, 4):
  if i == 4:
    break
  memoriaPrincipal.append(procesos.pop())

columnas = ["Datos Generales:", "Cola de listos:", "Proceso\nejecutando:", "Procesos\nbloqueados", "Procesos\nterminados:"]
contadorGlobal = 0
procesosTerminadosList = []
procesosBloqueados = []

while len(procesos) > 0 or len(memoriaPrincipal) > 0:

  if getWatch():
    char = msvcrt.getch()
    if char.lower() == b'p':
      pausa = True
    elif char.lower() == b'c':
      pausa = False
  if pausa:
    while pausa:
      cambiaPausa()
      time.sleep(0.1)

  #*Obtiene proceso a ejecutar
  procesoEjecutar = memoriaPrincipal.pop()

  if (len(memoriaPrincipal) + len(procesosBloqueados)) < 4 and len(procesos) > 0:
    #*Agrega un nuevo proceso a la memoria principal (procesos en ejecucion)
    newProceso = procesos.pop()
    newProceso["tiempoLlegada"] = contadorGlobal
    memoriaPrincipal.append(newProceso)

  while(procesoEjecutar["tiempoEstimado"] > 0):

    if getWatch():
      char = msvcrt.getch()
      if char.lower() == b'p':
        pausa = True
      elif char.lower() == b'c':
        pausa = False
      elif char.lower() == b'e':
        procesosBloqueados.append(procesoEjecutar)
        procesoEjecutar = None
        time.sleep(0.1)
        break
      elif char.lower() == b'w':
        procesoEjecutar["error"] = True
        procesoEjecutar["resultado"] = "Error"
        procesosTerminadosList.append(procesoEjecutar)
        procesoEjecutar = None
        time.sleep(0.1)
        break
    if pausa:
      while pausa:
        cambiaPausa()
        time.sleep(0.1)
      
    contadorGlobal += 1

    #*Modifica los valores de tiempos
    procesoEjecutar["tiempoTrans"] += 1
    procesoEjecutar['tiempoEstimado'] -= 1

    #?Ajusta el tiempo de espera para cada uno de los bloqueados
    if len(procesosBloqueados) > 0:
      for proceso in procesosBloqueados:
        proceso["timeOut"] += 1
        if proceso["timeOut"] == 8:
          proceso["timeOut"] = 0
          memoriaPrincipal.append(proceso)
          procesosBloqueados.remove(proceso)

    #*Campos para las columnas de la tabla
    datosGenerales = f"Contador global: {contadorGlobal}\nProcesos nuevos: {len(procesos)}"

    memoriaListos = "\n".join([f"ID: {proceso["id"]} | Tiempo estimado: {proceso["tiempo"]} | Tiempo transcurrido: {proceso['tiempoTrans']}" for proceso in memoriaPrincipal])

    procesoEjecutando = f"ID: {procesoEjecutar['id']}\nOperacion: {procesoEjecutar['operacionStr']}\nValores: {procesoEjecutar['fNum']} {procesoEjecutar['sNum']}\nTiempo transcurrido: {procesoEjecutar['tiempoTrans']}\nTiempo restante: {procesoEjecutar['tiempoEstimado']}"

    if len(procesosBloqueados) > 0:
      procesosBloq = "\n".join([f"ID: {proceso['id']} | Tiempo: {proceso['timeOut']}" for proceso in procesosBloqueados])
    else:
      procesosBloq = "No hay\nprocesos bloqueados"

    if len(procesosTerminadosList) > 0:
      procesosTerminados = "\n".join([f"ID: {proceso['id']} | Operacion: {proceso['operacionStr']}\nDatos: {proceso['fNum']} {proceso['sNum']} | {'Resultado: '+str(proceso['resultado']) if not proceso['error'] else 'Error'}\n" for ind, proceso in enumerate(procesosTerminadosList)])
    else:
      procesosTerminados = "No hay procesos\nterminados"
    
    fila = [datosGenerales, memoriaListos, procesoEjecutando, procesosBloq, procesosTerminados]

    sys.stdout.write('\033[H')
    sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))
    sys.stdout.flush()
    time.sleep(1)

    #!Casos de interrupcion o error
    if getWatch():
      char = msvcrt.getch()
      if char.lower() == b'p':
        pausa = True
      elif char.lower() == b'c':
        pausa = False
      elif char.lower() == b'e':
        procesosBloqueados.append(procesoEjecutar)
        procesoEjecutar = None
        time.sleep(0.1)
        break
      elif char.lower() == b'w':
        procesoEjecutar["error"] = True
        procesoEjecutar["resultado"] = "Error"
        procesosTerminadosList.append(procesoEjecutar)
        procesoEjecutar = None
        time.sleep(0.1)
        break
    if pausa:
      while pausa:
        cambiaPausa()
        time.sleep(0.1)
  
  if procesoEjecutar is not None:
    if procesoEjecutar["operacion"] == 1:
        procesoEjecutar["resultado"] = suma(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
    elif procesoEjecutar["operacion"] == 2:
      procesoEjecutar["resultado"] = resta(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
    elif procesoEjecutar["operacion"] == 3:
      procesoEjecutar["resultado"] = multiplicacion(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
    elif procesoEjecutar["operacion"] == 4:
      procesoEjecutar["resultado"] = division(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
    elif procesoEjecutar["operacion"] == 5:
      procesoEjecutar["resultado"] = residuo(procesoEjecutar["fNum"], procesoEjecutar["sNum"])

    procesosTerminadosList.append(procesoEjecutar)

datosGenerales = f"Contador global: {contadorGlobal}\nProcesos nuevos: {len(procesos)}"

memoriaListos = "\n".join([f"ID: {proceso['id']} | Tiempo estimado: {proceso['tiempo']} | Tiempo transcurrido: {proceso['tiempoTrans']}" for proceso in memoriaPrincipal])

procesoEjecutando = ""

procesosBloq = "\n".join([f"ID: {proceso['id']} | Tiempo: {proceso['timeOut']}" for proceso in procesosBloqueados])

procesosTerminados = "\n".join([f"ID: {proceso['id']} | Operacion: {proceso['operacionStr']}\nDatos: {proceso['fNum']} {proceso['sNum']} | {'Resultado: '+str(proceso['resultado']) if not proceso['error'] else 'Error'}\n" for ind, proceso in enumerate(procesosTerminadosList)])

fila = [datosGenerales, memoriaListos, procesoEjecutando, procesosBloq, procesosTerminados]

sys.stdout.write('\033[H')
sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))
sys.stdout.flush()
time.sleep(1)