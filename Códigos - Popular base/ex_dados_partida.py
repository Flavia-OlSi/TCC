import requests
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError,ClientError
import time  # Importando o módulo time para utilizar o sleep
import requests
import pandas as pd
import json
from tkinter import Tk, filedialog


def get_s3_client():
    return boto3.client('s3',
        aws_access_key_id='ASIAQ4KQC7P3NPECR7AE',
        aws_secret_access_key='5GFnv2oVFlcNzur0rKWYkd9x81utUujpgsyXTKxP',
        aws_session_token='IQoJb3JpZ2luX2VjECoaCXVzLXdlc3QtMiJHMEUCIQD+DIn5evjjUL1dr6r+uuo4U8eDc7yd4iF0sB+LMPmFRwIgdm35AZO4MRzbqYTDg2UbtG35pMuC4STO4S+30BHHi08qswIIYxAAGgwwNjA4MzQzODA3OTAiDDWIk0LA/ZvhB/ybxSqQAtb5O+hbNqDF/ZmfTrCHMlbrB/wOfvH5cawluiBjb/LyQ4M4+twDuh+pX9yRPxKw3IS7zjnIThJ7SGGP11SCFY5oF6dDdNLH5no3LplUadPAek49WNbkHaKKKZB72SZGKw2r4Tr1cHyPqM6NyyQz6WlvuAiPxhx900M5dn8/DLKoFHmjgwQJECq2+3RrmQfk0RQ8UcDibtXjkxEnoARlyZPr9lP8z8mG0iP2qPRNCmx+RwVUJb4KdsMf/KYFfyD0L6YXPhVQjNXm997zbWkInl1hUTXMID3sQ2dE+eUfnlj8gH79YS2hTmsx/O0IbPy9Rd2iP73IxDxufZeQxJzfa5593dmp0hxtxxuzc3NYC20DMPPDsbcGOp0BzQlVVjZD1StRVI4Q/t1SIfLhA8aU2PJo85lisycqO3bcQF//KF2FyAwZzO9pMB9ZFEAf/W+GCN0egvcB/V80KKBBPfIP5S5/WxwUlvV/uPXAr+ON+z4COFLuXBC5CW02hxZOuMVTsKJfrJyEnf1Fr3lXWHcFHvf87OLBWLmGzjqTQZHPa+SOd9L/zTu5gfJmzlVT2wLo3h3NB3KwVg==',
        region_name='us-east-1')

# Função para escolher o arquivo XLSX
def escolher_arquivo_xlsx():
    root = Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    arquivo = filedialog.askopenfilename(title="Escolha o arquivo XLSX", filetypes=[("Arquivos XLSX", "*.xlsx")])
    return arquivo

# Função para fazer chamada à API e obter os 'puuids'
def obter_puuids(api_key, matchid):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        puuids = [participant['puuid'] for participant in data['info']['participants']]
        return puuids
    else:
        print(f"Erro ao acessar API para matchid {matchid}: {response.status_code}")
        return []

# Função para obter partidas usando o 'puuid'
def obter_partidas_por_puuid(api_key, puuid):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100&api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        partidas = response.json()
        return partidas
    else:
        print(f"Erro ao acessar API para puuid {puuid}: {response.status_code}")
        return []
    
def get_match_info(matchid, api_key):
    if(check_if_object_exists(matchid)):
        return
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        match_info = json.dumps(response.json()).encode('utf-8')
        return match_info
    else:
        400
    
def check_if_object_exists(key):
    s3 = get_s3_client()       
    try:
        # Tenta buscar o objeto no bucket pela key
        s3.head_object(Bucket='match-info', Key=key)
        return True  
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

def upload_to_s3(bucket_name, key, content):
    try:
        s3_client = get_s3_client()        
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=content)
        
        print(f"Arquivo enviado com sucesso para {bucket_name}/{key}")
        
    except NoCredentialsError:
        print("Erro: Credenciais da AWS não encontradas.")
    except PartialCredentialsError:
        print("Erro: Credenciais da AWS incompletas.")
    except Exception as e:
        print(f"Erro ao enviar arquivo para o S3: {e}")

# Função principal para processar o arquivo XLSX e buscar puuids e partidas
def processar_matchids():
    count = 0
    # Escolhe o arquivo XLSX
    caminho_arquivo = escolher_arquivo_xlsx()
    
    # Lê o arquivo XLSX
    df = pd.read_excel(caminho_arquivo)
    
    # Supondo que a coluna que contém os 'matchIds' seja chamada 'matchId'
    matchids = df['matchId']
    
    # Sua API key da Riot
    api_key = "RGAPI-8e90acce-4dd4-4207-8a06-c137b5489dfc"
    
    # Itera sobre cada matchId e faz a chamada à API
    for matchid in matchids:
        puuids = obter_puuids(api_key, matchid)
        if puuids:
            for puuid in puuids:
                # print(f"PUUID para matchid {matchid}: {puuid}")
                
                # Faz a chamada à API para obter as partidas pelo puuid
                partidas = obter_partidas_por_puuid(api_key, puuid)
                
                if partidas:
                    for partida in partidas:
                        match_info = get_match_info(partida, api_key)
                        if match_info != 400:
                            print(f"Partida: {partida} - Puuid: {puuid} ")
                            upload_to_s3('match-info', partida + '.json', match_info)
                            count += 1
                        else:
                            print(f'Next...')

        
    print(f"Total de partidas enviadas para o S3: {count}")

# Chama a função principal
processar_matchids()
