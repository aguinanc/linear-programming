#!/usr/bin/env python3

#################################################
# Comparação dos Algoritmos de Prim e Kruskal
# para a grafo gerado automaticamente

########################### Executar com Python 3 ###########################

from datetime import datetime
from datetime import timedelta
import sys
from random import randint
from random import choice
import util
import agm

#######################################################################
# Apresentacao para usuario
print('\n\n')
print('                Arvore Geradora Minima - Grafo Gerado\n')
print('                Aplicacao Metodos Prim e Kruskal\n')
print('                ----------------------------\n\n\n')

############################
# Variaveis

num_v = 200     # num de vertices
num_a = 1000    # num de arestas
max_custo = 100 # maximo custo de uma aresta
min_custo = 1   # minimo custo de uma aresta

## Gera grafo
grafo_gerado = agm.Grafo('Grafo Gerado')

# gera arvore principal (v-1 arestas)
for v in range(1, num_v):
    # cria aresta vn -> vn+1, custo_n, nome=n
    grafo_gerado.cria_aresta(v, v+1, randint(min_custo, max_custo), v)

# gera conexoes restantes
for a in range(num_v, num_a+1):
    # seleciona vertice 1 aleatoriamente
    v1 = randint(1, num_v)
    # obtem vizinhos ja conectados a v1
    lista_indisponiveis = grafo_gerado.vizinhos(v1)
    # acrescenta v1 aos vertices indisponiveis
    lista_indisponiveis.append(v1)
    # seleciona vertice 2 aleatoriamente (v2 != indisponiveis)
    v2 = choice([i for i in range(1, num_v) if i != lista_indisponiveis])
    # cria aresta v1 -> v2, custo, nome=a
    grafo_gerado.cria_aresta(v1, v2, randint(min_custo, max_custo), a)

# Aplica algoritmo de Prim e registra tempo
t1 = datetime.now()
res_prim = agm.prim(grafo_gerado)
t2 = datetime.now()
deltat_prim = t2 - t1

# Aplica algoritmo de Kruskal e registra tempo
t1 = datetime.now()
res_kruskal = agm.kruskal(grafo_gerado)
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
g_res_prim = agm.Grafo('AGM_Prim_Grafo_Gerado')
for item in res_prim:
    g_res_prim.cria_aresta(item[0], item[1], item[2], item[3])

g_res_kruskal = agm.Grafo('AGM_Kruskal_Grafo_Gerado')
for item in res_kruskal:
    g_res_kruskal.cria_aresta(item[0], item[1], item[2], item[3])

# salva grafos em arquivos excel
print('Salvando matrizes de adjacencia... ')
print(grafo_gerado.nome()+'.xlsx')
print(g_res_prim.nome()+'.xlsx')
print(g_res_kruskal.nome()+'.xlsx')
util.salva_grafo_excel(grafo_gerado, grafo_gerado.nome())
util.salva_grafo_excel(g_res_prim, g_res_prim.nome())
util.salva_grafo_excel(g_res_kruskal, g_res_kruskal.nome())
print('\n')
print('--- Fim ---')

# Encerra programa
sys.exit(0)
