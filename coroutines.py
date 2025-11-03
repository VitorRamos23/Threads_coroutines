import asyncio
import random
import time

NUM_PHILOSOPHERS = 5

class Philosopher:
    def __init__(self, id, left_fork, right_fork):
        self.id = id
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.eating_count = 0

    async def think(self):
        await asyncio.sleep(random.uniform(0.1, 0.5))

    async def eat(self):
        await asyncio.sleep(random.uniform(0.1, 0.5))
        self.eating_count += 1

    async def dine_deadlock(self):
        while True:
            await self.think()
            async with self.left_fork:
                await asyncio.sleep(0.01) 
                async with self.right_fork:
                    await self.eat()
            
    async def dine_corrected(self, semaphore):
        while True:
            await self.think()
            async with semaphore:
                if self.id % 2 == 0: 
                    async with self.left_fork:
                        async with self.right_fork:
                            await self.eat()
                else: 
                    async with self.right_fork:
                        async with self.left_fork:
                            await self.eat()

async def run_simulation(strategy, timeout_s):
    forks = [asyncio.Lock() for _ in range(NUM_PHILOSOPHERS)]
    
    # Prepara os filósofos
    if strategy == 'deadlock':
        philosophers = [
            Philosopher(i, forks[i], forks[(i + 1) % NUM_PHILOSOPHERS])
            for i in range(NUM_PHILOSOPHERS)
        ]
        tasks = [asyncio.create_task(p.dine_deadlock()) for p in philosophers]
    else: 
        semaphore = asyncio.Semaphore(NUM_PHILOSOPHERS - 1)
        philosophers = [
            Philosopher(i, forks[i], forks[(i + 1) % NUM_PHILOSOPHERS])
            for i in range(NUM_PHILOSOPHERS)
        ]
        tasks = [asyncio.create_task(p.dine_corrected(semaphore)) for p in philosophers]

    start_time = time.time()
    try:
        # Roda a simulação pelo tempo limite
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=timeout_s)
    except asyncio.TimeoutError:
        # Timeout esperado
        pass
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        # Cancela todas as tarefas para garantir a parada
        for task in tasks:
            task.cancel()
        
        # Espera que as tarefas cancelem
        await asyncio.gather(*tasks, return_exceptions=True)

    end_time = time.time()
    
    # Coleta as métricas
    elapsed_time = end_time - start_time
    eating_counts = [p.eating_count for p in philosophers]

    # Retorna o tempo total e a contagem de refeições de cada filósofo
    return elapsed_time, eating_counts

def save_to_csv(filename, strategy, elapsed_time, eating_counts):
    import csv
    
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

async def main_all(timeout_deadlock=5, timeout_corrected=10):
    filename = 'results/coroutines_metrics.csv'
    
    print(f"\n--- Executando Deadlock (Timeout: {timeout_deadlock}s) ---")
    elapsed_time, eating_counts = await run_simulation('deadlock', timeout_deadlock)
    print(f"Tempo: {elapsed_time:.4f}s. Refeições (Total: {sum(eating_counts)}): {eating_counts}")
    save_to_csv(filename, 'deadlock', elapsed_time, eating_counts)

    print(f"\n--- Executando Corrigida (Timeout: {timeout_corrected}s) ---")
    elapsed_time, eating_counts = await run_simulation('corrected', timeout_corrected)
    print(f"Tempo: {elapsed_time:.4f}s. Refeições (Total: {sum(eating_counts)}): {eating_counts}")
    save_to_csv(filename, 'corrected', elapsed_time, eating_counts)

    print(f"\n--- Fim da Simulação de Corrotinas. Dados salvos em {filename} ---")

if __name__ == "__main__":
    # Garante que o diretório de resultados exista
    import os
    os.makedirs('results', exist_ok=True)
    asyncio.run(main_all())