#!/usr/bin/env python3

########################### Executar com Python 3 ###########################

import numpy as np
import argparse

file_help = "Entradas:\n" \
"Arquivo .txt contendo m e n: o número de linhas e colunas da matriz A, respectivamente; a matriz A: de dimensão mxn; e os vetores: b, c, de dimesao m e n respectivamente. O arquivo deve seguir a sintaxe abaixo:\n" \
"m = <m>;\n" \
"n = <n>;\n" \
"A = [<a11>, <a12>, ..., <a1n>, <a21>, <a22>, ..., <a2n>, ..., <am1>, <am2>, ..., <amn>];\n" \
"b = [<b1>, ..., <bm>];\n" \
"c = [<c1>, ..., <cn>];\n" \
"Espacos, colchetes '[]' ou quebras de linha sao opcionais. Os elementos <a11>, <b1>, <c1>, <m>, <n>, e assim por diante, devem ser substituidos por valores numericos. Por exemplo, 'A = [1, 3, 5, -1];' Os parametros m, n, A, b, c podem ser fornecidos em qualquer ordem.\n"

''' Func: Processa argumentos de entrada '''
def processa_argumentos(input_args, desc=''):
    usage_str = input_args[0]+" [-h] [-f INPUT_FILE]"
    # configuracao do parser
    parser = argparse.ArgumentParser(usage=usage_str+'\n\n'+desc+'\n\n'+file_help)
    parser.add_argument('-f', action="store", dest="input_file", type=str, default='input.txt', help="nome do arquivo de entrada, default='input.txt'")
    parser.add_argument('-m', action="store", dest="big_m_value", type=float, default='0', help="valor de Big-M")
    parser.add_argument('--auto-big-m', action="store_true", dest="auto_big_m", help="calcula Big-M automaticamente")
    # le argumentos e escreve nas variaveis
    args = parser.parse_args(input_args[1:])
    return args

''' Func: Exibe resultados de uma iteracao PAE '''
def print_info_iter_pae(iter_cnt, X, valor_obj, gap, var, e, deltat, totalt):
    print('---- iteracao '+str(iter_cnt)+' ----------------\n')
    cnt = 1
    for i in range(0, X.shape[0]):
        print('x'+str(cnt)+'= '+str(X[i,i])+'\n')
        cnt += 1
    print('Detalhes: valor funcao objetivo='+str(valor_obj)+'\tgap rel='+str(gap)+'\tvariacao da func. obj.='+str(var)+'\tConvergencia p/ e<='+str(e)+'\n')
    print('Duracao da iteracao='+str(deltat)+'\tTempo total='+str(totalt)+'\n')
    print("\n\n")
    return

''' Func: Le arquivo contendo informacoes matrizes "A", "b", "c"
          e dimensoes m e n '''
def le_arquivo_pl(nome_arquivo):
    with open(nome_arquivo) as f:
        dados = f.read()
        # remove quebras de linha
        dados = dados.replace('\n','')
        dados = dados.replace('\r','')
        # remove tabs e espacos
        dados = dados.replace('\t','')
        dados = dados.replace(' ','')
        # remove colchetes
        dados = dados.replace('[','')
        dados = dados.replace(']','')
        # divide seccoes por ';'
        dados = dados.split(';')
        # remove seccoes vazias
        # devido a algum ; em excesso
        dados = list(filter(None, dados))
        # remove seccoes com informacao
        # que nao seja uma das matrizes
        dados = [s for s in dados if (('A=' in s) or ('b=' in s) or ('c=' in s) or ('m=' in s) or ('n=' in s))]
        # indica erro se houver num de
        # seccoes estiver incorreto
        if (len(dados) != 5):
            return (-1, -1, [[]], [], [])
        # separa dados em uma lista de saida
        dados_filtrados = []
        # atribui dados de m, n, A, b, c
        dados_filtrados.append([s for s in dados if 'm=' in s])
        dados_filtrados.append([s for s in dados if 'n=' in s])
        dados_filtrados.append([s for s in dados if 'A=' in s])
        dados_filtrados.append([s for s in dados if 'b=' in s])
        dados_filtrados.append([s for s in dados if 'c=' in s])
        # checa se nenhuma informacao esta
        # faltando
        if (not all(len(d)!=0 for d in dados_filtrados)):
            return (-1, -1, [[]], [], [])
        # deixa apenas caracteres a direita
        # do sinal de igualdade em cada item
        dados_filtrados = [s[0].lstrip(s[0].replace('=','')).replace('=','') for s in dados_filtrados]
        # transfere dimensoes da matriz A para variaveis de saida
        m = int(dados_filtrados[0])
        n = int(dados_filtrados[1])
        # transforma strings em vetores de numeros
        dados_filtrados = [d.split(',') for d in dados_filtrados]
        # cria matriz A de saida,
        # converte elementos para float
        # e transforma array 1D em 2D
        A = np.reshape([float(a) for a in dados_filtrados[2]], (-1,n))
        # cria vetor b de saida
        b = np.array([float(bi) for bi in dados_filtrados[3]])
        # cria vetor c de saida
        c = np.array([float(ci) for ci in dados_filtrados[4]])
    return (m, n, A, b, c)

