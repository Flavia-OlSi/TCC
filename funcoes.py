import requests
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

APIKEY = 'RGAPI-588cf19f-24f7-4d28-acbf-d51e67dd58b9'

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
        aws_access_key_id='ASIAQ4KQC7P3J74ETMIK',
        aws_secret_access_key='aoyHC2aqGMxUn9k9gDECURqEhgO/fsEF5peOYc+2',
        aws_session_token='IQoJb3JpZ2luX2VjEDAaCXVzLXdlc3QtMiJHMEUCIQDe9+jffpwXPAbR/L9O7Pt1h9MLJlzIO0jS4Z5+kPbXdAIgD1WhfI9kpvzp6yCFH3HiRGXvzDr6O7YhAxpv8jyjPSIqswIISRAAGgwwNjA4MzQzODA3OTAiDGxI/FmEm8QbN10kRCqQAolFloaSW9g4daSDHDilg2CjLelM6pibK93cQ2NNj0FKV3ZM/O+croxdaEC6MeeOf/10q7Xq4c+B4vaAXBegw8UapvNWjmtP/mA65f4lEgTKdk9IdqOEcHugoWxvSoM4BpV4IPeV7bB9qYx34Q+e1nSz/eznMDTb3mGjy3IoUNvJ9ywtNosfx+CEDkj1sZN3zSXife2S6WA5fJX9+UUIk5w+iHqbkfjrQKYLEWt85dtSUdIp4+WcSn5ARFR1lBgBPrCXlcYFaSrSuHjhDbKRBB/BoPn8STZkOTvqG6nhZ0tZJB1VigNFbKfzf2w8fyNzvEBFokbOGbDpb8dl+GUZsAD72sdvcXNOfyoyqxSLvaDWMIq3wrYGOp0BDbBY1BPSXHETt7fVoLZNCWR+iymeBaiLWz5prHqoELC2BB2b7DNnGBC7Q6LZN08DZ4s2i95qGSnJ+1jMI35DF9F8xVVWX2kd32ZMPJFChh+bDncAaMZslIsl8h0uyAe6xXnietIzD/56jQaQS9L7e41/hHQuaGSVCmt4n9C4uK4y1Fms6EPRieTLZXQe82i8ebrqfrieXb/2VMfbyw==',
        region_name='us-east-1'  )

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