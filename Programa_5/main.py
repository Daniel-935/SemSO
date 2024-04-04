from tabulate import tabulate
import os
import time
import sys
import msvcrt

#*Modulos con las funciones
from funciones import *

while True:
  try:
    numProcesos = int(input("Ingrese el numero de procesos a realizar: "))
    if numProcesos <= 0:
      print("Por favor, ingrese un número entero positivo.")
      input("Presione <enter> para continuar")
      os.system("cls")
      continue
    break
  except ValueError:
    print("Por favor, ingrese un número entero.")
    input("Presione <enter> para continuar")
    os.system("cls")
    continue

while True:
  try:
    quantum = int(input("Ingrese el quantum deseado: "))
    if quantum < 5 or quantum >= 15:
      print("Por favor, ingrese un numero valido de quantum.")
      input("Presione <enter> para continuar")
      os.system("cls")
      continue
    break
  except ValueError:
    print("Por favor, ingrese un número entero.")
    input("Presione <enter> para continuar")
    os.system("cls")
    continue

#*Variables globales que se utilizan en toda la ejecucion
columnasEjecucion = ["Datos Generales:", "Cola de listos:", "Proceso\nejecutando:", "Procesos\nbloqueados", "Procesos\nterminados:"]
columnasTerminados = ["ID", "Operacion", "Datos", "Resultado", "Tiempos"]
columnasPausa = ["ID", "Estado", "Operacion", "Datos", "Resultado", "Tiempos"]

procesosNuevos = []
procesosListos = []
procesosBloqueados = []
procesosTerminados = []
contadorGlobal = 0
global mostrarTabla
global pausa
mostrarTabla = False
pausa = False

procesosNuevos = generaProcesos(numProcesos, quantum)[:]

#*Agrega los procesos nuevos a listos (maximo 4)
while len(procesosListos) < 4 and len(procesosNuevos) > 0:
  procesosListos.append(procesosNuevos.pop(0))
  procesosListos[-1]["tiempoLlegada"] = contadorGlobal

#!Bucle principal
while len(procesosListos) > 0 or len(procesosBloqueados) > 0 or len(procesosNuevos) > 0:
  
  #*Toma el primer proceso de la lista de listos
  if len(procesosListos) > 0:
    procesoEjecutar = procesosListos.pop(0)

  #*Comprueba si hay espacio libre en la memoria principal
  if (len(procesosListos) + len(procesosBloqueados)) + 1 < 4 and len(procesosNuevos) > 0:
    newListo = procesosNuevos.pop(0)
    newListo["tiempoLlegada"] = contadorGlobal
    procesosListos.append(newListo)

  #!Ejecuta el proceso de acuerdo al quantum
  if procesoEjecutar["tiempoRestante"] > 0:
    while procesoEjecutar["quantum"] > 0 and procesoEjecutar["tiempoRestante"] > 0:

      if procesoEjecutar["banderaRespuesta"] == False:
        procesoEjecutar["tiempoRespuesta"] = contadorGlobal
        procesoEjecutar["banderaRespuesta"] = True

      contadorGlobal += 1
      
      #*Si todos estan en bloqueado, no tiene porque modificar estos valores
      if len(procesosBloqueados) < 4:
        procesoEjecutar["tiempoRestante"] -= 1
        procesoEjecutar["tiempoTrans"] += 1
        procesoEjecutar["quantum"] -= 1

      #*Actualiza los tiempos de los bloqueados
      if len(procesosBloqueados) > 0:
        for proceso in procesosBloqueados:
          proceso["timeOut"] += 1
          #*En caso de que se termine el tiempo de bloqueo
          if proceso["timeOut"] == 8:
            proceso["bloqueado"] = False
            procesosListos.append(procesosBloqueados.pop(0))

      #?Funciones en caso de presionar una tecla
      if msvcrt.kbhit():
        char = msvcrt.getch()
        if char.lower() == b'p':
          pausa = True
        elif char.lower() == b'e':
          if procesoEjecutar["tiempoRestante"] > 0:
            #*Se reinicia el quantum ya que sera enviado a la cola de listos otra vez
            procesoEjecutar["bloqueado"] = True
            procesoEjecutar["quantum"] = quantum
            procesosBloqueados.append(procesoEjecutar)
            break
        elif char.lower() == b'w':
          procesoEjecutar["tiempoRestante"] = 0
          procesoEjecutar["error"] = True
          calculaTiempos(procesoEjecutar, contadorGlobal, 1)
          # procesosTerminados.append(procesoEjecutar)
          # procesoEjecutar = None
          break
        elif char.lower() == b'n':
          #*Crea un nuevo proceso
          #*Comprueba si hay espacio en la memoria principal
          if (len(procesosListos) + len(procesosBloqueados)) + 1 < 4:
            nuevoProceso = generaProceso(quantum)
            nuevoProceso["tiempoLlegada"] = contadorGlobal
            procesosListos.append(nuevoProceso)
          else:
            procesosNuevos.append(generaProceso(quantum))
        elif char.lower() == b'b':
          pausa = True
          mostrarTabla = True
      #*Bucle infinito hasta que se quite la pausa
      if pausa:
        while True:
          if msvcrt.kbhit():
            char = msvcrt.getch()
            if char.lower() == b'c':
              pausa = False
              mostrarTabla = False
              break
          
          if mostrarTabla:
            #*Se imprime la tabla de pausa
            sys.stdout.write('\033[H')
            sys.stdout.write(tabulate(getTablaPausa(procesosTerminados, procesosNuevos, procesosListos, procesosBloqueados, procesoEjecutar, contadorGlobal)[:], headers=columnasPausa, tablefmt='fancy_grid'))
            sys.stdout.flush()
            time.sleep(0.1)

      #*Muestra la tabla
      linea = getTablaEjecucion(procesosListos, procesosBloqueados, procesosNuevos, procesosTerminados, procesoEjecutar, contadorGlobal, quantum)
      sys.stdout.write('\033[H')
      sys.stdout.write(tabulate([linea], headers=columnasEjecucion, tablefmt='fancy_grid'))
      sys.stdout.flush()
      time.sleep(1)

    #*Al terminar el quantum, comprueba si el proceso termino
    if procesoEjecutar is not None and procesoEjecutar["tiempoRestante"] == 0:
      if procesoEjecutar["error"]:
        procesosTerminados.append(procesoEjecutar)
      else:
        if procesoEjecutar["operacion"] == 1:
          procesoEjecutar["resultado"] = suma(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
        elif procesoEjecutar["operacion"] == 2:
          procesoEjecutar["resultado"] = resta(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
        elif procesoEjecutar["operacion"] == 3:
          procesoEjecutar["resultado"] = multiplicacion(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
        elif procesoEjecutar["operacion"] == 4:
          procesoEjecutar["resultado"] = division(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
        elif procesoEjecutar["operacion"] == 5:
          procesoEjecutar["resultado"] = modulo(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
        
        #*Obtiene los tiempos
        calculaTiempos(procesoEjecutar, contadorGlobal, 1)
        procesosTerminados.append(procesoEjecutar)
    elif procesoEjecutar["bloqueado"] == False:
      #*Si no termino, se reinicia el quantum y se envia a la cola de listos
      procesoEjecutar["quantum"] = quantum
      procesosListos.append(procesoEjecutar)

  #*Proceso termina
  # if procesoEjecutar is not None and procesoEjecutar["tiempoRestante"] == 0:
  #   if procesoEjecutar["error"]:
  #     procesosTerminados.append(procesoEjecutar)
  #   else:
  #     if procesoEjecutar["operacion"] == 1:
  #       procesoEjecutar["resultado"] = suma(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
  #     elif procesoEjecutar["operacion"] == 2:
  #       procesoEjecutar["resultado"] = resta(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
  #     elif procesoEjecutar["operacion"] == 3:
  #       procesoEjecutar["resultado"] = multiplicacion(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
  #     elif procesoEjecutar["operacion"] == 4:
  #       procesoEjecutar["resultado"] = division(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
  #     elif procesoEjecutar["operacion"] == 5:
  #       procesoEjecutar["resultado"] = modulo(procesoEjecutar["fNum"], procesoEjecutar["sNum"])
      
  #     #*Obtiene los tiempos
  #     calculaTiempos(procesoEjecutar, contadorGlobal, 1)
  #     procesosTerminados.append(procesoEjecutar)

#!Imprime la tabla final
os.system("cls")
sys.stdout.write('\033[H')
sys.stdout.write(tabulate(getTablaTerminado(procesosTerminados), headers=columnasTerminados, tablefmt='fancy_grid'))
sys.stdout.flush()