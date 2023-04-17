import time
import random
from threading import Thread, Semaphore
from queue import Queue

class Coche:
    def __init__(self, nombre):
        self.nombre = nombre

class Surtidor:
    def __init__(self, numero, caja):
        self.numero = numero
        self.cola = Queue()
        self.caja = caja
        self.surtidor_libre = Semaphore(1)
        self.caja_libre = Semaphore(1)

class Gasolinera:
    def __init__(self, num_surtidores):
        self.surtidores = [Surtidor(i+1, Queue()) for i in range(num_surtidores)]
        self.cola_general = Queue()
        self.caja = Queue()

    def agregar_coches_a_cola(self, coches, intervalo_max):
        for coche in coches:
            tiempo_espera = random.randint(0, intervalo_max)
            time.sleep(tiempo_espera)
            self.cola_general.put(coche)

    def run(self):
        t1 = Thread(target=self.pasar_coches_a_surtidores)
        t2 = Thread(target=self.repostar)
        t3 = Thread(target=self.pagar)
        t1.start()
        t2.start()
        t3.start()

    def pasar_coches_a_surtidores(self):
        while True:
            coche = self.cola_general.get()
            surtidor_libre = None
            for surtidor in self.surtidores:
                if surtidor.surtidor_libre.acquire(blocking=False) and surtidor.cola.qsize() == 0:
                    surtidor_libre = surtidor
                    break

            if surtidor_libre is None:
                self.cola_general.put(coche)
            else:
                surtidor_libre.cola.put(coche)
                surtidor_libre.surtidor_libre.release()
                surtidor_libre.surtidor_libre.release()

    def repostar(self):
        while True:
            for surtidor in self.surtidores:
                if surtidor.cola.qsize() > 0:
                    if surtidor.surtidor_libre.acquire(blocking=False):
                        coche = surtidor.cola.get()
                        print(f"{coche.nombre} en surtidor {surtidor.numero}")
                        time.sleep(random.uniform(0.5, 1))
                        surtidor.surtidor_libre.release()
                        surtidor.caja.put(coche)

    def pagar(self):
        while True:
            if self.caja.qsize() > 0:
                if self.caja_libre.acquire(blocking=False):
                    coche = self.caja.get()
                    print(f"{coche.nombre} en caja")
                    time.sleep(0.3)
                    self.caja_libre.release()
    def iniciargasolinera():
        gasolinera = Gasolinera(3)
        coches = [Coche(f"Coche {i+1}") for i in range(50)]
        gasolinera.agregar_coches_a_cola(coches, 5)
        gasolinera.run()

Gasolinera.run(3)
