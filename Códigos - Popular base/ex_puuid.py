import os
import json
import pandas as pd
from tkinter import Tk, filedialog
from datetime import datetime

# Função para escolher a pasta
def escolher_pasta():
    root = Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    pasta = filedialog.askdirectory(title="Escolha a pasta com os arquivos JSON")
    return pasta

# Função para buscar recursivamente o campo "puuid" no JSON
def buscar_puuid(dados):
    puuids = []

    if isinstance(dados, dict):  # Se os dados são um dicionário
        for chave, valor in dados.items():
            if chave == 'puuid':  # Se encontrou a chave "puuid"
                puuids.append(valor)
            elif isinstance(valor, (dict, list)):  # Se o valor é outro dict ou uma lista, busca recursivamente
                puuids.extend(buscar_puuid(valor))

    elif isinstance(dados, list):  # Se os dados são uma lista
        for item in dados:
            puuids.extend(buscar_puuid(item))

    return puuids

# Função para ler os JSONs e pegar os valores de "puuid"
def processar_jsons(pasta):
    puuids = []  # Lista para armazenar todos os PUUIDs

    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.json'):
            caminho_arquivo = os.path.join(pasta, arquivo)
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                puuids.extend(buscar_puuid(dados)[:10])  # Pegando as 10 primeiras ocorrências de "puuid"

    return puuids

# Função principal
def main():
    pasta = escolher_pasta()
    if not pasta:
        print("Nenhuma pasta foi selecionada.")
        return

    puuids = processar_jsons(pasta)

    if puuids:
        # Pegando a data e hora atuais
        data_hora = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Definindo o nome do arquivo com a data e hora
        nome_arquivo = f'puuids_{data_hora}.xlsx'
        
        # Salvando os PUUIDs em um arquivo Excel
        df = pd.DataFrame(puuids, columns=['PUUID'])
        df.to_excel(nome_arquivo, index=False)
        print(f"Arquivo Excel '{nome_arquivo}' gerado com sucesso!")
    else:
        print("Nenhum valor 'puuid' encontrado nos arquivos JSON.")

if __name__ == '__main__':
    main()
