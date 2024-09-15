from funcoes import *
from bucket import *
import pandas as pd
import sys
import time  # Importando o módulo time para utilizar o sleep
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Função para selecionar um arquivo Excel usando uma interface gráfica
def selecionar_arquivo_excel():
    root = Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    arquivo = askopenfilename(title="Selecione o arquivo .xlsx", filetypes=[("Arquivo Excel", "*.xlsx")])
    return arquivo

# Carregar os parâmetros a partir de um arquivo Excel
def carregar_parametros_do_excel(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)
    # Supondo que os parâmetros estão na primeira coluna
    return df.iloc[:, 0].tolist()

# Abrir explorador de arquivos para o usuário selecionar o arquivo Excel
caminho_arquivo = selecionar_arquivo_excel()

if not caminho_arquivo:
    print("Nenhum arquivo selecionado. Saindo do programa.")
    sys.exit()

# Agora 'parametros' é uma lista obtida do arquivo Excel
parametros = carregar_parametros_do_excel(caminho_arquivo)

# Inicializando os nomes dos buckets
bucket_matchts_ids = 'matchts-ids-teste'
bucket_match_info = 'match-info-teste'
bucket_id = 3
bucket_info = 6  

count = 1
bucket_novo = 1

# Iterando sobre cada item na lista 'parametros'
for parametro in parametros:
    json_matchsids = get_matchs(parametro)
    if json_matchsids:
        for item in json_matchsids:
            # Usando os buckets dinâmicos nos uploads
            upload_to_s3(bucket_matchts_ids, item, '')
            match_info = get_match_info(item)
            upload_to_s3(bucket_match_info, item + '.json', match_info)
            print(count)
            count += 1
            bucket_novo += 1

            # Verifica se o contador de buckets chegou a 1000
            if bucket_novo == 1000:
                # Incrementa o número do bucket e cria dois novos buckets
                bucket_id += 1
                bucket_info += 1
                novo_bucket_1 = f'matchts-ids-teste{bucket_id}'
                novo_bucket_2 = f'match-info-teste{bucket_info}'
                
                create_s3_bucket(novo_bucket_1)
                create_s3_bucket(novo_bucket_2)
                
                print(f'Criados os novos buckets: {novo_bucket_1} e {novo_bucket_2}')
                
                # Atualizando os nomes dos buckets
                bucket_matchts_ids = novo_bucket_1
                bucket_match_info = novo_bucket_2
                
                # Reiniciando o contador de bucket_novo após criar novos buckets
                bucket_novo = 0
    
    # Aguardando 120 segundos (2 minutos) antes de processar o próximo parâmetro
    print(f'Aguardando 2 minutos antes de processar o próximo parâmetro...')
    time.sleep(120)
