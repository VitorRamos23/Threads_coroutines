# 🍽️ Análise Comparativa do Problema dos Filósofos Jantando: Corrotinas vs. Threads

Este projeto em Python explora o Problema dos Filósofos Jantando (Dining Philosophers Problem), um problema clássico de concorrência e sincronização em ciência da computação, utilizando e comparando duas abordagens de concorrência em Python: Threads (programação preemptiva) e Corrotinas com asyncio (programação cooperativa).

O objetivo principal é demonstrar a ocorrência de deadlock (impasse) e, em seguida, implementar soluções robustas para preveni-lo em ambos os modelos de concorrência.

## 💡 O Problema dos Filósofos Jantando

O problema, proposto por Edsger Dijkstra, ilustra os desafios de evitar deadlock e starvation em um sistema com recursos compartilhados.

Cinco filósofos estão sentados em uma mesa redonda, alternando entre pensar e comer. Para comer, cada filósofo precisa de dois hashis (recursos compartilhados): um à sua esquerda e um à sua direita. Eles pegam um hashi de cada vez.

Um deadlock ocorre quando todos os filósofos pegam simultaneamente o hashi à sua esquerda e esperam indefinidamente pelo hashi à sua direita, que está sendo segurado pelo vizinho. Isso cria uma dependência circular, impedindo que qualquer um deles comece a comer.

### Condições de Coffman para Deadlock

O deadlock é possível quando as quatro condições de Coffman são atendidas:

1. Exclusão Mútua: Os recursos (hashis) não podem ser compartilhados.

2. Posse e Espera (Hold and Wait): Cada filósofo segura um hashi e espera pelo outro.

3. Não Preempção: Um hashi não pode ser retirado à força; deve ser liberado voluntariamente.

4. Espera Circular: Existe uma cadeia circular de espera por recursos.

## 🛠️ Implementações e Soluções

O projeto contém quatro simulações principais, duas para cada modelo de concorrência:

| Arquivo                            | Modelo de Concorrência     | Cenário     | Mecanismos Utilizados                                                  |
|------------------------------------|-----------------------------|--------------|------------------------------------------------------------------------|
| `dining_philosophers_coroutines.py` | Corrotinas (asyncio)        | Deadlock     | `asyncio.Lock`                                                         |
| `dining_philosophers_coroutines.py` | Corrotinas (asyncio)        | Corrigido    | `asyncio.Semaphore (N-1)` e Ordem Hierárquica Assimétrica              |
| `dining_philosophers_threads.py`    | Threads (threading)         | Deadlock     | `threading.Lock`                                                       |
| `dining_philosophers_threads.py`    | Threads (threading)         | Corrigido    | `threading.Semaphore (N-1)` e Ordem Hierárquica Assimétrica            |

## Estratégias de Prevenção de Deadlock

As versões corrigidas utilizam uma combinação de duas estratégias clássicas para quebrar a condição de Espera Circular:

1. Semáforo Limitador (N-1): Um semáforo é usado para limitar o número de filósofos que podem tentar pegar hashis simultaneamente a N-1 (onde N é o número total de filósofos). Isso garante que sempre haverá um conjunto de hashis disponível, quebrando a espera circular.

2. Ordem Hierárquica Assimétrica: Filósofos com ID par pegam o garfo esquerdo e depois o direito, enquanto filósofos com ID ímpar pegam o garfo direito e depois o esquerdo. Essa assimetria impede que todos entrem em um estado de espera mútua.

## 📊 Comparação: Corrotinas vs. Threads

A principal diferença reside no modelo de concorrência e como o controle da execução é gerenciado:

| Característica     | Corrotinas (asyncio)                                       | Threads (threading)                                       |
|--------------------|-------------------------------------------------------------|------------------------------------------------------------|
| **Modelo**         | Cooperativo (requer `await` explícito para ceder)           | Preemptivo (SO decide quando alternar)                     |
| **Agendamento**    | Gerenciado pelo event loop do Python                        | Gerenciado pelo Sistema Operacional                        |
| **Overhead**       | Leve, baixo custo de troca de contexto                      | Mais pesado, maior custo de troca de contexto              |
| **Paralelismo Real** | Não (single-threaded, ideal para I/O-bound)                | Limitado pelo GIL (Global Interpreter Lock) em Python      |
| **Deadlock**       | Ocorre se a lógica de acesso a recursos for falha           | Ocorre se a lógica de acesso a recursos for falha          |

Ambas as abordagens são suscetíveis a deadlock se a lógica de acesso a recursos for falha, e ambas requerem as mesmas estratégias de prevenção para garantir a segurança do recurso.

## 🚀 Como Executar

O projeto requer apenas o Python 3.x.

1. Threads (dining_philosophers_threads.py)

Este arquivo executa uma simulação de 5 segundos da versão com deadlock e, em seguida, uma simulação de 10 segundos da versão corrigida

```python3 dining_philosophers_threads.py```


2. Corrotinas (dining_philosophers_coroutines.py)

Este arquivo executa uma simulação de 5 segundos da versão com deadlock e, em seguida, uma simulação de 10 segundos da versão corrigida.

```python3 dining_philosophers_coroutines.py```

###### Referências 
- [The Little Book of Semaphores](https://greenteapress.com/semaphores/LittleBookOfSemaphores.pdf)
