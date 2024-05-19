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
    if quantum < 5 or quantum >= 18:
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
columnasEjecucion = ["Datos Generales:", "Proceso\nejecutando:", "Procesos\nbloqueados", "Procesos\nterminados:"]
columnasTerminados = ["ID", "Operacion", "Datos", "Resultado", "Tiempos"]
columnasPausa = ["ID", "Estado", "Operacion", "Datos", "Resultado", "Tiempos"]

procesosNuevos = []
procesosListos = []
procesosBloqueados = []
procesosTerminados = []
memoria = [{"total": 0, "char": '', 'idProceso': 0} for i in range(46)]
# *Asignamos los 5 frames al OS
for i in range(5):
  memoria[i]["char"] = "!"
  memoria[i]["total"] = 1
contadorGlobal = 0
global mostrarTabla
global pausa
mostrarTabla = False
pausa = False
# *Para tener un control de los suspendidos y que el ciclo no termine
suspendidosEmpty = False

procesosNuevos = generaProcesos(numProcesos, quantum)[:]

#*Agrega los procesos nuevos a listos (maximo 4)

for i in range(len(procesosNuevos)):
  # *Calcula el total de frames que necesita el proceso
  proceso = procesosNuevos[0]
  paginas, porcentaje = getNumPaginas(proceso["size"])
  totalFrames = paginas + 1 if porcentaje > 0 else paginas

  # *Hay espacio en memoria para el proceso?
  if getMemSpaces(memoria) >= totalFrames:
    while paginas > 0 or porcentaje > 0:
      for frame in memoria:
        if frame["char"] == '':
          frame["char"] = proceso["estado"]
          frame["idProceso"] = proceso["id"]
          if paginas > 0:
            frame["total"] = 1
            paginas -= 1
          elif porcentaje > 0:
            frame["total"] = porcentaje
            porcentaje = 0
          break
    # *Despues de agregarse a los listos, se le asigna el tiempo de llegada y se elimina de la lista de nuevos
    proceso["tiempoLlegada"] = contadorGlobal
    procesosListos.append(proceso)
    procesosNuevos.pop(0)
  else:
    # *Llegar a este punto es que no hay mas espacio en memoria, truena el ciclo
    break

#!Bucle principal, mientras haya listos, bloquados, nuevos o suspendidos
while len(procesosListos) > 0 or len(procesosBloqueados) > 0 or len(procesosNuevos) > 0 or not suspendidosEmpty:
  
  # *Primero comprueba si hay por lo menos un suspendido, de lo contrario no se levanta la bandera
  suspendedido = getNextSuspendido()
  if not suspendedido:
    print("Hay un suspendido")
    suspendidosEmpty = True
  else:
    suspendidosEmpty = False

  #*Toma el primer proceso de la lista de listos
  if len(procesosListos) > 0:
    procesoEjecutar = procesosListos.pop(0)
    # *Se actualiza el estado
    cambiaEstado(procesoEjecutar["id"], '$', memoria)

  #*Comprueba si hay espacio libre en la memoria principal
  #*Primero toma el proceso, si hay espacio lo saca de nuevos
  if len(procesosNuevos) > 0:
    newListo = procesosNuevos[0]
    paginas, porcentaje = getNumPaginas(newListo["size"])
    totalFrames = paginas + 1 if porcentaje > 0 else paginas
    if getMemSpaces(memoria) >= totalFrames:
      while paginas > 0 or porcentaje > 0:
        for frame in memoria:
          if frame["char"] == '':
            frame["char"] = newListo["estado"]
            frame["idProceso"] = newListo["id"]
            if paginas > 0:
              frame["total"] = 1
              paginas -= 1
            elif porcentaje > 0:
              frame["total"] = porcentaje
              porcentaje = 0
            break
      # *Despues de agregarse a los listos, se le asigna el tiempo de llegada y se elimina de la lista de nuevos
      newListo["tiempoLlegada"] = contadorGlobal
      procesosListos.append(newListo)
      procesosNuevos.pop(0)

  #!Ejecuta el proceso de acuerdo al quantum
  if procesoEjecutar["tiempoRestante"] > 0 and procesoEjecutar is not None:
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

            # *Se actualiza el estado
            cambiaEstado(proceso["id"], '*', memoria)
            procesosListos.append(procesosBloqueados.pop(0))

      #?Funciones en caso de presionar una tecla
      if msvcrt.kbhit():
        char = msvcrt.getch()
        # *En este caso, como siempre se muestra la memoria la T solo es otra pausa mas
        if char.lower() == b'p' or char.lower() == b't':
          pausa = True
        elif char.lower() == b'e':
          if procesoEjecutar["tiempoRestante"] > 0:
            #*Se reinicia el quantum ya que sera enviado a la cola de listos otra vez
            procesoEjecutar["bloqueado"] = True
            procesoEjecutar["quantum"] = quantum

            # *Se actualiza el estado
            cambiaEstado(procesoEjecutar["id"], '#', memoria)
            procesosBloqueados.append(procesoEjecutar)
            break
        elif char.lower() == b'w':
          procesoEjecutar["tiempoRestante"] = 0
          procesoEjecutar["error"] = True
          # *Libera el espacio de memoria
          liberaMemoria(procesoEjecutar["id"], memoria)
          calculaTiempos(procesoEjecutar, contadorGlobal, 1)
          break
        elif char.lower() == b'n':
          #*Crea un nuevo proceso
          nuevoProceso = generaProceso(quantum)
          #*Comprueba si hay espacio en la memoria principal
          paginas, porcentaje = getNumPaginas(nuevoProceso["size"])
          totalFrames = paginas + 1 if porcentaje > 0 else paginas
          if getMemSpaces(memoria) >= totalFrames:
            while paginas > 0 or porcentaje > 0:
              for frame in memoria:
                if frame["char"] == '':
                  frame["char"] = nuevoProceso["estado"]
                  frame["idProceso"] = nuevoProceso["id"]
                  if paginas > 0:
                    frame["total"] = 1
                    paginas -= 1
                  elif porcentaje > 0:
                    frame["total"] = porcentaje
                    porcentaje = 0
                  break
            # *Despues de agregarse a los listos, se le asigna el tiempo de llegada y se elimina de la lista de nuevos
            nuevoProceso["tiempoLlegada"] = contadorGlobal
            procesosListos.append(nuevoProceso)
          else:
            procesosNuevos.append(generaProceso(quantum))
        elif char.lower() == b'b':
          pausa = True
          mostrarTabla = True
        elif char.lower() == b's':
          # *Si hay procesos en la cola de bloqueados
          if len(procesosBloqueados) > 0:
            procesoBloq = procesosBloqueados.pop(0)
            procesoBloq["bloqueado"] = False
            procesoBloq["timeOut"] = 0
            procesoBloq['estado'] = '*'
            # *Libera memoria
            liberaMemoria(procesoBloq["id"], memoria)

            # *se guarda en el archivo
            saveProceso(procesoBloq)
        elif char.lower() == b'r':
          # *Sacamos el proceso de suspendidos y se manda a listos si es que hay espacio en memoria
          nextSusp = getNextSuspendido()
          if nextSusp:
            # *Se comprueba si hay espacio en memoria
            paginas, porcentaje = getNumPaginas(nextSusp["size"])
            totalFrames = paginas + 1 if porcentaje > 0 else paginas
            if getMemSpaces(memoria) >= totalFrames:
              # *Saca el proceso de suspendidos y lo manda a listos
              nextSusp = takeNext()
              while paginas > 0 or porcentaje > 0:
                for frame in memoria:
                  if frame["char"] == '':
                    frame["char"] = nextSusp["estado"]
                    frame["idProceso"] = nextSusp["id"]
                    if paginas > 0:
                      frame["total"] = 1
                      paginas -= 1
                    elif porcentaje > 0:
                      frame["total"] = porcentaje
                      porcentaje = 0
                    break
              procesosListos.append(nextSusp)

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
            imprimir_tabla(memoria)

            #*Se imprime la tabla de pausa
            sys.stdout.write('\033[H')
            sys.stdout.write(tabulate(getTablaPausa(procesosTerminados, procesosNuevos, procesosListos, procesosBloqueados, procesoEjecutar, contadorGlobal)[:], headers=columnasPausa, tablefmt='fancy_grid'))
            sys.stdout.flush()
            time.sleep(0.1)

      os.system("cls")
      #*Muestra la memoria principal
      imprimir_tabla(memoria)

      #*Muestra la tabla
      linea = getTablaEjecucion(procesosBloqueados, procesosNuevos, procesosTerminados, procesoEjecutar, contadorGlobal, quantum)
      sys.stdout.write(tabulate([linea], headers=columnasEjecucion, tablefmt='fancy_grid'))
      sys.stdout.write('\033[H')
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
        # *Libera espacio de memoria
        liberaMemoria(procesoEjecutar["id"], memoria)

        procesosTerminados.append(procesoEjecutar)
    elif procesoEjecutar["bloqueado"] == False:
      #*Si no termino, se reinicia el quantum y se envia a la cola de listos
      procesoEjecutar["quantum"] = quantum
      # *Se actualiza el estado
      cambiaEstado(procesoEjecutar["id"], '*', memoria)
      procesosListos.append(procesoEjecutar)

  # !Si no hay proceso en ejecucion solo avanzan si hay bloqueados y el contador global
  else:
    contadorGlobal += 1
    if len(procesosBloqueados) > 0:
        for proceso in procesosBloqueados:
          proceso["timeOut"] += 1
          #*En caso de que se termine el tiempo de bloqueo
          if proceso["timeOut"] == 8:
            proceso["bloqueado"] = False
            # *Se actualiza el estado
            cambiaEstado(proceso["id"], '*', memoria)
            procesosListos.append(procesosBloqueados.pop(0))

    #?Funciones en caso de presionar una tecla
    if msvcrt.kbhit():
      char = msvcrt.getch()
      # *En este caso, como siempre se muestra la memoria la T solo es otra pausa mas
      if char.lower() == b'p' or char.lower() == b't':
        pausa = True
      elif char.lower() == b'n':
        #*Crea un nuevo proceso
        nuevoProceso = generaProceso(quantum)
        #*Comprueba si hay espacio en la memoria principal
        paginas, porcentaje = getNumPaginas(nuevoProceso["size"])
        totalFrames = paginas + 1 if porcentaje > 0 else paginas
        if getMemSpaces(memoria) >= totalFrames:
          while paginas > 0 or porcentaje > 0:
            for frame in memoria:
              if frame["char"] == '':
                frame["char"] = nuevoProceso["estado"]
                frame["idProceso"] = nuevoProceso["id"]
                if paginas > 0:
                  frame["total"] = 1
                  paginas -= 1
                elif porcentaje > 0:
                  frame["total"] = porcentaje
                  porcentaje = 0
                break
          # *Despues de agregarse a los listos, se le asigna el tiempo de llegada y se elimina de la lista de nuevos
          nuevoProceso["tiempoLlegada"] = contadorGlobal
          procesosListos.append(nuevoProceso)
        else:
          procesosNuevos.append(generaProceso(quantum))
      elif char.lower() == b'b':
        pausa = True
        mostrarTabla = True
      elif char.lower() == b's':
        # *Si hay procesos en la cola de bloqueados
        if len(procesosBloqueados) > 0:
          procesoBloq = procesosBloqueados.pop(0)
          procesoBloq["bloqueado"] = False
          procesoBloq["timeOut"] = 0
          procesoBloq['estado'] = '*'
          # *Libera memoria
          liberaMemoria(procesoBloq["id"], memoria)

          # *Se actualiza el estado y se guarda en el archivo
          cambiaEstado(procesoBloq["id"], '*', memoria)
          saveProceso(procesoBloq)
      elif char.lower() == b'r':
        # *Sacamos el proceso de suspendidos y se manda a listos si es que hay espacio en memoria
        nextSusp = getNextSuspendido()
        if nextSusp:
          # *Se comprueba si hay espacio en memoria
          paginas, porcentaje = getNumPaginas(nextSusp["size"])
          totalFrames = paginas + 1 if porcentaje > 0 else paginas
          if getMemSpaces(memoria) >= totalFrames:
            # *Saca el proceso de suspendidos y lo manda a listos
            nextSusp = takeNext()
            while paginas > 0 or porcentaje > 0:
              for frame in memoria:
                if frame["char"] == '':
                  frame["char"] = nextSusp["estado"]
                  frame["idProceso"] = nextSusp["id"]
                  if paginas > 0:
                    frame["total"] = 1
                    paginas -= 1
                  elif porcentaje > 0:
                    frame["total"] = porcentaje
                    porcentaje = 0
                  break
            procesosListos.append(nextSusp)
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
          imprimir_tabla(memoria)

          #*Se imprime la tabla de pausa
          sys.stdout.write('\033[H')
          sys.stdout.write(tabulate(getTablaPausa(procesosTerminados, procesosNuevos, procesosListos, procesosBloqueados, procesoEjecutar, contadorGlobal)[:], headers=columnasPausa, tablefmt='fancy_grid'))
          sys.stdout.flush()
          time.sleep(0.1)

    os.system("cls")
    #*Muestra la memoria principal
    imprimir_tabla(memoria)

    #*Muestra la tabla
    linea = getTablaEjecucion(procesosBloqueados, procesosNuevos, procesosTerminados, None, contadorGlobal, quantum)
    sys.stdout.write(tabulate([linea], headers=columnasEjecucion, tablefmt='fancy_grid'))
    sys.stdout.write('\033[H')
    time.sleep(1)
    

#!Imprime la tabla final y elimina el archivo de suspendidos
os.system("cls")
sys.stdout.write('\033[H')
sys.stdout.write(tabulate(getTablaTerminado(procesosTerminados), headers=columnasTerminados, tablefmt='fancy_grid'))
sys.stdout.flush()
if os.path.exists("suspendidos.json"):
  os.remove("suspendidos.json")