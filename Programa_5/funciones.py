import random

#!Funciones para generar datos aleatorios
def getIds(p: int):
  ids = set()
  for i in range(0, p):
    id = random.randint(1000, 9999)
    #*Valida que sea unico y que no sea 0
    if id not in ids and id > 0:
      ids.add(id)
  return ids
  
def getTiempos(p: int):
  tiempos = []
  for i in range(0, p):
    tiempo = random.randint(5, 18)
    if tiempo > 0:
      tiempos.append(tiempo)
  return tiempos

def getOperaciones(p: int):
  operaciones = []
  for i in range(0, p):
    a,b = random.randint(1, 1000), random.randint(1, 1000)
    operacion = random.randint(1, 5)
    if b == 0 and (operacion == 5 or operacion == 4):
      #*Si la operacion invalida para los numeros, pone por defecto una suma
      operacion = 1

    if operacion == 1:
      operacionStr = "+"
    elif operacion == 2:
      operacionStr = "-"
    elif operacion == 3:
      operacionStr = "*"
    elif operacion == 4:
      operacionStr = "/"
    elif operacion == 5:
      operacionStr = "%"

    operaciones.append({
      "fNum": a,
      "sNum": b,
      "operacion": operacion,
      "operacionStr": operacionStr
    })
  return operaciones

def getNewTiempo():
  return random.randint(5, 18)

def getNewId():
  return random.randint(1000, 9999)

def getNewOperacion():
  operacion = random.randint(1, 5)
  a, b = random.randint(1, 1000), random.randint(1, 1000)
  if b == 0 and (operacion == 5 or operacion == 4):
    operacion = 1

  if operacion == 1:
    operacionStr = "+"
  elif operacion == 2:
    operacionStr = "-"
  elif operacion == 3:
    operacionStr = "*"
  elif operacion == 4:
    operacionStr = "/"
  elif operacion == 5:
    operacionStr = "%"

  return {
    "fNum": a,
    "sNum": b,
    "operacion": operacion,
    "operacionStr": operacionStr
  }

def generaProcesos(p: int, q: int):
  auxProcesos = []
  #*Genera copia de cada lista que obtiene
  ids = getIds(p)
  tiempos = getTiempos(p)[:]
  operaciones = getOperaciones(p)[:]
  for i in range(0, p):
    tiempo = tiempos.pop()
    operacion = operaciones.pop()
    auxProcesos.append({
      "id": ids.pop(),
      "tiempo": tiempo,
      "tiempoRestante": tiempo,
      "operacion": operacion["operacion"],
      "operacionStr": operacion["operacionStr"],
      "fNum": operacion["fNum"],
      "sNum": operacion["sNum"],
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
      "banderaRespuesta": False,
      "quantum": q,
      "bloqueado": False
    })
  return auxProcesos

def generaProceso(q: int):
  id = getNewId()
  tiempo = getNewTiempo()
  operacion = getNewOperacion()
  return {
    "id": id,
    "tiempo": tiempo,
    "tiempoRestante": tiempo,
    "operacion": operacion["operacion"],
    "operacionStr": operacion["operacionStr"],
    "fNum": operacion["fNum"],
    "sNum": operacion["sNum"],
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
    "banderaRespuesta": False,
    "quantum": q,
    "bloqueado": False
  }

#!Funciones para mostrar la tabla
def getTablaEjecucion(procesosListos: list, procesosBloqueados: list, procesosNuevos: list, procesosTerminados: list, procesoEjecutar: dict, contadorGlobal: int ,q: int):

  #*Creo la linea a mostrar en la tabla
  bloqueadosStr = ""
  terminadosStr = ""
  datosGenerales = f"Contador global: {contadorGlobal}\nProcesos nuevos: {len(procesosNuevos)}\nQuantum: {q}"
  listosStr = "\n".join([f"ID: {proceso['id']} | Tiempo estimado: {proceso['tiempoRestante']} | Tiempo transcurrido: {proceso["tiempoTrans"]}" for proceso in procesosListos])
  ejecutandoStr = f"ID: {procesoEjecutar['id']}\nOperacion: {procesoEjecutar["operacionStr"]}\nValores: {procesoEjecutar['fNum']} {procesoEjecutar['sNum']}\nTiempo transcurrido: {procesoEjecutar['tiempoTrans']}\nTiempo restante: {procesoEjecutar['tiempoRestante']}\nQuantum restante: {procesoEjecutar['quantum']}"

  if len(procesosBloqueados) > 0:
    bloqueadosStr = "\n".join([f"ID: {proceso['id']} | Tiempo restante: {8 - proceso['timeOut']}" for proceso in procesosBloqueados])

  if len(procesosTerminados) > 0:
    terminadosStr = "\n".join([f"ID: {proceso['id']} | Operacion: {proceso['operacionStr']}\nDatos: {proceso['fNum']} {proceso['sNum']} | {'Resultado: '+str(proceso['resultado']) if not proceso['error'] else 'Error'}\n" for proceso in procesosTerminados])

  return [datosGenerales, listosStr, ejecutandoStr, bloqueadosStr, terminadosStr]

def getTablaTerminado(procesosTerminados: list):
  tablaFinal = []
  for proceso in procesosTerminados:
    lineaTiempos = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: {proceso['tiempoFinalizacion']}\nTiempo retorno: {proceso['tiempoRetorno']}\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta']}\nTiempo servicio: {proceso['tiempoServicio']}"

    tablaFinal.append([proceso['id'], proceso['operacionStr'], f"{proceso['fNum']} {proceso['sNum']}", f"{proceso['resultado'] if not proceso['error'] else 'Error'}", lineaTiempos])

  return tablaFinal

def getTablaPausa(procesosTerminados: list, procesosNuevos: list, procesosListos: list, procesosBloqueados: list, procesoEjecutar, contadorGlobal):

  tablaPausa = []

  if len(procesosTerminados) > 0:
    for proceso in procesosTerminados:
      tiemposTerminado = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: {proceso['tiempoFinalizacion']}\nTiempo retorno: {proceso['tiempoRetorno']}\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta']}\nTiempo servicio: {proceso['tiempoServicio']}"
      tablaPausa.append([proceso["id"], "Terminado", proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", proceso["resultado"] if not proceso["error"] else "Error", tiemposTerminado])

  if len(procesosNuevos) > 0:
    for proceso in procesosNuevos:
      tablaPausa.append([proceso["id"], "Nuevo", proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", "No ha iniciado", "No ha iniciado"])

  #*Procesos listos
  if len(procesosListos) > 0:
    for proceso in procesosListos:
      calculaTiempos(proceso, contadorGlobal, 3)
      tiemposListo = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: No terminado\nTiempo retorno: No terminado\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta'] if not proceso['banderaRespuesta'] else "No ha iniciado"}\nTiempo servicio: {proceso['tiempoServicio']}\nTiempo restante CPU: {proceso['tiempoRestante']}"
      tablaPausa.append([proceso["id"], "Listo", proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", "No ha terminado", tiemposListo])

  #*Procesos bloqueados
  if len(procesosBloqueados) > 0:
    for proceso in procesosBloqueados:
      calculaTiempos(proceso, contadorGlobal, 2)
      tiemposBloqueado = f"Tiempo llegada: {proceso['tiempoLlegada']}\nTiempo finalizacion: No terminado\nTiempo retorno: No terminado\nTiempo espera: {proceso['tiempoEspera']}\nTiempo respuesta: {proceso['tiempoRespuesta'] if proceso['banderaRespuesta'] else 'No ha iniciado'}\nTiempo servicio: {proceso['tiempoServicio']}\nBloqueo restante: {7 - proceso['timeOut']}"
      tablaPausa.append([proceso["id"], "Bloqueado", proceso["operacionStr"], f"{proceso['fNum']} {proceso['sNum']}", "No ha terminado", tiemposBloqueado])

  if procesoEjecutar is not None:
    calculaTiempos(procesoEjecutar, contadorGlobal, 4)
    tiemposEjecutando = f"Tiempo llegada: {procesoEjecutar['tiempoLlegada']}\nTiempo finalizacion: No terminado\nTiempo retorno: No terminado\nTiempo espera: {procesoEjecutar['tiempoEspera']}\nTiempo respuesta: {procesoEjecutar['tiempoRespuesta']}\nTiempo servicio: {procesoEjecutar['tiempoServicio']}\nTiempo restante CPU: {procesoEjecutar['tiempoRestante']}"
    tablaPausa.append([procesoEjecutar["id"], "Ejecutando", procesoEjecutar["operacionStr"], f"{procesoEjecutar['fNum']} {procesoEjecutar['sNum']}", "No ha terminado", tiemposEjecutando])

  return tablaPausa

#!Funciones para obtener los tiempos
def calculaTiempos(proceso, contadorGlobal, tipo):
  #?1 = terminado, 2 = bloqueado, 3 = listo, 4 = ejecutando
  proceso["tiempoFinalizacion"] = contadorGlobal
  proceso["tiempoRetorno"] = proceso["tiempoFinalizacion"] - proceso["tiempoLlegada"]
  if proceso["error"] or tipo == 3 or tipo == 2 or tipo == 4:
    proceso["tiempoServicio"] = proceso["tiempoTrans"]
  else:
    proceso["tiempoServicio"] = proceso["tiempo"]
  if tipo == 3 or tipo == 2 or tipo == 4:
    proceso["tiempoEspera"] = contadorGlobal - proceso["tiempoLlegada"] - proceso["tiempoServicio"]
  else:
    proceso["tiempoEspera"] = proceso["tiempoRetorno"] - proceso["tiempoServicio"]


#!Funciones para las operaciones (resultados)
def suma(a: int, b: int):
  return a + b

def resta(a: int, b: int):
  return a - b

def multiplicacion(a: int, b: int):
  return a * b

def division(a: int, b: int):
  return a / b

def modulo(a: int, b: int):
  return a % b