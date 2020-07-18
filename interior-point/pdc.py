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
print('                Primal-Dual Classico\n')
print('                ----------------------------\n\n\n')

#######################################################################
# Constantes


#######################################################################
# Tratamento de entradas

# Trata argumentos
opcoes = util.processa_argumentos(sys.argv, 'Primal-Dual Classico')

# Extrai dados de arquivo de entrada
m, n, A, b, c = util.le_arquivo_pl(opcoes.input_file)

# Obtem 'epsilon', 'tau' e 'sigma' do usuario
epsilon = float(input("Informe o valor de 'e': "))
print('\n')
tau = float(input("Informe o valor de 'tau': "))
print('\n')
sigma = float(input("Informe o valor de 'sigma': "))
print('\n')

# Opcionalmente, obtem x0 do usuario
x0 = []
for i in range(1, n+1):
    x = input("Informe o valor de 'x"+str(i)+"' (digite 'N' para ignorar): ")
    print('\n')
    if (x.isnumeric()):
        x0.append(x)
    else:
        print('Ponto inicial nao informado, assumindo [1, 1, ..., 1]')
        x0 = np.ones(n)
        break
# Opcionalmente, obtem y0 do usuario
y0 = []
for i in range(1, m+1):
    y = input("Informe o valor de 'y"+str(i)+"' (digite 'N' para ignorar): ")
    print('\n')
    if (y.isnumeric()):
        y0.append(y)
    else:
        print('Ponto inicial nao informado, assumindo [0, 0, ..., 0]')
        y0 = np.zeros(m)
        break
# Opcionalmente, obtem z0 do usuario
z0 = []
for i in range(1, n+1):
    z = input("Informe o valor de 'z"+str(i)+"' (digite 'N' para ignorar): ")
    print('\n')
    if (z.isnumeric()):
        z0.append(z)
    else:
        print('Ponto inicial nao informado, assumindo [1, 1, ..., 1]')
        z0 = np.ones(n)
        break

#######################################################################
# Algoritmo Primal-Dual Classico

#### cria vetores e matrizes auxiliares
Xk = np.zeros((n, n))
Zk = np.zeros((n, n))
Xkinv = np.zeros((n, n))
Zkinv = np.zeros((n, n))
Dkinv = np.zeros((n, n))
# inicializa Xk+1 e Zk+1
for i in range(0,n):
    Xk[i,i] = x0[i]
    Zk[i,i] = z0[i]
# inicializa yk
yk = y0
#### inicializacao de variaveis auxiliares
# contador de iteracoes
iter_cnt = 0
# variaveis de tempo
tempo_total = datetime.timedelta()
# indicacao de otimalidade
otimo = False
#### pre-calcula valores mais utilizadas
At = np.transpose(A)
e = np.ones(n)

# loop principal do algoritmo
while True:
    # registra inicio da iteracao
    tempo1 = datetime.datetime.now()
    # incrementa contador de  iteracoes
    iter_cnt += 1
    # armazena Xk*Zk, pois sera reutilizado
    XkZk = np.dot(Xk, Zk)
    # calcula gamma = Tr[XkZk]
    gamma = np.trace(XkZk)
    # calcula mu = sigma*(gamma/n)
    mu = sigma*(gamma/n)
    # calcula rp = b - Ax
    rp = b - np.dot(A, np.diagonal(Xk))
    # faz de rp vetor coluna
    rp = rp.reshape(-1, 1)
    # calcula rd = c - At*yk - zk
    rd = c - np.dot(At, yk) - np.diagonal(Zk)
    # faz de rd vetor coluna
    rd = rd.reshape(-1, 1)
    # calcula rc = mu*e - Xk*Zk*e
    rc = mu*e - np.dot(XkZk, e)
    # faz de rc vetor coluna
    rc = rc.reshape(-1, 1)
    # verifica otimalidade
    F2 = np.square(np.linalg.norm(np.concatenate([rp, rd, rc]), ord=2))
    if (F2 <= epsilon):
        otimo = True
        break
    # armazena (Xk)^-1 para ser reutilizada
    for i in range(0, n):
        Xkinv[i,i] = 1/Xk[i,i]
    # calcula Dk = [(Xk)^-1 *Zk]
    Dk = np.dot(Xkinv, Zk)
    # armazena (Zk)^-1
    for i in range(0, n):
        Zkinv[i,i] = 1/Zk[i,i]
    # armazena (Dk)^-1
    for i in range(0, n):
        Dkinv[i,i] = 1/Dk[i,i]
    # armazena A(Dk)^-1
    ADkinv = np.dot(A, Dkinv)
    # calcula dy = [A(Dk)^-1 *At]^-1 *[rp+A(Dk)^-1 *rd-A(Zk)^-1 *rc]
    dy = np.dot(np.linalg.inv(np.dot(ADkinv, At)), rp + np.dot(ADkinv, rd) - np.dot(np.dot(A, Zkinv), rc))
    # calcula dx = (Dk)^-1[At*dy - rd + (Xk)^-1 *rc]
    dx = np.dot(Dkinv, (np.dot(At, dy)-rd+np.dot(Xkinv, rc)))
    # calcula dz = (Xk)^-1[rc - Zk*dx]
    dz = np.dot(Xkinv, rc - np.dot(Zk, dx))
    # calcula rhop = min{-xi/dxi}
    rhop = np.inf
    for i in range(0, len(dx)):
        if (dx[i] < 0):
            p = -Xk[i,i]/dx[i]
            if (p < rhop):
                rhop = p
    # calcula rhod = min{-zi/dzi}
    rhod = np.inf
    for i in range(0, len(dz)):
        if (dz[i] < 0):
            p = -Zk[i,i]/dz[i]
            if (p < rhod):
                rhod = p
    # verifica solucao ilimitada
    if (rhop == np.inf or rhod == np.inf):
        break
    # calcula alphap = min{tau*rhop, 1}
    alphap = tau*rhop
    if (alphap > 1):
        alphap = 1
    # calcula alphad = min{tau*rhod, 1}
    alphad = tau*rhod
    if (alphad > 1):
        alphad = 1
    # atualiza Xk <= Xk+1 = xk + alphap*dx
    for i in range(0, n):
        Xk[i,i] = Xk[i,i] + alphap*dx[i]
    # atualiza yk <= yk+1 = yk + alphad*dy
    for i in range(0, m):
        yk[i] = yk[i] + alphad*dy[i]
    # atualiza Zk <= Zk+1 = zk + alphad*dz
    for i in range(0, n):
        Zk[i,i] = Zk[i,i] + alphad*dz[i]
    # registra fim da iteracao
    tempo2 = datetime.datetime.now()
    # soma iteracao ao tempo total
    tempo_total += tempo2 - tempo1
    # mostra resultado da iteracao no terminal
    util.print_info_iter_pdc(iter_cnt,np.diagonal(Xk),np.diagonal(Zk),yk,rp,rd,rc,F2,epsilon,tempo2-tempo1,tempo_total)

# trata solucao obtida
if (otimo):
    print('>>>>>> Resultado: Solucao otima alcancada\n')
else:
    print('>>>>>> Resultado: Solucao ilimitada\n')

