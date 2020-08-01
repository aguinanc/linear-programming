#!/usr/bin/env python3

#################################################
# Comparação dos Algoritmos de Prim e Kruskal
# para a NSFNET

########################### Executar com Python 3 ###########################

from numpy import array
from datetime import datetime
from datetime import timedelta
import sys
from random import randint
import agm

# Definicao de tabela representando NSFNET

matriz_nsfnet = array(\
[ \
[ 1,  2,   3,   4,   5,  6,   7,   8,  9,  10, 11, 12,  13,  14, 15, 16,  17, 18,  19, 20,  21,  22, 23, 24,  25], \
[ 1,  1,   2,   2,   2,  3,   3,   4,  5,   5,  6,  6,   7,   7,  8,  9,  10, 11,  11, 12,  12,  13, 13, 14,  15], \
[ 2,  5,   3,   4,   9,  4,   5,   7,  6,  12,  7,  8,  10,  14,  9, 11,  11, 13,  15, 13,  15,  14, 16, 15,  16], \
[75, 120, 75, 120, 300, 75, 120, 150, 60, 300, 75, 60, 150, 300, 60, 60, 105, 75, 120, 60, 120, 120, 75, 60, 120] \
] )

# Cria grafo NSFNET baseado em matriz do problema
nsfnet = agm.Grafo('NSFNET')

for col in range(0, matriz_nsfnet.shape[1]):
    # criar arco (orig, dest, custo, nome)
    nsfnet.cria_arco(matriz_nsfnet[:,col][1], matriz_nsfnet[:,col][2], matriz_nsfnet[:,col][3], matriz_nsfnet[:,col][0]) 
    # criar arco (dest, orig, custo, nome)
    nsfnet.cria_arco(matriz_nsfnet[:,col][2], matriz_nsfnet[:,col][1], matriz_nsfnet[:,col][3], matriz_nsfnet[:,col][0]) 

print('----------------------')
print(nsfnet.nome())
nsfnet.print_grafo()
print('----------------------\n\n')

# Aplica algoritmo de Prim e registra tempo
t1 = datetime.now()
res_prim = agm.prim(nsfnet)
t2 = datetime.now()
deltat_prim = t2 - t1

# Aplica algoritmo de Kruskal e registra tempo
t1 = datetime.now()
#res_kruskal = agm.kruskal(nsfnet)
t2 = datetime.now()
deltat_kruskal = t2 - t1

print('Arvore= ')
res_prim.print_grafo()

# Encerra programa
sys.exit(0)
