import requests
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

APIKEY = 'RGAPI-f565e5e5-682c-4c40-9401-56a976cdfe08'

def get_matchs(puuid):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100&api_key={APIKEY}"
    response = requests.get(url)
    if response.status_code == 200:
        upload_to_s3('puuids', puuid, '')
        return response.json()
    
def get_match_info(matchid):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={APIKEY}"
    response = requests.get(url)
    if response.status_code == 200:
        match_info = json.dumps(response.json()).encode('utf-8')
        return match_info
    
def get_s3_client():
    return boto3.client('s3',
        aws_access_key_id='ASIAQ4KQC7P3O3RQ7R75',
        aws_secret_access_key='aBf37g7k1VwknGL06IuRCqEgmuc4bHcM5tnObXCs',
        aws_session_token='IQoJb3JpZ2luX2VjEMr//////////wEaCXVzLXdlc3QtMiJHMEUCIG1nJnzJCfLeNFy6FEdrwBovHWVoqeWJXey6rbLyagd3AiEAu1p7Jugnm+jFdW5hXaZ6GU474xiKNhFJ84GDrs4a/xkqvAII8v//////////ARAAGgwwNjA4MzQzODA3OTAiDCAe/rh6a5meRaVzNyqQAhkHwCLLdGqJJEgh3p+rtoaEOrOmOBiHzGC+Hp5oYQj2jgB0hH8e/9oWHAUUJL41Av98fBqB9UOmz/LU9EaWzT3Abgdx7k86lHTbtE7xVeclXMpK84cjN+D7wbjncFJT6WTL/GaUqSdnymlPvtaOv8GJgfNkc+njGjLpOyiYXgRjZUq4xTF5C+RUbonAFMtNzH9awdlHS3iso1Z+bC8wDrvvrb5zNJ3FfTPSdxeuhCtIAA5/NfkZV/VzUHzIN8wjU7IaSIuY9zvErPlTRsF/JHO1UtXR03Ny2733Rbn50mY5Xe0Uq/EVROIOTvOL/XMEbec5fFuUhcpcAnhQdnLfwrwzf0tSawuntamI+zQDfMDlMLmunLcGOp0BQ4sxqieWJLp6VLE/JTzC9RVpOIzNz+q4BrgaUiuteMykdbizWfzkcqHpXuSSpUx63SFuRX03mI+j+vMQCb5lpIjS+O9x9hkPRBkTx7RwF2SeMBe6/ReM1w0DiWxWOVTGrXfMCg8jvWyxHnDacPgrUZgqw9S13aS8j5hy1D0p78apEBduhdaA25PTsgWFXmZQav0Hj+GqBrHgIeqxdA==',
        region_name='us-east-1')

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