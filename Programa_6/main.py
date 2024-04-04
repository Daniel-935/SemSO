import os
import time
import sys
import msvcrt

from Actor import Actor

#!Programa productor-consumidor

#*Contenedor con 22 espacios
#? _ = Espacio vacio, * = Espacio ocupado
buffer = ["_"] * 22
#! Codigo de la tecla ESC = b'\x1b'

prueba = [1, 2, 3, 4]
tam = len(prueba)

indice = 7
for i in range(0, 6):
  print(prueba[(indice + i) % tam])

