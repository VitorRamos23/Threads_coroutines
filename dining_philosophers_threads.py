import threading
import time
import random
import csv
import os

NUM_PHILOSOPHERS = 5

class Philosopher(threading.Thread):
    def __init__(self, id, left_fork, right_fork, strategy, semaphore=None):
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
                # A thread pode ficar BLOQUEADA aqui, impedindo a saída do loop
                if self._running:
                     self.dine_deadlock()
            elif self.strategy == 'corrected':
                if self._running:
                    self.dine_corrected(self.semaphore)

    def think(self):
        time.sleep(random.uniform(0.1, 0.5))

    def eat(self):
        time.sleep(random.uniform(0.1, 0.5))
        self.eating_count += 1

    def dine_deadlock(self):
        if not self._running: return # Checagem extra antes de adquirir o primeiro recurso
        self.left_fork.acquire()
        
        try:
            time.sleep(0.01) # Simula um pequeno atraso que pode exacerbar o deadlock
            
            if not self._running: return # Checagem extra antes de adquirir o segundo recurso
            self.right_fork.acquire()
            
            try:
                self.eat()
            finally:
                self.right_fork.release()
        finally:
            self.left_fork.release()

    def dine_corrected(self, semaphore):
        if not self._running: return 
        with semaphore: 
            if not self._running: return 
            if self.id % 2 == 0: 
                with self.left_fork: 
                    with self.right_fork:
                        self.eat()
            else: 
                with self.right_fork: 
                    with self.left_fork:
                        self.eat()

    def stop(self):
        self._running = False

def save_to_csv(filename, strategy, elapsed_time, eating_counts):
    
    # Se o arquivo não existe, escreve o cabeçalho
    try:
        with open(filename, 'r') as f:
            first_row = next(csv.reader(f))
            if first_row[0] != 'Estrategia':
                raise FileNotFoundError
    except (FileNotFoundError, StopIteration):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            header = ['Estrategia', 'Tempo_Total_s'] + [f'Filosofo_{i}_Refeicoes' for i in range(NUM_PHILOSOPHERS)]
            writer.writerow(header)

    # Escreve a linha de dados
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        row = [strategy, f'{elapsed_time:.4f}'] + eating_counts
        writer.writerow(row)

def run_simulation(strategy, timeout_s):
    forks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]
    semaphore = threading.Semaphore(NUM_PHILOSOPHERS - 1) if strategy == 'corrected' else None
    
    philosophers = [
        Philosopher(i, forks[i], forks[(i + 1) % NUM_PHILOSOPHERS], strategy=strategy, semaphore=semaphore)
        for i in range(NUM_PHILOSOPHERS)
    ]

    start_time = time.time()
    for p in philosophers:
        p.start()

    time.sleep(timeout_s) # Roda pelo tempo limite

    # Tenta parar as threads
    for p in philosophers:
        p.stop()
    
    # Faz join nas threads, mas a thread em deadlock pode não parar
    for p in philosophers:
        p.join(timeout=1) 

    end_time = time.time()

    elapsed_time = end_time - start_time
    eating_counts = [p.eating_count for p in philosophers]
    
    return elapsed_time, eating_counts

def main_all(timeout_deadlock=5, timeout_corrected=10):
    # Garante que o diretório de resultados exista
    os.makedirs('results', exist_ok=True)
    filename = 'results/threads_metrics.csv'

    print(f"\n--- Executando Deadlock (Timeout: {timeout_deadlock}s) ---")
    elapsed_time, eating_counts = run_simulation('deadlock', timeout_deadlock)
    print(f"Tempo: {elapsed_time:.4f}s. Refeições (Total: {sum(eating_counts)}): {eating_counts}")
    save_to_csv(filename, 'deadlock', elapsed_time, eating_counts)
    
    print(f"\n--- Executando Corrigida (Timeout: {timeout_corrected}s) ---")
    elapsed_time, eating_counts = run_simulation('corrected', timeout_corrected)
    print(f"Tempo: {elapsed_time:.4f}s. Refeições (Total: {sum(eating_counts)}): {eating_counts}")
    save_to_csv(filename, 'corrected', elapsed_time, eating_counts)

    print(f"\n--- Fim da Simulação de Threads. Dados salvos em {filename} ---")


if __name__ == "__main__":
    main_all()