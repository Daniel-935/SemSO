import os
import time
import sys
import msvcrt
from msvcrt import getch
import random
from colorama import Fore, Style

from Actor import Actor

#!Programa productor-consumidor

#*Contenedor con 22 espacios
#? _ = Espacio vacio, * = Espacio ocupado
buffer = ["_"] * 22
#! Codigo de la tecla ESC = b'\x1b'

productor = Actor()
consumidor = Actor()
termina = True

#? par = Productor, impar = Consumidor
def dormir():
  if random.randint(1, 100) % 2 == 0:
    return 0
  return 1

def consumeProduce():
  return random.randint(3, 6)

#*Comprueba si el espacio esta vacio
def isEmpty(ind: int):
  if buffer[ind] == "_":
    return True
  return False

while termina:

  productor.setEstado(False)
  consumidor.setEstado(False)
  #*Genera numero para saber a quien despertar
  if(dormir() == 0):
    productor.setEstado(True)
    os.system('cls')
    sys.stdout.write('\033[H')
    print(buffer)
    print(f"{Fore.CYAN}Productor{Style.RESET_ALL} intentando acceder al buffer")
    print(f"Consumidor dormido...")
    sys.stdout.flush()
    if msvcrt.kbhit():
      if getch() == b'\x1b':
        break
    time.sleep(1)
  else:
    consumidor.setEstado(True)
    os.system('cls')
    sys.stdout.write('\033[H')
    print(buffer)
    print(f"{Fore.RED}Consumidor{Style.RESET_ALL} intentando acceder al buffer")
    print(f"Productor dormido...")
    sys.stdout.flush()
    if msvcrt.kbhit():
      if getch() == b'\x1b':
        break
    time.sleep(1)

  
  if productor.getEstado() and isEmpty(productor.getIndxCircular(22)) and consumidor.getEstado() == False:
    num = consumeProduce()
    for i in range(0, num):
      buffer[productor.getIndxCircular(22)] = "*"
      #*Imprime los datos...
      sys.stdout.write('\033[H')
      print(buffer)
      print(f"{Fore.CYAN}Productor activo{Style.RESET_ALL}. Intentando generar {Fore.CYAN}{num}{Style.RESET_ALL} elementos")
      print(f"Consumidor dormido...")
      sys.stdout.flush()
      if msvcrt.kbhit():
        if getch() == b'\x1b':
          termina = False
          break
      time.sleep(1)

      #*Si se encuentra con un espacio ocupado, se detiene
      if not isEmpty(productor.getNextIndx(22)):
        break
      productor.increaseInd()
    productor.setEstado(False)
  elif consumidor.getEstado() and not isEmpty(consumidor.getIndxCircular(22)) and productor.getEstado() == False:
    num = consumeProduce()
    
    for i in range(0, num):
      buffer[consumidor.getIndxCircular(22)] = "_"
      
      sys.stdout.write('\033[H')
      print(buffer)
      print(f"{Fore.RED}Consumidor activo{Style.RESET_ALL}. Intentando consumir {Fore.RED}{num}{Style.RESET_ALL} elementos")
      print(f"Productor dormido...")
      sys.stdout.flush()
      if msvcrt.kbhit():
        if getch() == b'\x1b':
          termina = False
          break
      time.sleep(1)

      #*Si se encuentra con un espacio vacio, se detiene
      if isEmpty(consumidor.getNextIndx(22)):
        break
      consumidor.increaseInd()
    consumidor.setEstado(False)

  if msvcrt.kbhit():
    if getch() == b'\x1b':
      break

