# Pesquisa sobre o Problema dos Filósofos Jantando

## Descrição do Problema

O Problema dos Filósofos Jantando é um problema clássico de sincronização em ciência da computação, proposto por Edsger Dijkstra. Ele ilustra os desafios de evitar *deadlock* e *starvation* em um sistema com recursos compartilhados.

Imagine cinco filósofos sentados em uma mesa redonda. Entre cada par de filósofos há um único hashi (ou garfo). Cada filósofo alterna entre pensar e comer. Para comer, um filósofo precisa de dois hashis: um à sua esquerda e um à sua direita. Eles pegam um hashi de cada vez.

## Condição de Deadlock

Um *deadlock* ocorre se todos os filósofos, simultaneamente, pegam o hashi à sua esquerda (ou à sua direita). Nesse cenário, cada filósofo está segurando um hashi e esperando pelo outro hashi que está sendo segurado por seu vizinho. Isso cria uma dependência circular, e nenhum filósofo consegue pegar o segundo hashi para começar a comer, resultando em um impasse onde todos esperam indefinidamente.

As quatro condições de Coffman para deadlock são:
1.  **Exclusão Mútua**: Os recursos (hashis) não podem ser compartilhados; apenas um filósofo pode usar um hashi por vez.
2.  **Posse e Espera (Hold and Wait)**: Cada filósofo segura um hashi e espera pelo outro.
3.  **Não Preempção**: Um hashi não pode ser retirado de um filósofo que o está segurando; ele deve ser liberado voluntariamente.
4.  **Espera Circular**: Existe uma cadeia circular de filósofos, onde cada um espera por um recurso que está sendo segurado pelo próximo na cadeia.

## Soluções Clássicas para Evitar Deadlock

Diversas soluções foram propostas para evitar o *deadlock* no Problema dos Filósofos Jantando. Algumas das mais comuns incluem:

1.  **Limitar o número de filósofos comendo simultaneamente (N-1)**:
    *   Permitir que no máximo N-1 filósofos peguem hashis de cada vez. Isso garante que sempre haverá pelo menos um conjunto de hashis disponível para um filósofo comer, quebrando a condição de espera circular. Isso pode ser implementado com um semáforo que limita o número de filósofos que podem tentar pegar hashis.

2.  **Ordem Hierárquica dos Recursos**: 
    *   Atribuir uma ordem global aos hashis (por exemplo, numerá-los de 0 a N-1). Todos os filósofos devem pegar o hashi com o número mais baixo primeiro e depois o hashi com o número mais alto. Por exemplo, o filósofo 0 pega o hashi 0, depois o hashi 1. O filósofo 1 pega o hashi 1, depois o hashi 2, e assim por diante. O último filósofo (N-1) deve pegar o hashi N-1 e depois o hashi 0. Isso quebra a espera circular, pois não é possível que todos esperem por um recurso de número menor que já está ocupado.

3.  **Filósofo assimétrico (Uma exceção)**:
    *   Fazer com que um dos filósofos (ou um número ímpar de filósofos) pegue o hashi da direita primeiro e depois o da esquerda, enquanto os outros (ou um número par de filósofos) pegam o hashi da esquerda primeiro e depois o da direita. Isso também quebra a condição de espera circular.

4.  **Monitor**: 
    *   Utilizar uma estrutura de monitor para gerenciar o acesso aos hashis. O monitor garante que apenas um filósofo por vez pode verificar e pegar os hashis, evitando condições de corrida e *deadlock* ao controlar o estado de 
