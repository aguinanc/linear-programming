#!/usr/bin/env python3

#################################################
# Comparação dos Algoritmos de Prim e Kruskal
# para a NSFNET

########################### Executar com Python 3 ###########################

from numpy import array
from datetime import datetime
from datetime import timedelta
import sys
import util
import agm

#######################################################################
# Apresentacao para usuario
print('\n\n')
print('                Arvore Geradora Minima - Grafo NSFNET\n')
print('                Aplicacao Metodos Prim e Kruskal\n')
print('                ----------------------------\n\n\n')

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

# Aplica algoritmo de Prim e registra tempo
t1 = datetime.now()
res_prim = agm.prim(nsfnet)
t2 = datetime.now()
deltat_prim = t2 - t1

# Aplica algoritmo de Kruskal e registra tempo
t1 = datetime.now()
res_kruskal = agm.kruskal(nsfnet)
t2 = datetime.now()
deltat_kruskal = t2 - t1

print('Resultado Prim:')
print('\tcusto total da arvore= '+str(sum([a[2] for a in res_prim])))
print('\ttempo de processamento= '+str(deltat_prim))
print('\n')

print('Resultado Kruskal:')
print('\tcusto total da arvore= '+str(sum([a[2] for a in res_kruskal])))
print('\ttempo de processamento= '+str(deltat_kruskal))
print('\n')

# cria estrutura de Grafo com resultado
# para posteriormente salvar em excel
g_res_prim = agm.Grafo('AGM_Prim_NSFNET')
for item in res_prim:
    g_res_prim.cria_aresta(item[0], item[1], item[2], item[3])

g_res_kruskal = agm.Grafo('AGM_Kruskal_NSFNET')
for item in res_kruskal:
    g_res_kruskal.cria_aresta(item[0], item[1], item[2], item[3])

# salva grafos em arquivos excel
print('Salvando matrizes de adjacencia... ')
print(nsfnet.nome()+'.xlsx')
print(g_res_prim.nome()+'.xlsx')
print(g_res_kruskal.nome()+'.xlsx')
util.salva_grafo_excel(nsfnet, nsfnet.nome())
util.salva_grafo_excel(g_res_prim, g_res_prim.nome())
util.salva_grafo_excel(g_res_kruskal, g_res_kruskal.nome())
print('\n')
print('--- Fim ---')

# Encerra programa
sys.exit(0)
