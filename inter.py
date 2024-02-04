from msvcrt import getch

while(True):
    char = getch()
    if(char == b'q'):
        print("Termina programa")
        break
    if(char == b'e'):
        print("Interrupcion")
        
    if(char == b'w'):
        print("Error")
        
    if(char == b'p'):
        print("pausa")
        
    if(char == b'c'):
        print("Continuar")