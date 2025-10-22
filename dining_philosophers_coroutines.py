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
        print(f"Filosofo {self.id} esta pensando.")
        await asyncio.sleep(random.uniform(0.1, 0.5))

    async def eat(self):
        print(f"Filosofo {self.id} esta comendo ({self.eating_count + 1}).")
        await asyncio.sleep(random.uniform(0.1, 0.5))
        self.eating_count += 1

    async def dine_deadlock(self):
        while True:
            await self.think()
            print(f"Filosofo {self.id} tentando pegar garfo ESQUERDO.")
            async with self.left_fork:
                print(f"Filosofo {self.id} pegou garfo ESQUERDO. Tentando pegar garfo DIREITO.")
                await asyncio.sleep(0.01) # Simula um pequeno atraso que pode exacerbar o deadlock
                async with self.right_fork:
                    print(f"Filosofo {self.id} pegou garfo DIREITO.")
                    await self.eat()
                    print(f"Filosofo {self.id} terminou de comer. Soltando garfos.")
            
    async def dine_corrected(self, semaphore):
        while True:
            await self.think()
            async with semaphore: # Limita o número de filosofos que podem tentar pegar garfos
                # Implementação da ordem hierárquica (garfo menor primeiro)
                if self.id % 2 == 0: # Filosofos pares pegam o garfo esquerdo primeiro
                    print(f"Filosofo {self.id} (par) tentando pegar garfo ESQUERDO.")
                    async with self.left_fork:
                        print(f"Filosofo {self.id} (par) pegou garfo ESQUERDO. Tentando pegar garfo DIREITO.")
                        async with self.right_fork:
                            print(f"Filosofo {self.id} (par) pegou garfo DIREITO.")
                            await self.eat()
                            print(f"Filosofo {self.id} (par) terminou de comer. Soltando garfos.")
                else: # Filosofos impares pegam o garfo direito primeiro
                    print(f"Filosofo {self.id} (impar) tentando pegar garfo DIREITO.")
                    async with self.right_fork:
                        print(f"Filosofo {self.id} (impar) pegou garfo DIREITO. Tentando pegar garfo ESQUERDO.")
                        async with self.left_fork:
                            print(f"Filosofo {self.id} (impar) pegou garfo ESQUERDO.")
                            await self.eat()
                            print(f"Filosofo {self.id} (impar) terminou de comer. Soltando garfos.")

async def main_deadlock():
    forks = [asyncio.Lock() for _ in range(NUM_PHILOSOPHERS)]
    philosophers = [
        Philosopher(i, forks[i], forks[(i + 1) % NUM_PHILOSOPHERS])
        for i in range(NUM_PHILOSOPHERS)
    ]

    tasks = [asyncio.create_task(p.dine_deadlock()) for p in philosophers]
    await asyncio.gather(*tasks)

async def main_corrected():
    forks = [asyncio.Lock() for _ in range(NUM_PHILOSOPHERS)]
    # Solução N-1: Permite que no máximo N-1 filosofos tentem pegar garfos ao mesmo tempo
    # Isso garante que sempre haverá um conjunto de garfos disponível para um filosofo
    semaphore = asyncio.Semaphore(NUM_PHILOSOPHERS - 1)

    philosophers = [
        Philosopher(i, forks[i], forks[(i + 1) % NUM_PHILOSOPHERS])
        for i in range(NUM_PHILOSOPHERS)
    ]

    tasks = [asyncio.create_task(p.dine_corrected(semaphore)) for p in philosophers]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("\n--- Executando versão com deadlock (corrotinas) ---")
    # Para observar o deadlock, pode ser necessário rodar por um tempo ou ajustar os sleeps
    # asyncio.run(main_deadlock())
    # Para demonstrar o deadlock, vamos rodar por um tempo limitado e ver se todos comem
    try:
        asyncio.run(asyncio.wait_for(main_deadlock(), timeout=5))
    except asyncio.TimeoutError:
        print("\nDeadlock provavelmente ocorreu ou a simulação atingiu o tempo limite.")
    
    print("\n--- Executando versão corrigida (corrotinas) ---")
    try:
        asyncio.run(asyncio.wait_for(main_corrected(), timeout=10))
    except asyncio.TimeoutError:
        print("\nSimulação corrigida atingiu o tempo limite.")

    print("\n--- Fim da simulação de corrotinas ---")

