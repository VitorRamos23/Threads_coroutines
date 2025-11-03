# 💡 O Problema dos Filósofos Jantando

O problema, proposto por Edsger Dijkstra, ilustra os desafios de evitar deadlock e starvation em um sistema com recursos compartilhados.

Cinco filósofos estão sentados em uma mesa redonda, alternando entre pensar e comer. Para comer, cada filósofo precisa de dois hashis (recursos compartilhados): um à sua esquerda e um à sua direita. Eles pegam um hashi de cada vez. Nesse sentido, cada filósofo alterna entre duas tarefas: comer ou pensar. Quando um filósofo fica com fome, ele tenta pegar os garfos à sua esquerda e à sua direita, um de cada vez, independente da ordem. Caso ele consiga pegar dois garfos, ele come durante um determinado tempo e depois recoloca os garfos na mesa. Em seguida ele volta a pensar.


Por definição, o problema em questão é: 

  Você é capaz de propor um algoritmo que implemente cada filósofo de modo que ele execute as tarefas de comer e pensar sem nunca ficar travado?


## 🍽️ Análise Comparativa do Problema dos Filósofos Jantando: Corrotinas vs. Threads

Este projeto em Python explora o Problema dos Filósofos Jantando (Dining Philosophers Problem), um problema clássico de concorrência e sincronização em ciência da computação, utilizando e comparando duas abordagens de concorrência em Python: Threads (programação preemptiva) e Corrotinas com asyncio (programação cooperativa).

O objetivo principal é demonstrar a ocorrência de deadlock (impasse) e, em seguida, implementar soluções robustas para preveni-lo em ambos os modelos de concorrência.


## 🚀 Como Executar

O projeto requer apenas o Python 3.x.

Foi utilizado a ferramenta de execução [Vs Code](https://code.visualstudio.com/) com as devidas ferramentas necessarias para a execução do projeto.



1. Threads (threads.py)

Este arquivo executa uma simulação de 5 segundos da versão com deadlock e, em seguida, uma simulação de 10 segundos da versão corrigida

Comando para a execução do arquivo pelo terminal : ```python3 threads.py```


2. Corrotinas (coroutines.py)

Este arquivo executa uma simulação de 5 segundos da versão com deadlock e, em seguida, uma simulação de 10 segundos da versão corrigida.

Comando para a execução do arquivo pelo terminal :  ```python3 coroutines.py```

Obs : Pode ser utilizado o comando "F5" ou clicar na seta de execução caso não queira usar o terminal

## 🛠️ Implementações e Soluções

O projeto contém quatro simulações principais, duas para cada modelo de concorrência:

| Arquivo                            | Modelo de Concorrência     | Cenário     | Mecanismos Utilizados                                                  |
|------------------------------------|-----------------------------|--------------|------------------------------------------------------------------------|
| `coroutines.py` | Corrotinas (asyncio)        | Deadlock     | `asyncio.Lock`                                                         |
| `coroutines.py` | Corrotinas (asyncio)        | Corrigido    | `asyncio.Semaphore (N-1)` e Ordem Hierárquica Assimétrica              |
| `threads.py`    | Threads (threading)         | Deadlock     | `threading.Lock`                                                       |
| `threads.py`    | Threads (threading)         | Corrigido    | `threading.Semaphore (N-1)` e Ordem Hierárquica Assimétrica            |


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

### Mais informações e detalhes estão presentes no relatório do projeto [report.pdf](./threads.py)

###### Referências 
- [The Little Book of Semaphores](https://greenteapress.com/semaphores/LittleBookOfSemaphores.pdf)
