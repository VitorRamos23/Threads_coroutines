import threading
import time
import random

NUM_PHILOSOPHERS = 5

class Philosopher(threading.Thread):
    def __init__(self, id, left_fork, right_fork, strategy=None, semaphore=None):
        super().__init__()
        self.id = id
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.eating_count = 0
        self._running = True
        self.strategy = strategy
        self.semaphore = semaphore

    def run(self):
        while self._running:
            self.think()
            if self.strategy == 'deadlock':
                self.dine_deadlock()
            elif self.strategy == 'corrected':
                self.dine_corrected(self.semaphore)

    def think(self):
        print(f"Filosofo {self.id} esta pensando.")
        time.sleep(random.uniform(0.1, 0.5))

    def eat(self):
        print(f"Filosofo {self.id} esta comendo ({self.eating_count + 1}).")
        time.sleep(random.uniform(0.1, 0.5))
        self.eating_count += 1

    def dine_deadlock(self):
        print(f"Filosofo {self.id} tentando pegar garfo ESQUERDO.")
        self.left_fork.acquire()
        print(f"Filosofo {self.id} pegou garfo ESQUERDO. Tentando pegar garfo DIREITO.")
        time.sleep(0.01) # Simula um pequeno atraso que pode exacerbar o deadlock
        self.right_fork.acquire()
        print(f"Filosofo {self.id} pegou garfo DIREITO.")
        self.eat()
        print(f"Filosofo {self.id} terminou de comer. Soltando garfos.")
        self.right_fork.release()
        self.left_fork.release()

    def dine_corrected(self, semaphore):
        with semaphore: 
            if self.id % 2 == 0: 
                print(f"Filosofo {self.id} (par) tentando pegar garfo ESQUERDO.")
                with self.left_fork: # Usando 'with'
                    print(f"Filosofo {self.id} (par) pegou garfo ESQUERDO. Tentando pegar garfo DIREITO.")
                    with self.right_fork: # Usando 'with'
                        print(f"Filosofo {self.id} (par) pegou garfo DIREITO.")
                        self.eat()
                        print(f"Filosofo {self.id} (par) terminou de comer. Soltando garfos.")
            else: 
                print(f"Filosofo {self.id} (impar) tentando pegar garfo DIREITO.")
                with self.right_fork: # Usando 'with'
                    print(f"Filosofo {self.id} (impar) pegou garfo DIREITO. Tentando pegar garfo ESQUERDO.")
                    with self.left_fork: # Usando 'with'
                        print(f"Filosofo {self.id} (impar) pegou garfo ESQUERDO.")
                        self.eat()
                        print(f"Filosofo {self.id} (impar) terminou de comer. Soltando garfos.")

    def stop(self):
        self._running = False

def run_deadlock_threads():
    forks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]
    philosophers = [
        Philosopher(i, forks[i], forks[(i + 1) % NUM_PHILOSOPHERS], strategy='deadlock')
        for i in range(NUM_PHILOSOPHERS)
    ]

    for p in philosophers:
        p.start()

    time.sleep(5) # Rodar por 5 segundos para observar o deadlock
    for p in philosophers:
        p.stop()
        p.join(timeout=1) # Tenta parar as threads

def run_corrected_threads():
    forks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]
    # Solução N-1: Permite que no máximo N-1 filosofos tentem pegar garfos ao mesmo tempo
    semaphore = threading.Semaphore(NUM_PHILOSOPHERS - 1)

    philosophers = [
        Philosopher(i, forks[i], forks[(i + 1) % NUM_PHILOSOPHERS], strategy='corrected', semaphore=semaphore)
        for i in range(NUM_PHILOSOPHERS)
    ]

    for p in philosophers:
        p.start()

    time.sleep(10) # Rodar por 10 segundos
    for p in philosophers:
        p.stop()
        p.join(timeout=1) # Tenta parar as threads

if __name__ == "__main__":
    print("\n--- Executando versão com deadlock (threads) ---")
    run_deadlock_threads()
    print("\nDeadlock provavelmente ocorreu ou a simulação atingiu o tempo limite.")

    print("\n--- Executando versão corrigida (threads) ---")
    run_corrected_threads()

    print("\n--- Fim da simulação de threads ---")