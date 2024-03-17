import os
from tabulate import tabulate
import time
import sys
import msvcrt
from funciones import *

global pausa
global mostrarTabla
pausa = False
mostrarTabla = False
#*Regresa el metodo para estar esperando en todo momento el input
def getWatch():
  return msvcrt.kbhit()

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
columnasPausa = ["ID", "Estado", "Operacion", "Datos", "Resultado", "Tiempos"]
tablaPausa = []

for i in range(0, numProcesos):

  op = operaciones.pop(0)
  fNum = op["fNum"]
  sNum = op["sNum"]
  operacion = op["operacion"]
  operacionStr = op["operacionStr"]

  tiempo = tiempos.pop(0)

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

# print(procesos)
# input()

#*Asigna los cuatro primeros procesos a la memoria principal
if len(procesos) > 4:
  for i in range(0, 4):
    if i == 4:
      break
    memoriaPrincipal.append(procesos.pop(0))
else:
  for i in range(0, len(procesos)):
    memoriaPrincipal.append(procesos.pop(0))

columnas = ["Datos Generales:", "Cola de listos:", "Proceso\nejecutando:", "Procesos\nbloqueados", "Procesos\nterminados:"]
contadorGlobal = 0
procesosTerminadosList = []
procesosBloqueados = []

while len(procesos) > 0 or len(memoriaPrincipal) > 0 or len(procesosBloqueados) > 0:

  #*Obtiene proceso a ejecutar
  #*Comprueba si hay procesos en la memoria principal (todos en bloqueado)
  if len(memoriaPrincipal) != 0 and len(procesosBloqueados) < 4:
    procesoEjecutar = memoriaPrincipal.pop(0)
  else:

    contadorGlobal += 1

    if getWatch():
      char = msvcrt.getch()
      if char.lower() == b'p':
        pausa = True
      elif char.lower() == b'c':
        pausa = False
        mostrarTabla = False
      elif char.lower() == b'n':
        #*Crea un nuevo proceso
        newTiempo = generaTiempo()
        newOperaciones = generaOperacion()
        auxProceso = {
          "id": generaId(),
          "tiempo": newTiempo,
          "tiempoEstimado": newTiempo,
          "operacion": newOperaciones["operacion"],
          "operacionStr": newOperaciones["operacionStr"],
          "fNum": newOperaciones["fNum"],
          "sNum": newOperaciones["sNum"],
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
        }
        #*Si hay espacio en la memoria principal, se agrega el proceso
        if (len(memoriaPrincipal) + len(procesosBloqueados)) < 3:
          memoriaPrincipal.append(auxProceso)
        else:
          procesos.append(auxProceso)
      elif char.lower() == b'b':
        mostrarTabla = True
        pausa = True
    if pausa:
      while pausa:
        if(mostrarTabla):
          tablaPausa = []
          #!Muestra la tabla "final"
          #?Para todos los procesos en no terminados se agrega el tiempo restante de CPU(tiempoEstimado)
          #*Comprueba si hay procesos terminados
          if len(procesosTerminadosList) > 0:
            for proceso in procesosTerminadosList:
              tiemposProceso = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: {proceso['tiempoFinalizacion']}\nTiempo retorno: {proceso['tiempoRetorno']}\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta']}\nTiempo servicio: {proceso['tiempoServicio']}"
              tablaPausa.append([proceso["id"], "Terminado", proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", proceso["resultado"] if not proceso["error"] else "Error", tiemposProceso])
          
          #*Procesos nuevos
          if len(procesos) > 0:
            for proceso in procesos:
              tablaPausa.append([proceso["id"], "Nuevo", proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", "No ha iniciado", "No ha iniciado"])

          #*Procesos listos
          if len(memoriaPrincipal) > 0:
            for proceso in memoriaPrincipal:
              #*Se calculan los tiempos necesarios
              proceso["tiempoServicio"] = proceso["tiempoTrans"]
              proceso["tiempoEspera"] = max(0, (contadorGlobal - proceso["tiempoLlegada"]) - proceso["tiempoServicio"])
              tiemposProceso = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: No terminado\nTiempo retorno: No terminado\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta']}\nTiempo servicio: {proceso['tiempoServicio']}\nTiempo restante CPU: {proceso['tiempoEstimado']}"
              tablaPausa.append([proceso["id"], "Listo",proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", "No ha terminado", tiemposProceso])

          if len(procesosBloqueados) > 0:
            for proceso in procesosBloqueados:
              proceso["tiempoServicio"] = proceso["tiempoTrans"]
              
              proceso["tiempoEspera"] = max(0, (contadorGlobal - proceso["tiempoLlegada"]) - proceso["tiempoServicio"])
              #?En bloqueados se muestra el tiempo que lleva (timeOut)
              tiemposProceso = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: No terminado\nTiempo retorno: No terminado\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta']}\nTiempo servicio: {proceso['tiempoServicio']}\nBloqueo restante: {8 - proceso['timeOut']}\nTiempo restante CPU: {proceso['tiempoEstimado']}"
              tablaPausa.append([proceso["id"], "Bloqueado",proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", "No ha terminado", tiemposProceso])

          #?Al final se muestra el proceso en ejecucion
          if procesoEjecutar is not None:
            procesoEjecutar["tiempoServicio"] = procesoEjecutar["tiempoTrans"]
            procesoEjecutar["tiempoEspera"] = max(0, contadorGlobal - procesoEjecutar["tiempoLlegada"] - procesoEjecutar["tiempoServicio"])
            tiemposProceso = f"Tiempo llegada: {procesoEjecutar['tiempoLlegada']}\nTiempo finalizacion: No terminado\nTiempo retorno: No terminado\nTiempo espera: {procesoEjecutar['tiempoEspera']}\nTiempo respuesta: {procesoEjecutar['tiempoRespuesta']}\nTiempo servicio: {procesoEjecutar['tiempoServicio']}\nTiempo restante CPU: {procesoEjecutar['tiempoEstimado']}"
            procesoEjecutando = f"ID: {procesoEjecutar['id']}\nOperacion: {procesoEjecutar['operacionStr']}\nValores: {procesoEjecutar['fNum']} {procesoEjecutar['sNum']}\nTiempo transcurrido: {procesoEjecutar['tiempoTrans']}\nTiempo restante: {procesoEjecutar['tiempoEstimado']}"
            tablaPausa.append([procesoEjecutar["id"], "Ejecutando", procesoEjecutar["operacionStr"], f"{procesoEjecutar['fNum']} {procesoEjecutar['sNum']}", "No ha terminado", tiemposProceso])

          sys.stdout.write('\033[H')
          sys.stdout.write(tabulate(tablaPausa, headers=columnasPausa, tablefmt='fancy_grid'))
          sys.stdout.flush()
        
        if getWatch():
          char = msvcrt.getch()
          if char.lower() == b'c':
            pausa = False
            mostrarTabla = False
            os.system("cls")
        time.sleep(0.1)

    for proceso in procesosBloqueados:
      proceso["timeOut"] += 1
      if proceso["timeOut"] == 8:
        proceso["timeOut"] = 0
        memoriaPrincipal.append(proceso)
        procesosBloqueados.pop(0)

    #*Se imprime la tabla y se modifican los tiempos de bloqueado
    datosGenerales = f"Contador global: {contadorGlobal}\nProcesos nuevos: {len(procesos)}"

    memoriaListos = ""

    procesoEjecutando = ""
    procesosBloq = "\n".join([f"ID: {proceso['id']} | Tiempo restante: {8 - proceso['timeOut']}" for proceso in procesosBloqueados])

    if len(procesosTerminadosList) > 0:
      procesosTerminados = "\n".join([f"ID: {proceso['id']} | Operacion: {proceso['operacionStr']}\nDatos: {proceso['fNum']} {proceso['sNum']} | {'Resultado: '+str(proceso['resultado']) if not proceso['error'] else 'Error'}\n" for ind, proceso in enumerate(procesosTerminadosList)])
    else:
      procesosTerminados = "No hay procesos\nterminados"
    
    fila = [datosGenerales, memoriaListos, procesoEjecutando, procesosBloq, procesosTerminados]

    sys.stdout.write('\033[H')
    sys.stdout.write(tabulate([fila], headers=columnas, tablefmt='fancy_grid'))
    sys.stdout.flush()
    time.sleep(1)
    continue

  if (len(memoriaPrincipal) + len(procesosBloqueados)) < 3 and len(procesos) > 0:
    #*Agrega un nuevo proceso a la memoria principal (procesos en ejecucion)
    newProceso = procesos.pop(0)
    newProceso["tiempoLlegada"] = contadorGlobal
    memoriaPrincipal.append(newProceso)

  while(procesoEjecutar["tiempoEstimado"] > 1):

    contadorGlobal += 1

    #!Casos de interrupcion o error
    if getWatch():
      char = msvcrt.getch()
      if char.lower() == b'p':
        pausa = True
      elif char.lower() == b'c':
        pausa = False
        mostrarTabla = False
      elif char.lower() == b'e':
        procesosBloqueados.append(procesoEjecutar)
        procesoEjecutar = None
        time.sleep(0.1)
        break
      elif char.lower() == b'w':
        procesoEjecutar["error"] = True
        procesoEjecutar["resultado"] = "Error"
        procesoEjecutar["tiempoFinalizacion"] = contadorGlobal
        procesoEjecutar["tiempoRetorno"] = procesoEjecutar["tiempoFinalizacion"] - procesoEjecutar["tiempoLlegada"]
        procesoEjecutar["tiempoServicio"] = procesoEjecutar["tiempoTrans"]
        procesoEjecutar["tiempoEspera"] = procesoEjecutar["tiempoRetorno"] - procesoEjecutar["tiempoServicio"]

        procesosTerminadosList.append(procesoEjecutar)
        procesoEjecutar = None
        time.sleep(0.1)
        break
      elif char.lower() == b'n':
        #*Crea un nuevo proceso
        newTiempo = generaTiempo()
        newOperaciones = generaOperacion()
        auxProceso = {
          "id": generaId(),
          "tiempo": newTiempo,
          "tiempoEstimado": newTiempo,
          "operacion": newOperaciones["operacion"],
          "operacionStr": newOperaciones["operacionStr"],
          "fNum": newOperaciones["fNum"],
          "sNum": newOperaciones["sNum"],
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
        }
        #*Si hay espacio en la memoria principal, se agrega el proceso
        if (len(memoriaPrincipal) + len(procesosBloqueados)) < 3:
          memoriaPrincipal.append(auxProceso)
        else:
          procesos.append(auxProceso)
      elif char.lower() == b'b':
        mostrarTabla = True
        pausa = True
    if pausa:
      while pausa:
        if(mostrarTabla):
          tablaPausa = []
          #!Muestra la tabla "final"
          #?Para todos los procesos en no terminados se agrega el tiempo restante de CPU(tiempoEstimado)
          #*Comprueba si hay procesos terminados
          if len(procesosTerminadosList) > 0:
            for proceso in procesosTerminadosList:
              tiemposProceso = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: {proceso['tiempoFinalizacion']}\nTiempo retorno: {proceso['tiempoRetorno']}\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta']}\nTiempo servicio: {proceso['tiempoServicio']}"
              tablaPausa.append([proceso["id"], "Terminado", proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", proceso["resultado"] if not proceso["error"] else "Error", tiemposProceso])
          
          #*Procesos nuevos
          if len(procesos) > 0:
            for proceso in procesos:
              tablaPausa.append([proceso["id"], "Nuevo", proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", "No ha iniciado", "No ha iniciado"])

          #*Procesos listos
          if len(memoriaPrincipal) > 0:
            for proceso in memoriaPrincipal:
              #*Se calculan los tiempos necesarios
              proceso["tiempoServicio"] = proceso["tiempoTrans"]
              proceso["tiempoEspera"] = max(0, (contadorGlobal - proceso["tiempoLlegada"]) - proceso["tiempoServicio"])
              tiemposProceso = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: No terminado\nTiempo retorno: No terminado\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta']}\nTiempo servicio: {proceso['tiempoServicio']}\nTiempo restante CPU: {proceso['tiempoEstimado']}"
              tablaPausa.append([proceso["id"], "Listo",proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", "No ha terminado", tiemposProceso])

          if len(procesosBloqueados) > 0:
            for proceso in procesosBloqueados:
              proceso["tiempoServicio"] = proceso["tiempoTrans"]
              
              proceso["tiempoEspera"] = max(0, (contadorGlobal - proceso["tiempoLlegada"]) - proceso["tiempoServicio"])
              #?En bloqueados se muestra el tiempo que lleva (timeOut)
              tiemposProceso = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: No terminado\nTiempo retorno: No terminado\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta']}\nTiempo servicio: {proceso['tiempoServicio']}\nBloqueo restante: {8 - proceso['timeOut']}\nTiempo restante CPU: {proceso['tiempoEstimado']}"
              tablaPausa.append([proceso["id"], "Bloqueado",proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", "No ha terminado", tiemposProceso])

          #?Al final se muestra el proceso en ejecucion
          if procesoEjecutar is not None:
            procesoEjecutar["tiempoServicio"] = procesoEjecutar["tiempoTrans"]
            procesoEjecutar["tiempoEspera"] = max(0, contadorGlobal - procesoEjecutar["tiempoLlegada"] - procesoEjecutar["tiempoServicio"])
            tiemposProceso = f"Tiempo llegada: {procesoEjecutar['tiempoLlegada']}\nTiempo finalizacion: No terminado\nTiempo retorno: No terminado\nTiempo espera: {procesoEjecutar['tiempoEspera']}\nTiempo respuesta: {procesoEjecutar['tiempoRespuesta']}\nTiempo servicio: {procesoEjecutar['tiempoServicio']}\nTiempo restante CPU: {procesoEjecutar['tiempoEstimado']}"
            procesoEjecutando = f"ID: {procesoEjecutar['id']}\nOperacion: {procesoEjecutar['operacionStr']}\nValores: {procesoEjecutar['fNum']} {procesoEjecutar['sNum']}\nTiempo transcurrido: {procesoEjecutar['tiempoTrans']}\nTiempo restante: {procesoEjecutar['tiempoEstimado']}"
            tablaPausa.append([procesoEjecutar["id"], "Ejecutando", procesoEjecutar["operacionStr"], f"{procesoEjecutar['fNum']} {procesoEjecutar['sNum']}", "No ha terminado", tiemposProceso])

          sys.stdout.write('\033[H')
          sys.stdout.write(tabulate(tablaPausa, headers=columnasPausa, tablefmt='fancy_grid'))
          sys.stdout.flush()
        
        if getWatch():
          char = msvcrt.getch()
          if char.lower() == b'c':
            pausa = False
            mostrarTabla = False
            os.system("cls")
        time.sleep(0.1)

    #*Tiempos de respuesta
    if not procesoEjecutar["banderaRespuesta"]:
      procesoEjecutar["tiempoRespuesta"] = contadorGlobal - 1
      procesoEjecutar["banderaRespuesta"] = True
    
    #contadorGlobal += 1

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
          procesosBloqueados.pop(0)

    #*Campos para las columnas de la tabla
    datosGenerales = f"Contador global: {contadorGlobal}\nProcesos nuevos: {len(procesos)}"

    memoriaListos = "\n".join([f"ID: {proceso["id"]} | Tiempo estimado: {proceso["tiempo"]} | Tiempo transcurrido: {proceso['tiempoTrans']}" for proceso in memoriaPrincipal])

    procesoEjecutando = f"ID: {procesoEjecutar['id']}\nOperacion: {procesoEjecutar['operacionStr']}\nValores: {procesoEjecutar['fNum']} {procesoEjecutar['sNum']}\nTiempo transcurrido: {procesoEjecutar['tiempoTrans']}\nTiempo restante: {procesoEjecutar['tiempoEstimado']}"

    if len(procesosBloqueados) > 0:
      procesosBloq = "\n".join([f"ID: {proceso['id']} | Tiempo restante: {8 - proceso['timeOut']}" for proceso in procesosBloqueados])
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
  
  os.system("cls")

  #*Proceso termina
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

    procesoEjecutar["tiempoFinalizacion"] = contadorGlobal
    procesoEjecutar["tiempoRetorno"] = procesoEjecutar["tiempoFinalizacion"] - procesoEjecutar["tiempoLlegada"]
    #*Si no hubo error en el proceso, se guarda el tiempo de servicio como el TME
    procesoEjecutar["tiempoServicio"] = procesoEjecutar["tiempo"]
    #*Tiempo que pasó en espera
    procesoEjecutar["tiempoEspera"] = procesoEjecutar["tiempoRetorno"] - procesoEjecutar["tiempoServicio"]

    procesosTerminadosList.append(procesoEjecutar)

#*Se crea otra tabla para mostrar los resultados finales

columnas = ["ID", "Operacion", "Datos", "Resultado", "Tiempos"]

printProcesos = []

for proceso in procesosTerminadosList:

  tiemposProceso = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: {proceso['tiempoFinalizacion']}\nTiempo retorno: {proceso['tiempoRetorno']}\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta']}\nTiempo servicio: {proceso['tiempoServicio']}"

  printProcesos.append([proceso["id"], proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", proceso["resultado"] if not proceso["error"] else "Error", tiemposProceso])

os.system("cls")
sys.stdout.write('\033[H')
sys.stdout.write(tabulate(printProcesos, headers=columnas, tablefmt='fancy_grid'))
sys.stdout.flush()
time.sleep(1)