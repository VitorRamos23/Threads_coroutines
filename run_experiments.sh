#!/bin/bash

# Cria o diretório de resultados se não existir
mkdir -p results

echo "### Iniciando Experimentos de Concorrência (5 Repetições cada) ###"

# Limpa CSVs anteriores
rm -f results/coroutines_metrics.csv
rm -f results/threads_metrics.csv

# Define o número de repetições
REPETITIONS=5

# --- Experimentos com Corrotinas ---
echo ""
echo "--- Rodando Corrotinas (asyncio) ---"
for i in $(seq 1 $REPETITIONS); do
    echo "Execução $i/$REPETITIONS: Corrotinas"
    python3 dining_philosophers_coroutines_revised.py
done

# --- Experimentos com Threads ---
echo ""
echo "--- Rodando Threads (threading) ---"
for i in $(seq 1 $REPETITIONS); do
    echo "Execução $i/$REPETITIONS: Threads"
    python3 dining_philosophers_threads_revised.py
done

echo ""
echo "### Experimentos Concluídos! ###"
echo "Resultados em: results/coroutines_metrics.csv e results/threads_metrics.csv"