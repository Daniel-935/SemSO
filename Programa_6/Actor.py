
class Actor:
    def __init__(self) -> None:
        self.indice = 0
        self.dormido = False
        self.consume = 0
        self.produce = 0
    
    def getIndice(self):
        return self.indice
    
    def increaseInd(self):
        self.indice += 1
    
    def getIndxCircular(self, t: int):
        return (self.indice % t)
    
    def getNextIndx(self, t: int):
        return (self.indice + 1) % t

    #*Si esta dormido o no
    def getEstado(self):
        return self.dormido
    
    def setEstado(self, e: bool):
        self.dormido = e

    def getConsume(self):
        return self.consume
    
    def setConsume(self, c: int):
        self.consume = c

    def getProduce(self):
        return self.produce
    
    def setProduce(self, p: int):
        self.produce = p
