import random

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

#*Recibe el numero de procesos total
def getId(p: int):
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

#*Genera las operaciones con dos numeros aleatorios
#?Primero genera los numeros y despues valida las operaciones
def generarOperaciones(p: int):
  operaciones = []
  for i in range(0, p):
    a, b = random.randint(1, 1000), random.randint(1, 1000)
    operacion = random.randint(1, 5)
    if b == 0 and (operacion == 5 or operacion == 4):
      operacion = 1

    #*Crea el string de operacion
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
      "operacionStr": operacionStr,
    })
  return operaciones