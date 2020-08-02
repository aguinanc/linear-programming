#!/usr/bin/env python3

#################################################
# Utilidades

########################### Executar com Python 3 ###########################

from xlsxwriter import Workbook
import agm

def salva_grafo_excel(grafo, nome_arq='grafo'):
    workbook = Workbook(nome_arq+'.xlsx')
    worksheet = workbook.add_worksheet()
    # obtem lista de vertices
    lista_v = grafo.vertices()
    # cria dicionario para indice de vertices
    idx_v = {}
    # preenche dicionario com indices de
    # vertices na planilha
    idx = 1
    for v in lista_v:
        idx_v[v] = idx
        idx += 1
    # escreve vertices na primeira coluna
    col = 1
    for v in lista_v:
        worksheet.write(0, col, str(v))
        col += 1
    # escreve vertices na primeira linha
    linha = 1
    for v in lista_v:
        worksheet.write(linha, 0, str(v))
        linha += 1
    # preenche tabela
    for v1 in lista_v:
        for v2 in grafo.vizinhos(v1):
            worksheet.write(idx_v[v1], idx_v[v2], grafo.dist(v1, v2))
    # encerra escrita
    workbook.close()

