import threading
import time
import queue
import random

class Surtidor():
    def __init__(self,tempo,cantidad,repos,caja,colacoches) :
        self.tiempo = tempo
        self.cantidad = cantidad
        self.tiemporepos = repos
        self.caja = caja
        self.cola = colacoches

tempo = int(input("introduzca el timepo que tardan en llegar los coches"))
cantidad = int(input("introduzca la cantidad de surtidores disponibles"))
timepopago = 3 

colacoches = queue.Queue(maxsize=0)

class Coche():
    def __init__(self):
        self.nombre = str(random.randint(0,9999))

#crear una funcion que genere 50 coches 

def generador():
    for i in range(50):
        coche = Coche()
        colacoches.put(coche)
        print("coche ",coche.nombre," llego a la cola")
        time.sleep(random.randint(0,tempo))
generador()
print(colacoches)
#que los coches se agreguen a la colacoches en un periodo de timepo random entre 0 y tempo



        