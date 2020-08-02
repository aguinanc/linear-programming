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
        self.lista_arc = []
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
        self.lista_arc.append((v1, v2, custo, nome))
        return 0
    def cria_aresta(self, v1, v2, custo, nome=''):
        res1 = self.cria_arco(v1, v2, custo, nome)
        if res1 == 0:
            self.cria_arco(v2, v1, custo, nome)
        else:
            return -1
    def arco(self, v1, v2):
        if v1 in self.dicio_vertices:
            if v2 in self.dicio_vertices[v1]:
                return self.dicio_vertices[v1][v2].nome
            else:
                return None
        else:
            return None
    def lista_arcos(self):
        return self.lista_arc
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
        if v in self.dicio_vertices:
            return list(self.dicio_vertices[v].keys())
        else:
            return []
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
    # cria lista para arcos da Arvore Geradora Minima
    lista_arvore = []
    # obtem numero de vertices e arcos
    num_v = g.num_vertices()
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
        # atualiza arestas da arvore geradora
        lista_arvore.append((melhor_arco[0], melhor_arco[1], custo, g.arco(melhor_arco[0], melhor_arco[1])))
        # atualiza vertices ja visitados
        ja_visitados.append(melhor_arco[1])
        nao_visitados.remove(melhor_arco[1])
    return lista_arvore

def kruskal(g):
    ''' Aplica algoritmo de Kruskal '''
    ''' O algoritmo trabalha com arcos, ao inves de
        arestas, pois a classe Grafo possui direcoes.
        No entanto, o algoritmo ignora arcos que correspondem
        a mesma aresta '''
    # obtem numero de vertices
    max_num_vert = g.num_vertices()
    # cria lista para arestas da Arvore Geradora Minima
    lista_arvore = []
    # obtem lista de arcos
    lista_arcos = g.lista_arcos()
    # ordena lista de forma nao-decrescente pelo custo
    lista_arcos.sort(key=lambda elem: elem[2])
    # adiciona aresta de menor custo
    lista_arvore.append(lista_arcos[0])
    # indice da aresta
    idx = 1
    # contagem de arestas
    cnt = 1
    # adiciona arestas ate todos os vertices estarem presentes
    while cnt < max_num_vert-1:
        # vertices da aresta sob analise
        v1 = lista_arcos[idx][0]
        v2 = lista_arcos[idx][1]
        # verifica se nao sera criado um ciclo
        repetida = False
        # listas para monitorar conjuntos e ciclos
        grupos_unidos_v1 = []
        grupos_unidos_v2 = []
        ciclos = False
        for subgrupo in lista_arvore:
            if repetida == True:
                break
            # se subgrupo e aresta sozinha
            if type(subgrupo) == tuple:
                # verifica se aresta nao e repetida
                if v1 in subgrupo[:2] and v2 in subgrupo[:2]:
                    repetida = True
                    break
                # verifica se haveria uniao com vertice v1
                if v1 in subgrupo[:2]:
                    if subgrupo not in grupos_unidos_v1:
                        if subgrupo not in grupos_unidos_v2: 
                            grupos_unidos_v1.append(subgrupo)
                        else:
                            # ha um ciclo
                            ciclos = True
                            break
                # verifica se haveria uniao com vertice v2
                if v2 in subgrupo[:2]:
                    if subgrupo not in grupos_unidos_v2:
                        if subgrupo not in grupos_unidos_v1: 
                            grupos_unidos_v2.append(subgrupo)
                        else:
                            # ha um ciclo
                            ciclos = True
                            break
            else:
                # se subgrupo contem varias arestas
                for aresta in subgrupo:
                    # verifica se aresta nao e repetida
                    if v1 in aresta[:2] and v2 in aresta[:2]:
                        repetida = True
                        break
                    # verifica se haveria uniao com vertice v1
                    if v1 in aresta[:2]:
                        if subgrupo not in grupos_unidos_v1:
                            if subgrupo not in grupos_unidos_v2: 
                                grupos_unidos_v1.append(subgrupo)
                            else:
                                # ha um ciclo
                                ciclos = True
                                break
                    # verifica se haveria uniao com vertice v2
                    if v2 in aresta[:2]:
                        if subgrupo not in grupos_unidos_v2:
                            if subgrupo not in grupos_unidos_v1: 
                                grupos_unidos_v2.append(subgrupo)
                            else:
                                # ha um ciclo
                                ciclos = True
                                break
        # se aresta ja existe, pula para a proxima
        if repetida == True:
            idx += 1
            continue
        # se aresta forma ciclo, pula para a proxima
        if ciclos == True:
            idx += 1
            continue
        # remove subgrupos da lista atual
        for subgrupo in grupos_unidos_v1:
            lista_arvore.remove(subgrupo)
        for subgrupo in grupos_unidos_v2:
            lista_arvore.remove(subgrupo)
        # obtem arestas sozinhas
        arestas_sozinhas_v1 = [i for i in grupos_unidos_v1 if type(i)==tuple] 
        arestas_sozinhas_v2 = [i for i in grupos_unidos_v2 if type(i)==tuple] 
        arestas_sozinhas = arestas_sozinhas_v1 + arestas_sozinhas_v2
        # concatena arestas que estao separadas em grupos distintos
        arestas_em_grupos_v1 = [i for i in grupos_unidos_v1 if type(i)==list] 
        arestas_em_grupos_v2 = [i for i in grupos_unidos_v2 if type(i)==list] 
        concatenado = []
        for i in arestas_em_grupos_v1:
            concatenado += i
        for i in arestas_em_grupos_v2:
            concatenado += i
        # concatena arestas sozinhas e arestas que estavam em grupos
        grupos_unidos = concatenado + arestas_sozinhas
        # acrescenta aresta nova
        if (len(grupos_unidos) > 0):
            grupos_unidos.append(lista_arcos[idx])
            lista_arvore.append(grupos_unidos)
        else:
            lista_arvore.append(lista_arcos[idx])
        # incrementa contador de arestas
        cnt += 1
        # incrementa index da aresta candidata
        idx += 1
    # retorna lista com arestas (forma um unico subgrupo)
    return lista_arvore[0]
