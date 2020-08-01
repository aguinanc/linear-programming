#!/usr/bin/env python3

#################################################
# Algoritmos para busca de Arvore Geradora Minima

########################### Executar com Python 3 ###########################

from numpy import inf
from random import randint

class Arco:
    def __init__(self, custo, nome=''):
        self.custo = custo
        self.nome = nome

class Grafo:
    def __init__(self, nome):
        self.nome_grafo = nome
        self.dicio_vertices = {}
        self.num_vert = 0
        self.num_arc = 0
    def cria_vert(self, v):
        self.dicio_vertices[v] = {}
        self.num_vert += 1
        return 0
    def cria_arco(self, v1, v2, custo, nome=''):
        if v1 not in self.dicio_vertices:
            self.cria_vert(v1)
        if v2 in self.dicio_vertices[v1]:
            return -1
        if v2 not in self.dicio_vertices:
            self.cria_vert(v2)
        self.dicio_vertices[v1][v2] = Arco(custo, nome)
        self.num_arc += 1
        return 0
    def remove_vert(v):
        if v in self.dicio_vertices:
            self.dicio_vertices.pop(v)
        return 0
    def arco(self, v1, v2):
        if v1 in self.dicio_vertices:
            if v2 in self.dicio_vertices[v1]:
                return self.dicio_vertices[v1][v2].nome
            else:
                return None
        else:
            return None
    def dist(self, v1, v2):
        if v1 in self.dicio_vertices:
            if v2 in self.dicio_vertices[v1]:
                return self.dicio_vertices[v1][v2].custo
            else:
                return inf
        else:
            return inf
    def vertices(self):
        return list(self.dicio_vertices.keys())
    def num_vertices(self):
        return self.num_vert
    def num_arcos(self):
        return self.num_arc
    def vizinhos(self, v):
        return list(self.dicio_vertices[v].keys())
    def num_vizinhos(self, v):
        return len(self.vizinhos(v))
    def nome(self):
        return self.nome_grafo
    def print_grafo(self):
        for v in self.dicio_vertices.keys():
            print('Vertice= '+str(v))
            print('\tConectado a '+str(self.vizinhos(v)))

def prim(g):
    ''' Aplica algoritmo de Prim '''
    # cria conjunto de arestas da Arvore Geradora Minima
    arvore = Grafo('ArvGeradoraMin')
    cnt = 0
    # obtem numero de vertices e arcos
    num_v = g.num_vertices()
    num_a = g.num_arcos()
    # vertices visitados
    ja_visitados = []
    # vertices nao visitados
    nao_visitados = g.vertices()
    # escolhe vertice aleatorio
    v_inicial = nao_visitados[randint(0,num_v-1)]
    nao_visitados.remove(v_inicial)
    ja_visitados.append(v_inicial)
    while len(nao_visitados) > 0:
        # busca arco de menor peso
        custo = inf
        melhor_arco = ('', '')
        for v_atual in ja_visitados:
            viz_disponiveis = g.vizinhos(v_atual)
            for vizinho in viz_disponiveis:
                if vizinho in nao_visitados and g.dist(v_atual, vizinho) < custo:
                    melhor_arco = (v_atual, vizinho)
                    custo = g.dist(v_atual, vizinho)
        # atualiza arvore geradora
        arvore.cria_arco(melhor_arco[0], melhor_arco[1], custo, g.arco(melhor_arco[0], melhor_arco[1]))
        # atualiza vertices ja visitados
        ja_visitados.append(melhor_arco[1])
        nao_visitados.remove(melhor_arco[1])
    return arvore

