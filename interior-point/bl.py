#!/usr/bin/env python3

########################### Executar com Python 3 ###########################

import numpy as np
import datetime
import sys
import util
import scipy
import scipy.linalg

#######################################################################
# Apresentacao para usuario
print('\n\n')
print('                Algoritmo\n')
print('                Barreira Logaritmica\n')
print('                ----------------------------\n\n\n')

#######################################################################
# Constantes

fator_big_m = 1000

#######################################################################
# Tratamento de entradas

# Trata argumentos
opcoes = util.processa_argumentos(sys.argv, 'Barreira Logaritmica')

valor_big_m = opcoes.big_m_value
auto_big_m = opcoes.auto_big_m

# Extrai dados de arquivo de entrada
m, n, A, b, c = util.le_arquivo_pl(opcoes.input_file)

# Obtem 'epsilon', 'tau', 'mu' e 'beta' do usuario
epsilon = float(input("Informe o valor de 'epsilon': "))
print('\n')
tau = 2
while tau > 1:
    tau = float(input("Informe o valor de 'tau': "))
    print('\n')
    if (tau > 1):
        print('Error: tau must be in 0 <= tau <= 1\n')
mu = float(input("Informe o valor de 'mu': "))
print('\n')
beta = float(input("Informe o valor de 'beta': "))
print('\n')

#######################################################################
# Algoritmo Barreira Logaritmica

# Escolhe-se inicialmente x0 = [1,1,...,1]
x0 = np.ones(n)
# Veifica-se se x0 factivel
# p = b - Ax0
p = b - np.dot(A, x0)
# transforma p em uma matrix de 1 coluna
p = p.reshape(-1, 1)

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

#### inverte custos uma vez que Barreira Log.
#### trabalha com maximizacao
c = -c

#### cria vetores e matrizes auxiliares
Xk = np.zeros((n, n))
Xk_novo = np.zeros((n, n))
dx_antigo = np.zeros(n)
# inicializa Xk+1
for i in range(0,n):
    Xk_novo[i,i] = x0[i]
#
#### inicializacao de variaveis auxiliares
# contador de iteracoes
iter_cnt = 0
# variaveis de tempo
tempo_total = datetime.timedelta()
# indicador de otimalidade
otimo = False

# exibe valores iniciais
util.print_info_iter_bl(iter_cnt ,Xk, -np.dot(c, np.diagonal(Xk)), 0, 0, epsilon, 0, 0)

# loop principal do algoritmo
while True:
    # registra inicio da iteracao
    tempo1 = datetime.datetime.now()
    # incrementa contador de  iteracoes
    iter_cnt += 1
    # atualiza Xk
    for i in range(0,n):
        Xk[i,i] = Xk_novo[i,i]
    # calcula ck = Xk*c
    ck = np.dot(Xk, c)
    # transforma ck em vetor coluna
    ck = ck.reshape(-1, 1)
    # calcula Ak = A*Xk
    Ak = np.dot(A, Xk)
    # calcula (Ak)^t
    Akt = np.transpose(Ak)
    # resolve Pk = I - (Ak)^t [Ak(Ak)^t]^-1 *Ak
    Pk = np.identity(n, dtype=float) - np.dot(np.dot(Akt, np.linalg.inv(np.dot(Ak, Akt))), Ak)
    # resolve dx = Xk*Pk*(ck + mu*e)
    dx = np.dot(np.dot(Xk, Pk), ck + mu*np.ones(n).reshape(-1,1))
    # calcula lambdak = min{-xi/dxi}
    lambdak = np.inf
    for i in range(0, n):
        if (dx[i] < 0):
            p = -Xk[i,i]/dx[i]
            if (p < lambdak):
                lambdak = p
    # verifica solucao ilimitada
    if (lambdak == np.inf):
        break
    # resolve alphak = min{1/mu, tau*lambdak}
    alphak = tau*lambdak
    if (alphak > 1/mu):
        alphak = 1/mu
    # calcula novo Xk
    for i in range(0,n):
        Xk_novo[i,i] = Xk[i,i] + alphak *dx[i]
    # atualiza mu
    mu = beta*mu
    # calcula condicoes de otimalidade
    valor_obj_antigo = np.dot(c, np.diagonal(Xk))
    valor_obj_novo = np.dot(c, np.diagonal(Xk_novo))
    delta_cx = np.absolute(valor_obj_novo - valor_obj_antigo)
    delta_dx = np.absolute(dx - dx_antigo)
    # atualiza dx antigo
    dx_antigo = dx
    # registra fim da iteracao
    tempo2 = datetime.datetime.now()
    # soma iteracao ao tempo total
    tempo_total += tempo2 - tempo1
    # mostra resultado da iteracao no terminal
    # fornece -valor func obj, pois o PL original era de min
    util.print_info_iter_bl(iter_cnt ,Xk_novo, -valor_obj_novo, delta_cx, delta_dx, epsilon, tempo2-tempo1, tempo_total)
    # verifica otimalidade
    if (delta_cx <= epsilon or (delta_dx <= epsilon).all()):
        otimo = True
        break

# trata solucao obtida
if (otimo):
    print('>>>>>> Resultado: Solucao otima alcancada\n')
else:
    print('>>>>>> Resultado: Solucao ilimitada\n')

