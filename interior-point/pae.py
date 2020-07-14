#!/usr/bin/env python3

########################### Executar com Python 3 ###########################

import numpy as np
import datetime
import sys
import util
import scipy
import scipy.linalg

#############################################################################
# Tratamento de entradas

# Trata argumentos
opcoes = util.processa_argumentos(sys.argv, 'Primal Afim-Escala')
# Extrai matrizes de arquivo de entrada
#A, b, c = util.le_arquivo_pl(opcoes.input_file)

#############  PARA DEBUG APENAS ############
# !  !  !  !                       !  !  !  !

n = 7
m = 3
e = 0.0001
tau = 0.99

c = np.array([0, 0, 0, -0.75, 20, -0.5, 6])
b = np.array([0, 0, 1])
A = np.array([[1, 0, 0, 0.25, -8, -1, 9], [0, 1, 0, 0.5, -12, -0.5, 3], [0, 0, 1, 0, 0, 1, 0]])

fator_big_m = 1000
valor_big_m = 1000
auto_big_m = True

##############################################

#############################################################################
# Algoritmo Primal Afim-Escala

# Escolhe-se inicialmente x0 = [1,1,...,1]
x0 = np.ones(n)
# Veifica-se se x0 factivel
# p = b - Ax0
p = b - np.dot(A, x0)
# transforma p em uma matrix de 1 coluna
p = p.reshape(-1, 1)
### debug
print('p=\n')
print(p)
#-------
big_m = False
for i in range(0, m):
    if (p[i,0] != 0):
        # debug
        print('big-M = yes\n')
        # -----
        big_m = True

# faz Big-M se necessario
if (big_m):
    # calcula valor de big-M
    if (auto_big_m):
        M = np.absolute(np.amax(c)*np.amax(b)/np.amin(A))*fator_big_m
    else:
        M = valor_big_m
    n += 1
    # expande vetor c
    c = np.concatenate([c,[M]])
    # expande matrix A
    A = np.concatenate([A,p],axis=1)
    # expande vetor x0
    x0 = np.concatenate([x0, [1]])

#### cria vetores e matrizes auxiliares
# cria vetor para diagonal de Xk e Xk+1
Xk = np.zeros((n, n))
Xk_novo = np.zeros((n, n))
# inicializa Xk+1
for i in range(0,n):
    Xk_novo[i,i] = x0[i]

# cria vetor para diagonal de Xk2
Xk2 = np.zeros((n, n))
#### inicializa criterio de parada
# gap relativo
gap = np.inf
# variacao do valor da funcao objetivo
var = np.inf
#### inicializacao de variaveis auxiliares
# contador de iteracoes
iter_cnt = 0
# variaveis de tempo
tempo_total = datetime.timedelta()
#### pre-calcula variavies mais utilizadas
At = np.transpose(A)

# loop principal do algoritmo
while gap > e and var > e:
    # registra inicio da iteracao
    tempo1 = datetime.datetime.now()
    # incrementa contador de  iteracoes
    iter_cnt += 1
    # atualiza Xk <= Xk_novo
    for i in range(0,n):
        Xk[i,i] = Xk_novo[i,i]
    # calcula e armazena Xk^2
    for i in range(0,len(Xk)):
        Xk2[i,i] = Xk[i,i]*Xk[i,i]
    # calcula e armazena A(Xk)^2
    AXk2 = np.dot(A,Xk2)
    # resolve yk = (A*(Xk)^2 *At)^-1 *A(Xk)^2 *c
    # como um sistema linear (A*(Xk)^2 *At)*yk = A(Xk)^2 *c
    # factorizacao Cholesky
    ch, low = scipy.linalg.cho_factor(np.dot(AXk2, At))
    yk = scipy.linalg.cho_solve((ch, low), np.dot(AXk2, c))
    # resolve zk = c - At*yk
    zk = c - np.dot(At,yk)
    # resolve dk = -(Xk)^2*zk
    dk = np.dot(-Xk2, zk)
    # verifica solucao ilimitada ou multipla
    if (not (dk<0).any()):
        break
    # resolve alphak = tau*min{-xk/dk}
    min_passo = np.inf
    for i in range(0, n):
        if (dk[i] < 0):
            p = -Xk[i,i]/dk[i]
            if (p < min_passo):
                min_passo = p
    alphak = tau*min_passo
    # calcula novo Xk
    for i in range(0,n):
        Xk_novo[i,i] = Xk[i,i] + alphak *dk[i]
    # atualiza gap relativo
    Xkzk = np.dot(Xk,zk)
    valor_obj = np.dot(c, np.diagonal(Xk))
    valor_obj_novo = np.dot(c, np.diagonal(Xk_novo))
    gap = np.linalg.norm(Xkzk, ord=2)/(1 + np.absolute(np.dot(b,yk)+valor_obj))
    var = np.absolute(valor_obj_novo-valor_obj)/(1 + np.absolute(valor_obj))
    # registra fim da iteracao
    tempo2 = datetime.datetime.now()
    # soma iteracao ao tempo total
    tempo_total += tempo2 - tempo1
    # mostra resultado da iteracao no terminal
    util.print_info_iter_pae(iter_cnt,Xk,valor_obj,gap,var,e,tempo2-tempo1,tempo_total)

# trata solucao obtida
if ((dk>0).all()):
    print('>>>>>> Resultado: Solucao ilimitada\n')
elif ((dk==0).all()):
    print('>>>>>> Resultado: Solucao otima multipla\n')
else:
    print('>>>>>> Resultado: Solucao otima alcancada\n')

