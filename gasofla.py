import threading
import queue
import time
import random


class Coche:
    def __init__(self, nombre):
        self.nombre = nombre


class Surtidor:
    def __init__(self, numero):
        self.numero = numero
        self.caja = True
        self.cola = queue.Queue()

    def agregar_a_cola(self, coche):
        self.cola.put(coche)
        print(f"{coche.nombre} ha llegado a la gasolinera y está esperando su turno en la cola del surtidor {self.numero}.")

    def repostar(self):
        while True:
            if not self.cola.empty():
                coche = self.cola.get()
                print(f"El surtidor {self.numero} está repostando el coche {coche.nombre}.")
                time.sleep(random.uniform(0.5, 1))
                print(f"El coche {coche.nombre} ha terminado de repostar en el surtidor {self.numero}.")
            else:
                time.sleep(1)

    def pagar(self):
        caja = queue.Queue()
        while True:
            if not self.cola.empty():
                coche = self.cola.queue[0]
                if self.caja and caja.empty():
                    self.caja = False
                    print(f"El coche {coche.nombre} ha pasado a la caja del surtidor {self.numero}.")
                    caja.put(self.cola.get())
                    time.sleep(0.3)
                    self.caja = True
                    print(f"El coche {coche.nombre} ha pagado en la caja del surtidor {self.numero}.")
                else:
                    time.sleep(1)
            else:
                time.sleep(1)


def agregar_coches_a_cola(surtidor, lista_coches):
    for coche in lista_coches:
        surtidor.agregar_a_cola(coche)
        time.sleep(random.randint(1, 3))

n = int(input("cuantos surtidores quieres que haya"))
surtidores = [Surtidor(i) for i in range(1, n)]
coches = [Coche(f"Coche {i+1}") for i in range(50)]

for surtidor in surtidores:
    threading.Thread(target=surtidor.repostar, daemon=True).start()
    threading.Thread(target=surtidor.pagar, daemon=True).start()

for surtidor in surtidores:
    threading.Thread(target=agregar_coches_a_cola, args=(surtidor, coches), daemon=True).start()

while True:
    pass
