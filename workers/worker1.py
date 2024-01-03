import boto3
from botocore.config import Config
import logging
import os
import json
from dotenv import load_dotenv
from api_open_ia import openai_thread_busca_status,openai_thread_submit_tool

load_dotenv('../config/.env')
logging.basicConfig(filename='worker1-2.log', encoding='utf-8', level=logging.INFO)

print('[worker1] >>> worker1 subiu !!!')
logging.info('[worker1] >>> worker1 subiu !!!')
# Configuração pra usar o LocalStack
localstack_url = 'http://localhost:4566'
aws_access_key_id = 'test'
aws_secret_access_key = 'test'

# Configuração boto3
client_config = Config(
    region_name='us-east-1',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

if os.getenv("SQS")=='LOCAL':    
    # Cria o cliente SQS apontando para o LocalStack
    sqs_client = boto3.client(
        'sqs',
        endpoint_url=localstack_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=client_config
    )
else:
    # Cria o cliente SQS apontando para o LocalStack
    sqs_client = boto3.client('sqs',config=client_config)
    
logging.info('[worker1] SQS='+str(os.getenv("SQS")))
print('[worker1] SQS='+str(os.getenv("SQS")))


# Nome da fila FIFO #SQS_FILA_GPT_ASSINCRONA
queue_name = str(os.getenv("SQS_FILA_01_AGUARDA_STATUS"))
print('[worker1] SQS_FILA_01_AGUARDA_STATUS='+str(queue_name))

try:
    # Pega a URL da fila
    response = sqs_client.get_queue_url(QueueName=queue_name)
    queue_url = response['QueueUrl']
except Exception as e:
    logging.error(f"Erro: {e}")
    
    
logging.info("[worker1] Aguardando mensagens... Para interromper, pressione Ctrl+C")

try:
    while True:
        # Recebe mensagens da fila com uma espera longa
        messages = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        if 'Messages' in messages:
            for message in messages['Messages']:
                status_run=''
                # Processa a mensagem
                logging.info('')          
                body = json.loads(message['Body'])                
                thread_id=body['dados']['thread_id']
                run_id=body['dados']['run_id']
                
                #retorno1 = openai_thread_busca_status(thread_id,run_id)
                logging.info ('[worker1] FAKE VERIFICA STATUS DA THREAD!!!!')

                
                if status_run=='requires_action':
                  logging.info ('status_run=requires_action')
                
                if (1==2):
                  # Deleta a mensagem da fila após processá-la
                  sqs_client.delete_message(
                       QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                   )
                  logging.info(f"[worker1] Mensagem verifica status da thread foi Removida da fila: {message['ReceiptHandle']}")
        else:
            # Se não há mensagens, o loop continua
            logging.info("[worker1] Nenhuma mensagem nova.")
except KeyboardInterrupt:
    logging.error("[worker1] \nInterrompido pelo usuário.")